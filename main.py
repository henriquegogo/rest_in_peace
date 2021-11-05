from wsgiref import simple_server, util
from urllib.parse import parse_qsl
import os, mimetypes, sqlite3, json

class Server:
    host: str
    port: int
    routes = []

    def __init__(self, host: str = '', port: int = 8000):
        self.host = host
        self.port = port

    def post(self, route: str):
        def wrapper(func): self.routes.append(('POST', route, func))
        return wrapper

    def get(self, route: str):
        def wrapper(func): self.routes.append(('GET', route, func))
        return wrapper

    def put(self, route: str):
        def wrapper(func): self.routes.append(('PUT', route, func))
        return wrapper

    def delete(self, route: str):
        def wrapper(func): self.routes.append(('DELETE', route, func))
        return wrapper

    def run(self):
        def serve_static(env, res):
            static_folder = 'public' + env['PATH_INFO']

            if '.' in static_folder and os.path.exists(static_folder):
                res('200 OK', [('Content-Type', mimetypes.guess_type(static_folder)[0])])
                return util.FileWrapper(open(static_folder, "rb"))
            else:
                res('404 Not Found', [('Content-Type', 'text/plain')])
                return ''

        def server(env, res):
            path_items = [item for item in env['PATH_INFO'].split('/')[1:] if item]

            for method, route, func in self.routes:
                route_items = [item for item in route.split('/')[1:] if item]

                if method == env['REQUEST_METHOD'] and len(path_items) == len(route_items):
                    params = [path_items[i] for i, item in enumerate(route_items) if item[0] == '{']
                    post_data = [
                        json.loads(env['wsgi.input'].read(int(env['CONTENT_LENGTH'])).decode())
                    ] if env['CONTENT_LENGTH'] else []
                    query_string = [dict(parse_qsl(env['QUERY_STRING']))] if env['QUERY_STRING'] else []

                    try:
                        res_body = json.dumps(func(*params, *post_data, *query_string))
                        res('200 OK', [('Content-type', 'application/json; charset=utf-8')])
                        return [res_body.encode()]
                    except: pass

            return serve_static(env, res)

        with simple_server.make_server(self.host, self.port, server) as httpd:
            print(f'INFO: Application running on {self.host}:{self.port} (Press CTRL+C to quit)')
            httpd.serve_forever()

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

    def list(self, collection: str):
        schema = [row[1] for row in self.execute(f'PRAGMA table_info({collection})')]
        return [dict(zip(schema, row)) for row in self.execute(f'SELECT * FROM {collection}')]

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

app = Server()

@app.get('/')
def schema():
    return Database().schema()

@app.get('/{collection}')
def list(collection: str):
    return Database().list(collection)

@app.post('/{collection}')
def create(collection: str, body: dict):
    return Database().create(collection, body)

@app.get('/{collection}/{id}')
def read(collection: str, id: str):
    return Database().read(collection, id)

@app.put('/{collection}/{id}')
def update(collection: str, id: str, body: dict):
    return Database().update(collection, id, body)

@app.delete('/{collection}/{id}')
def delete(collection: str, id: str):
    Database().delete(collection, id)

if __name__ == '__main__':
    app.run()
