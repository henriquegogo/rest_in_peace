from server import Server
from database import Database

app = Server()
db = Database()

@app.get('/')
def schema(params: dict = {}):
    return db.schema()

@app.get('/{collection}')
def list(collection: str, params: dict = {}):
    return db.list(collection)

@app.post('/{collection}')
def create(collection: str, body: dict):
    return db.create(collection, body)

@app.get('/{collection}/{id}')
def read(collection: str, id: str, params: dict = {}):
    return db.read(collection, id)

@app.put('/{collection}/{id}')
def update(collection: str, id: str, body: dict):
    return db.update(collection, id, body)

@app.delete('/{collection}/{id}')
def delete(collection: str, id: str):
    db.delete(collection, id)

if __name__ == '__main__':
    app.run()
