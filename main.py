from fastapi import Body, FastAPI, HTTPException
from uvicorn import run # type: ignore
import sqlite3

db_path = 'database.db'
app = FastAPI()

def column_type(value):
    try:
        int(value)
        return 'INTEGER'
    except:
        return 'TEXT'

@app.get('/')
def root():
    db = sqlite3.connect(db_path).cursor()
    return [row[0] for row in
            db.execute('SELECT name FROM sqlite_master WHERE type="table" AND name NOT LIKE "sqlite_%"')]

@app.get('/{collection}')
def list(collection: str):
    db = sqlite3.connect(db_path).cursor()
    try:
        schema = [row[1] for row in db.execute(f'PRAGMA table_info({collection})')]
        return [zip(schema, row) for row in db.execute(f'SELECT * FROM {collection}')]
    except: raise HTTPException(status_code=404)

@app.post('/{collection}')
def create(collection: str, body: dict = Body(None)):
    connection = sqlite3.connect(db_path)
    db = connection.cursor()
    try: db.execute(f'CREATE TABLE {collection} (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE)')
    except: pass
    try: [db.execute(f'ALTER TABLE {collection} ADD COLUMN {key} {column_type(value)}') for key, value in body.items()]
    except: pass
    try:
        keys = ', '.join([key for key in body.keys()])
        values = str(tuple([value for value in body.values()]))
        db.execute(f'INSERT INTO {collection} ({keys}) VALUES {values}')
        connection.commit()
        return HTTPException(status_code=201)
    except: raise HTTPException(status_code=400)

@app.get('/{collection}/{id}')
def read(collection: str, id: str):
    db = sqlite3.connect(db_path).cursor()
    try:
        schema = [row[1] for row in db.execute(f'PRAGMA table_info({collection})')]
        return [zip(schema, row) for row in db.execute(f'SELECT * FROM {collection} WHERE id = ?', id)][0]
    except: raise HTTPException(status_code=404)

#WIP
@app.put('/{collection}/{id}')
def update(collection: str, id: str, body: dict = Body(None)):
    connection = sqlite3.connect(db_path)
    db = connection.cursor()
    try:
        [db.execute(f'UPDATE {collection} SET {key} = "{value}" WHERE id = ?', id) for key, value in body.items()]
        connection.commit()
        return HTTPException(status_code=200)
    except: raise HTTPException(status_code=400)

@app.delete('/{collection}/{id}')
def delete(collection: str, id: str):
    connection = sqlite3.connect(db_path)
    db = connection.cursor()
    try:
        db.execute(f'DELETE FROM {collection} WHERE id = ?', id)
        connection.commit()
        return HTTPException(status_code=200)
    except: raise HTTPException(status_code=404)

if __name__ == '__main__':
    run('__main__:app')
