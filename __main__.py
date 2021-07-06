from sys import argv
from typing import Dict, Iterator, List, Tuple, Union

from flask import Flask, jsonify, request
from flask.wrappers import Response
from sqlalchemy import create_engine

Alphanum = Union[str, int, float]


class Database():
    def __init__(self) -> None:
        self.execute = create_engine(f'sqlite:///{argv[1] if len(argv) > 1 else "database.db"}').execute


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
        return self.findall(table, f'id = {id}')[0]


    def insert(self, table: str, keys: List[str], values: List[str]) -> None:
        self.execute(f'INSERT INTO {table} ({", ".join(keys)}) VALUES({", ".join(values)})')


db: Database = Database()
app: Flask = Flask(__name__)

@app.get('/')
def tables() -> Response:
    tables: List[str] = db.tables()
    return jsonify(tables)

@app.get('/<table>')
def findall(table: str) -> Response:
    args: Iterator[Tuple[str, str]] = request.args.items()
    criteria: List[str] = [f'{arg[0]}="{arg[1]}"' for arg in args]
    where = ' AND '.join(criteria) if len(criteria) > 0 else 'TRUE'
    items: List[Dict[str, Alphanum]] = db.findall(table, where)
    return jsonify(items)

@app.get('/<table>/<id>')
def findone(table: str, id: int) -> Response:
    items: Dict[str, Alphanum] = db.findone(table, id)
    return jsonify(items)

@app.post('/<table>')
def insert(table: str) -> Response:
    keys: List[str] = list(request.form.keys())
    values: List[str] = [f'"{value}"' for value in request.form.values()]
    db.insert(table, keys, values)
    return jsonify('OK')

if __name__ == '__main__':
    app.run()
