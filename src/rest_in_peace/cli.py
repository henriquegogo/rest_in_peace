from sys import argv
from .database import Database
from .server import Server
from .openapi import openapi

db = Database(argv[1] if len(argv) > 1 else 'database.db')
app = Server(int(argv[2]) if len(argv) > 2 else 8000)

@app.get('/openapi.json')
def definitions():
    return openapi(db.schema(), 'localhost', app.port)

@app.get('/{collection}')
def list(collection: str, params: dict = {}):
    return db.list(collection, params)

@app.post('/{collection}')
def create(collection: str, body: dict):
    db.table(collection, body)
    return db.create(collection, body), '201 Created'

@app.delete('/{collection}')
def drop(collection: str):
    return db.drop(collection), '204 No Content'

@app.get('/{collection}/{id}')
def read(collection: str, id: str):
    return db.read(collection, id)

@app.put('/{collection}/{id}')
def update(collection: str, id: str, body: dict):
    return db.update(collection, id, body)

@app.delete('/{collection}/{id}')
def delete(collection: str, id: str):
    return db.delete(collection, id)

def main():
    app.run()

if __name__ == '__main__':
    main()
