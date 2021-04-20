from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import sys, sqlite3, json


class Database():
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()


    def close(self):
        self.connection.close()


    def tables(self):
        items = []
        for row in self.cursor.execute('SELECT name FROM sqlite_master WHERE type="table" OR type="view"'):
            if row[0][0:7] != 'sqlite_': items.append(row[0])

        return items


    def findall(self, table):
        schema = []
        for row in self.cursor.execute(f'PRAGMA table_info({table})'):
            schema.append(row[1])

        items = []
        for row in self.cursor.execute(f'SELECT * FROM {table}'):
            item = {}
            for i in range(len(row)):
                item[schema[i]] = row[i]

            items.append(item)

        return items


    def findone(self, table, column, value):
        schema = []
        for row in self.cursor.execute(f'PRAGMA table_info({table})'):
            schema.append(row[1])

        for row in self.cursor.execute(f'SELECT * FROM {table} WHERE {column} = ?', value):
            item = {}
            for i in range(len(row)):
                item[schema[i]] = row[i]
            break;

        return item


class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path[:4] != '/api':
            super().do_GET()

        else:
            db = Database()
            data = {}
            path = self.path[4:]
            paths = path.split('/')

            try:
                if path == '' or path == '/':
                    data = db.tables()

                elif len(path.split('/')) == 2:
                    table = paths[1]
                    data = db.findall(table)

                elif len(path.split('/')) == 3:
                    table = paths[1]
                    id = paths[2]
                    data = db.findone(table, 'id', id)

                elif len(path.split('/')) == 4:
                    table = paths[1]
                    column = paths[2]
                    value = paths[3]
                    data = db.findone(table, column, value)

                else:
                    self.send_response(404)
            except:
                self.send_response(404)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())



def start_server(port):
    server = HTTPServer(('', port), RequestHandler)
    print(f'Server started in port {port}')
    server.serve_forever()


def main():
    start_server(8000)


if __name__ == '__main__':
    main()
