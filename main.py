from fastapi import Body, FastAPI
from uvicorn import run # type: ignore
from plyvel import DB # type: ignore
import json

db = DB('database', create_if_missing=True)
app: FastAPI = FastAPI()

@app.get('/{prefix}')
def read(prefix):
    return [json.loads(value.decode()) for _, value in db.iterator(prefix=prefix.encode())]

@app.post('/{id}')
def write(id, body = Body(None)):
    return db.put(id.encode(), json.dumps(body).encode())

@app.delete('/{id}')
def delete(id):
    return db.delete(id.encode())

if __name__ == '__main__':
    run('__main__:app')
