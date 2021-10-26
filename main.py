from flask import Flask, Response, jsonify, request
from plyvel import DB # type: ignore

db: DB = DB('database', create_if_missing=True)
app: Flask = Flask(__name__)

@app.get('/')
def root() -> Response:
    return Response(status=200)

@app.get('/<prefix>')
def read(prefix: str) -> Response:
    items = []

    for _, value in db.iterator(prefix=prefix.encode()):
        items.append(value.decode())

    return jsonify(items)

@app.post('/<id>')
@app.put('/<id>')
def write(id: str) -> Response:
    db.put(id.encode(), str(request.json).encode())

    return Response(status=200)

@app.delete('/<id>')
def delete(id: str) -> Response:
    db.delete(id.encode())

    return Response(status=200)

if __name__ == '__main__':
    app.run()
