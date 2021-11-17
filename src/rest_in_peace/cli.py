from sys import argv
from .database import Database
from .server import Server

db = Database(argv[1] if len(argv) > 1 else 'database.db')
app = Server(int(argv[2]) if len(argv) > 2 else 8000)

@app.get('/openapi.json')
def openapi():
    definitions = {
        'openapi': '3.0.0',
        'servers': [{'url': 'http://localhost:8000'}],
        'info': {'title': 'API', 'version': '1.0.0'},
        'paths': {
            '/': {'get': {'description': 'Static index.html contained in /public folder'}},
            '/openapi.json': {'get': {'description': 'Return API definitions'}}
        },
        'components': {'schemas': {}}
    }

    for table, columns in db.schema().items():
        definitions['paths'][f'/{table}'] = {
            'get': {'description': f'Return all {table}'},
            'post': {'description': f'Create a new item for {table} and return the created item'},
            'delete': {'description': f'Delete all {table} structure and remove routes'}
        }
        definitions['paths'][f'/{table}/{{id}}'] = {
            'get': {'description': f'Return an specific item from {table}'},
            'put': {'description': f'Update an specific item from {table}'},
            'delete': {'description': f'Delete an specific item from {table}'}
        }
        definitions['components']['schemas'][table] = {"properties": {}}

        for row_name, row_type in columns.items():
            definitions['components']['schemas'][table]["properties"][row_name] = {
                "type": 'string' if row_type == 'TEXT' else 'NUMBER' if row_type == 'REAL' else row_type.lower()
            }

    return definitions

@app.get('/{collection}')
def list(collection: str, params: dict = {}):
    return db.list(collection, params)

@app.post('/{collection}')
def create(collection: str, body: dict):
    db.table(collection, body)
    return db.create(collection, body)

@app.delete('/{collection}')
def drop(collection: str):
    return db.drop(collection)

@app.get('/{collection}/{id}')
def read(collection: str, id: str):
    return db.read(collection, id)

@app.put('/{collection}/{id}')
def update(collection: str, id: str, body: dict):
    return db.update(collection, id, body)

@app.delete('/{collection}/{id}')
def delete(collection: str, id: str):
    db.delete(collection, id)

def main():
    app.run()

if __name__ == '__main__':
    main()
