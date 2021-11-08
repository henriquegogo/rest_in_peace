from server import Server
from database import Database

app = Server()
db = Database()

@app.get('/schema.json')
def schema():
    return db.schema()

@app.get('/{collection}')
def list(collection: str, params: dict = {}):
    return db.list(collection, params)

@app.post('/{collection}')
def create(collection: str, body: dict):
    return db.create(collection, body)

@app.get('/{collection}/{id}')
def read(collection: str, id: str):
    return db.read(collection, id)

@app.put('/{collection}/{id}')
def update(collection: str, id: str, body: dict):
    return db.update(collection, id, body)

@app.delete('/{collection}/{id}')
def delete(collection: str, id: str):
    db.delete(collection, id)

if __name__ == '__main__':
    app.run()
