from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine


class Database():
    def __init__(self):
        self.execute = create_engine('sqlite:///database.db').execute


    def tables(self):
        items = []
        for row in self.execute('SELECT name FROM sqlite_master WHERE type="table" OR type="view"'):
            if row[0][0:7] != 'sqlite_': items.append(row[0])

        return items


    def findall(self, table, where):
        schema = []
        for row in self.execute(f'PRAGMA table_info({table})'):
            schema.append(row[1])

        items = []
        for row in self.execute(f'SELECT * FROM {table} WHERE {where}'):
            item = {}
            for i in range(len(row)):
                item[schema[i]] = row[i]

            items.append(item)

        return items


    def findone(self, table, id):
        schema = []
        for row in self.execute(f'PRAGMA table_info({table})'):
            schema.append(row[1])

        item = {}
        for row in self.execute(f'SELECT * FROM {table} WHERE id = {id}'):
            for i in range(len(row)):
                item[schema[i]] = row[i]
            break;

        return item


    def insert(self, table, data):
        self.execute(f'INSERT INTO {table} (name) VALUES({data})')


db = Database()
app = FastAPI()

@app.get('/api')
def tables():
    tables = db.tables()
    return tables

@app.get('/api/{table}')
def findall(table, where = 'TRUE'):
    items = db.findall(table, where)
    return items

@app.get('/api/{table}/{id}')
def findone(table, id):
    items = db.findone(table, id)
    return items

app.mount('/', StaticFiles(directory='.', html=True), name="static")
