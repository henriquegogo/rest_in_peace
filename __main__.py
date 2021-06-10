from typing import Dict, List, Union

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine # type: ignore
from sys import argv
from uvicorn import run # type: ignore

Alphanum = Union[str, int, float]


class Database():
    def __init__(self) -> None:
        self.execute = create_engine(f'sqlite:///{argv[1] or "database.db"}').execute


    def tables(self) -> List[str]:
        items: List[str] = []
        for row in self.execute('SELECT name FROM sqlite_master WHERE type="table" OR type="view"'):
            if row[0][0:7] != 'sqlite_': items.append(row[0])

        return items


    def findall(self, table: str, where: str) -> List[Dict[str, Alphanum]]:
        schema: List[str] = []
        for row in self.execute(f'PRAGMA table_info({table})'):
            schema.append(row[1])

        items: List[Dict[str, Alphanum]] = []
        for row in self.execute(f'SELECT * FROM {table} WHERE {where}'):
            item: Dict[str, Alphanum] = {}
            for i in range(len(row)):
                item[schema[i]] = row[i]

            items.append(item)

        return items


    def findone(self, table: str, id: int) -> Dict[str, Alphanum]:
        schema: List[str] = []
        for row in self.execute(f'PRAGMA table_info({table})'):
            schema.append(row[1])

        item: Dict[str, Alphanum] = {}
        for row in self.execute(f'SELECT * FROM {table} WHERE id = {id}'):
            for i in range(len(row)):
                item[schema[i]] = row[i]
            break;

        return item


    def insert(self, table: str, data: str) -> None:
        self.execute(f'INSERT INTO {table} (name) VALUES({data})')


db: Database = Database()
app: FastAPI = FastAPI()

@app.get('/api')
def tables() -> List[str]:
    tables: List[str] = db.tables()
    return tables

@app.get('/api/{table}')
def findall(table: str, where: str = 'TRUE') -> List[Dict[str, Alphanum]]:
    items: List[Dict[str, Alphanum]] = db.findall(table, where)
    return items

@app.get('/api/{table}/{id}')
def findone(table: str, id: int) -> Dict[str, Alphanum]:
    items: Dict[str, Alphanum] = db.findone(table, id)
    return items

app.mount('/', StaticFiles(directory='.', html=True), name="static")

if __name__ == '__main__':
    run('__main__:app')
