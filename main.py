import sqlite3

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


class Database():
    def __init__(self):
        self.connection = sqlite3.connect('./database.db')
        self.execute = self.connection.cursor().execute


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
        for row in self.execute(f'SELECT * FROM {table} WHERE id = ?', id):
            for i in range(len(row)):
                item[schema[i]] = row[i]
            break;

        return item


    def insert(self, table, data):
        self.execute(f'INSERT INTO {table} (name) VALUES(?)', data)


app = FastAPI()

@app.get('/api')
def tables():
    db = Database()
    tables = db.tables()
    return tables

@app.get('/api/{table}')
def findall(table):
    db = Database()
    items = db.findall(table, 'TRUE')
    return items

@app.get('/api/{table}/{id}')
def findone(table, id):
    db = Database()
    items = db.findone(table, id)
    return items

app.mount('/', StaticFiles(directory='.', html=True), name="static")
