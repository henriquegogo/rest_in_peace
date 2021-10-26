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

@app.get('/{prefix}')
def list(prefix):
    return [json.loads(value.decode()) for _, value in db.iterator(prefix=(prefix + '/').encode())]

@app.get('/{prefix}/{id}')
def read(prefix, id):
    return json.loads(db.get((prefix + '/' + id).encode()))

@app.post('/')
@app.post('/{prefix}')
def write(prefix = None, body = Body(None)):
    body['id'] = str(uuid4())
    key = prefix + '/' + body['id'] if prefix else body['id']
    db.put(key.encode(), json.dumps(body).encode())
    return

@app.put('/{id}')
@app.put('/{prefix}/{id}')
def update(id, prefix = None, body = Body(None)):
    key = prefix + '/' + id if prefix else id
    db.put(key.encode(), json.dumps(body).encode())
    return

@app.delete('/{id}')
@app.delete('/{prefix}/{id}')
def delete(id, prefix = None):
    key = prefix + '/' + id if prefix else id
    db.delete(key.encode())
    return

if __name__ == '__main__':
    run('__main__:app')
