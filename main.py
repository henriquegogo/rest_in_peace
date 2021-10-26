from fastapi import Body, FastAPI
from uvicorn import run # type: ignore
from plyvel import DB # type: ignore
from uuid import uuid4
import json

db = DB('database', create_if_missing=True)
app: FastAPI = FastAPI()

@app.get('/')
def root():
    return [key.decode() for key, _ in db.iterator()]

@app.get('/{collection}')
def list(collection):
    return [json.loads(value.decode())
            for _, value in db.iterator(prefix=(collection + '/').encode())]

@app.get('/{collection}/{id}')
def read(collection, id):
    return json.loads(db.get((collection + '/' + id).encode()))

@app.post('/')
@app.post('/{collection}')
def write(collection = None, body = Body(None)):
    body['id'] = str(uuid4())
    key = collection + '/' + body['id'] if collection else body['id']
    db.put(key.encode(), json.dumps(body).encode())
    return

@app.put('/{id}')
@app.put('/{collection}/{id}')
def update(id, collection = None, body = Body(None)):
    key = collection + '/' + id if collection else id
    db.put(key.encode(), json.dumps(body).encode())
    return

@app.delete('/{id}')
@app.delete('/{collection}/{id}')
def delete(id, collection = None):
    key = collection + '/' + id if collection else id
    db.delete(key.encode())
    return

if __name__ == '__main__':
    run('__main__:app')
