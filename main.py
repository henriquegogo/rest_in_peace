from flask import Flask, Response, jsonify, request
from plyvel import DB # type: ignore
from uuid import uuid4

db: DB = DB('database', create_if_missing=True)
app: Flask = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.get('/')
def root() -> Response:
    items: list[str] = []

    for _, value in db.iterator(prefix=b'_tables:'):
        items.append(value.decode())

    return jsonify(items)

@app.get('/<collection>')
def list(collection: str) -> Response:
    items: dict[str, str] = {}

    for key, value in db.iterator(prefix=(collection + ':').encode()):
        prefix_length = len(collection) + 1
        items[key.decode()[prefix_length:]] = value.decode()

    return jsonify(items)

@app.post('/<collection>')
def create(collection: str) -> Response:
    key: str = collection + ':' + str(uuid4())
    data: str = request.get_data(as_text=True)

    db.put(('_tables:' + collection).encode(), collection.encode())
    db.put(key.encode(), data.encode())

    return Response(status=200)

@app.get('/<collection>/<id>')
def read(collection: str, id: str) -> Response:
    key: str = collection + ':' + id
    data: str = db.get(key.encode()).decode()

    return jsonify(data)

@app.put('/<collection>/<id>')
def update(collection: str, id: str) -> Response:
    key: str = collection + ':' + id
    data: str = request.get_data(as_text=True)

    db.put(key.encode(), data.encode())

    return Response(status=200)

@app.delete('/<collection>/<id>')
def delete(collection: str, id: str) -> Response:
    key: str = collection + ':' + id
    db.delete(key.encode())

    return Response(status=200)

if __name__ == '__main__':
    app.run()
