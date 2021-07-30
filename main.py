from flask import Flask, Response, jsonify, request
from plyvel import DB # type: ignore
from uuid import uuid4

db: DB = DB('database', create_if_missing=True)
app: Flask = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.get('/')
def root() -> Response:
    items: dict[str, str] = {}

    for key, value in db.iterator():
        items[key.decode()] = value.decode()

    return jsonify(items)

@app.post('/')
def create() -> Response:
    id: str = str(uuid4())
    data: str = request.get_data(as_text=True)

    db.put(id.encode(), data.encode())

    return Response(status=200)

@app.get('/<id>')
def read(id: str) -> Response:
    data: str = db.get(id.encode()).decode()

    return jsonify(data)

@app.put('/<id>')
def update(id: str, body: str) -> Response:
    data: str = db.put(id.encode(), body.encode())

    return jsonify(data)

@app.delete('/<id>')
def delete(id: str) -> Response:
    db.delete(id.encode())

    return Response(status=200)

if __name__ == '__main__':
    app.run()
