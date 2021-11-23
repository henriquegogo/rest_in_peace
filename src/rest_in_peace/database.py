import sqlite3

class Database:
    def __init__(self, db_path: str = 'database.db'):
        connection = sqlite3.connect(db_path)
        self.cursor = connection.cursor()
        self.execute = self.cursor.execute
        self.commit = connection.commit

    def schema(self):
        result = {}

        for table in [row[0] for row in
                      self.execute('SELECT name FROM sqlite_master WHERE type="table" AND name NOT LIKE "sqlite_%"')]:
            result[table] = {}

            for row in self.execute(f'PRAGMA table_info({table})'):
                result[table][row[1]] = row[2]

        return result

    def table(self, table: str, data: dict):
        schema = [row[1] for row in self.execute(f'PRAGMA table_info({table})')]

        if not len(schema):
            self.execute(f'CREATE TABLE {table} (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE)')

        for key, value in data.items():
            column_type = 'INTEGER' if isinstance(value, int) else 'REAL' if isinstance(value, float) else 'TEXT'
            if key not in schema: self.execute(f'ALTER TABLE {table} ADD COLUMN {key} {column_type}')

    def drop(self, table: str):
        self.execute(f'DROP TABLE {table}')
        self.commit()
        return ''

    def list(self, table: str, params: dict):
        schema = [row[1] for row in self.execute(f'PRAGMA table_info({table})')]
        where = ' AND '.join([f'{key}="{params[key]}"' for key in params.keys()
                              if key not in ['orderby', 'limit', 'offset']])
        orderby = params['orderby'] if 'orderby' in params else 'id ASC'
        limit = params['limit'] if 'limit' in params else '10'
        offset = params['offset'] if 'offset' in params else '0'

        return [dict(zip(schema, row)) for row in
                self.execute(f'SELECT * FROM {table} WHERE {where if where else 1} \
                             ORDER BY {orderby} LIMIT {limit} OFFSET {offset}')]

    def create(self, table: str, body: dict):
        keys = ', '.join(list(body.keys()))
        values = str(list(body.values()))[1:-1]
        self.execute(f'INSERT INTO {table} ({keys}) VALUES ({values})')
        self.commit()

        return self.read(table, str(self.cursor.lastrowid))

    def read(self, table: str, id: str):
        schema = [row[1] for row in self.execute(f'PRAGMA table_info({table})')]

        return [dict(zip(schema, row)) for row in
                self.execute(f'SELECT * FROM {table} WHERE id = {id} LIMIT 1')][0]

    def update(self, table: str, id: str, body: dict):
        for key, value in body.items(): self.execute(f'UPDATE {table} SET {key} = "{value}" WHERE id = {id}')
        self.commit()

        return self.read(table, id)

    def delete(self, table: str, id: str):
        data = self.read(table, id)
        self.execute(f'DELETE FROM {table} WHERE id = {id}')
        self.commit()

        return data
