from fastapi import Body, FastAPI, HTTPException
from uvicorn import run # type: ignore
import sqlite3

class Database:
    db_path = 'database.db'

    def __init__(self):
        connection = sqlite3.connect(self.db_path)
        self.execute = connection.cursor().execute
        self.commit = connection.commit

    @staticmethod
    def column_type(value):
        try:
            int(str(value))
            return 'INTEGER'
        except: pass
        try:
            float(str(value))
            return 'REAL'
        except: pass
        return 'TEXT'

    def tables(self):
        return [row[0] for row in
                self.execute('SELECT name FROM sqlite_master WHERE type="table" AND name NOT LIKE "sqlite_%"')]

    def list(self, collection: str):
        schema = [row[1] for row in self.execute(f'PRAGMA table_info({collection})')]
        return [zip(schema, row) for row in self.execute(f'SELECT * FROM {collection}')]

    def create(self, collection: str, body: dict):
        try: self.execute(f'CREATE TABLE {collection} (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE)')
        except: pass
        schema = [row[1] for row in self.execute(f'PRAGMA table_info({collection})')]
        for key, value in body.items():
            if key not in schema: self.execute(f'ALTER TABLE {collection} ADD COLUMN {key} {Database.column_type(value)}')
        keys = ', '.join([key for key in body.keys()])
        values = str([value for value in body.values()])[1:-1]
        self.execute(f'INSERT INTO {collection} ({keys}) VALUES ({values})')
        self.commit()

    def read(self, collection: str, id: str):
        schema = [row[1] for row in self.execute(f'PRAGMA table_info({collection})')]
        return [zip(schema, row) for row in self.execute(f'SELECT * FROM {collection} WHERE id = ?', id)][0]

    def update(self, collection: str, id: str, body: dict):
        for key, value in body.items(): self.execute(f'UPDATE {collection} SET {key} = "{value}" WHERE id = ?', id)
        self.commit()

    def delete(self, collection: str, id: str):
        self.execute(f'DELETE FROM {collection} WHERE id = ?', id)
        self.commit()

app = FastAPI()

@app.get('/')
def root():
    return Database().tables()

@app.get('/{collection}')
def list(collection: str):
    try: return Database().list(collection)
    except: raise HTTPException(status_code=404)

@app.post('/{collection}')
def create(collection: str, body: dict = Body(None)):
    try:
        Database().create(collection, body)
        return HTTPException(status_code=201)
    except: raise HTTPException(status_code=400)

@app.get('/{collection}/{id}')
def read(collection: str, id: str):
    try: return Database().read(collection, id)
    except: raise HTTPException(status_code=404)

@app.put('/{collection}/{id}')
def update(collection: str, id: str, body: dict = Body(None)):
    try:
        Database().update(collection, id, body)
        return HTTPException(status_code=200)
    except: raise HTTPException(status_code=400)

@app.delete('/{collection}/{id}')
def delete(collection: str, id: str):
    try:
        Database().delete(collection, id)
        return HTTPException(status_code=200)
    except: raise HTTPException(status_code=404)

if __name__ == '__main__':
    run('__main__:app')
