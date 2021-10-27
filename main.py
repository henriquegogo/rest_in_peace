from fastapi import Body, FastAPI
from uvicorn import run # type: ignore
from plyvel import DB # type: ignore
from uuid import uuid4
import json

db = DB('database', create_if_missing=True)
app = FastAPI()

@app.get('/')
def root(limit: int = 10, offset: int = 0):
    return [key.decode() for key, _ in db][offset:offset+limit]

@app.get('/{collection}')
def list(collection: str, limit: int = 10, offset: int = 0):
    return [json.loads(value.decode())
            for _, value in db.iterator(prefix=(collection + '/').encode())
            ][offset:offset+limit]

@app.get('/{collection}/{id}')
def read(collection: str, id: str):
    return json.loads(db.get((collection + '/' + id).encode()))

@app.post('/{collection}')
def write(collection: str, body: dict = Body(None)):
    body['id'] = str(uuid4())
    key = collection + '/' + body['id']
    return db.put(key.encode(), json.dumps(body).encode())

@app.put('/{collection}/{id}')
@app.post('/{collection}/{id}')
def update(collection: str, id: str, body: dict = Body(None)):
    key = collection + '/' + id
    return db.put(key.encode(), json.dumps(body).encode())

@app.delete('/{collection}/{id}')
def delete(collection: str, id: str):
    key = collection + '/' + id
    return db.delete(key.encode())

if __name__ == '__main__':
    run('__main__:app')
