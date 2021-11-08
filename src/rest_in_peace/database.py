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

    def list(self, collection: str, params: dict):
        schema = [row[1] for row in self.execute(f'PRAGMA table_info({collection})')]
        where = ' AND '.join([f'{key}="{params[key]}"' for key in params.keys()
                              if key not in ['orderby', 'limit', 'offset']])

        return [dict(zip(schema, row)) for row in
                self.execute(f'SELECT * FROM {collection} \
                             WHERE {where if where else "TRUE"} \
                             ORDER BY {params["orderby"] if "orderby" in params else "id ASC"} \
                             LIMIT {params["limit"] if "limit" in params else 10} \
                             OFFSET {params["offset"] if "offset" in params else 0}')]

    def create(self, collection: str, body: dict):
        schema = [row[1] for row in self.execute(f'PRAGMA table_info({collection})')]
        if not len(schema):
            self.execute(f'CREATE TABLE {collection} (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE)')

        for key, value in body.items():
            column_type = 'INTEGER' if isinstance(value, int) else 'REAL' if isinstance(value, float) else 'TEXT'
            if key not in schema: self.execute(f'ALTER TABLE {collection} ADD COLUMN {key} {column_type}')

        keys = ', '.join([key for key in body.keys()])
        values = str([value for value in body.values()])[1:-1]

        self.execute(f'INSERT INTO {collection} ({keys}) VALUES ({values})')
        self.commit()

        return self.read(collection, str(self.cursor.lastrowid))

    def read(self, collection: str, id: str):
        schema = [row[1] for row in self.execute(f'PRAGMA table_info({collection})')]
        return [dict(zip(schema, row)) for row in
                self.execute(f'SELECT * FROM {collection} WHERE id = ? LIMIT 1', id)][0]

    def update(self, collection: str, id: str, body: dict):
        for key, value in body.items(): self.execute(f'UPDATE {collection} SET {key} = "{value}" WHERE id = ?', id)
        self.commit()
        return self.read(collection, id)

    def delete(self, collection: str, id: str):
        self.execute(f'DELETE FROM {collection} WHERE id = ?', id)
        self.commit()
