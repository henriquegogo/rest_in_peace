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
    items: dict[str, str] = {}
    search: Optional[str] = request.args.get('q')

    for key, value in db.iterator(prefix=(collection + ':').encode()):
        if search and search not in value.decode():
            continue

        prefix_length = len(collection) + 1
        id: str = key.decode()[prefix_length:]

        try:
            items[id] = json.loads(value.decode())
        except:
            items[id] = value.decode()

    return jsonify(items)

@app.post('/<collection>')
def create(collection: str) -> Response:
    key: str = collection + ':' + str(uuid4())
    db.put(('_collections:' + collection).encode(), collection.encode())

    if request.json:
        data: Optional[str] = json.dumps(request.json)
        db.put(key.encode(), data.encode())
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
        return json.loads(data.decode())
    else:
        items: dict[str, str] = {}

        for prop, value in db.iterator(prefix=(key + ':').encode()):
            prefix_length = len(key) + 1
            items[prop.decode()[prefix_length:]] = value.decode()

        return jsonify(items)

@app.put('/<collection>/<id>')
def update(collection: str, id: str) -> Response:
    key: str = collection + ':' + id

    if request.json:
        data: Optional[str] = str(request.json)
        db.put(key.encode(), data.encode())
    else:
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
