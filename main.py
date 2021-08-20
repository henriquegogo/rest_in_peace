from flask import Flask, Response, jsonify, request
from plyvel import DB # type: ignore
from uuid import uuid4
from typing import Optional
import json

db: DB = DB('database', create_if_missing=True)
app: Flask = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.get('/')
def root() -> Response:
    items = []

    for _, value in db.iterator(prefix=b'_collections:'):
        items.append(value.decode())

    return jsonify(items)

@app.get('/<collection>')
def list(collection: str) -> Response:
    items = {}
    search: Optional[str] = request.args.get('q')

    for prefix_key, value in db.iterator(prefix=(collection + ':').encode()):
        if search and search not in value.decode():
            continue

        prefix_length: int = len(collection) + 1
        key: str = prefix_key.decode()[prefix_length:]
        id: str = key.split(':')[0]

        try:
            if value.decode().isnumeric():
                raise
            else:
                items[id] = json.loads(value.decode())
        except:
            if len(key) > len(id) and ':' in key:
                if not id in items:
                    items[id] = {}
                elif type(items[id]) is str:
                    items[key] = value.decode()
                    continue

                prop: str = key.split(':')[1]
                items[id][prop] = value.decode()
            else:
                items[id] = value.decode()

    return jsonify(items)

@app.post('/<collection>')
def create(collection: str) -> Response:
    key: str = collection + ':' + str(uuid4())
    data_string: str = request.get_data(as_text=True)
    db.put(('_collections:' + collection).encode(), collection.encode())


    if request.json:
        data: Optional[str] = json.dumps(request.json)
        db.put(key.encode(), data.encode())
    elif '=' not in data_string:
        db.put(key.encode(), data_string.encode())
    else:
        for arg in request.form:
            data: Optional[str] = request.form.get(arg)
            db.put((key + ':' + arg).encode(), data.encode())

    return Response(status=200)

@app.get('/<collection>/<id>')
def read(collection: str, id: str) -> Response:
    key: str = collection + ':' + id
    data: bytes = db.get(key.encode())

    if data:
        try:
            return json.loads(data.decode())
        except:
            return Response(data.decode())
    else:
        items: dict[str, str] = {}

        for prop, value in db.iterator(prefix=(key + ':').encode()):
            prefix_length = len(key) + 1
            items[prop.decode()[prefix_length:]] = value.decode()

        return jsonify(items)

@app.put('/<collection>/<id>')
def update(collection: str, id: str) -> Response:
    key: str = collection + ':' + id
    data_string: str = request.get_data(as_text=True)

    if request.json:
        data: Optional[str] = str(request.json)
        db.put(key.encode(), data.encode())
    elif '=' not in data_string:
        db.put(key.encode(), data_string.encode())
    else:
        db.delete(key.encode())
        for arg in request.form:
            data: Optional[str] = request.form.get(arg)
            db.put((key + ':' + arg).encode(), data.encode())

    return Response(status=200)

@app.delete('/<collection>/<id>')
def delete(collection: str, id: str) -> Response:
    key: str = collection + ':' + id
    db.delete(key.encode())

    for prop, _ in db.iterator(prefix=(key + ':').encode()):
        db.delete(prop)

    return Response(status=200)

if __name__ == '__main__':
    app.run()
