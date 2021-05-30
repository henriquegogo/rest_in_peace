from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import sys, sqlite3, json


class Database():
    def __init__(self):
        self.connection = sqlite3.connect(sys.argv[1] or 'database.db')
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

        for row in self.execute(f'SELECT * FROM {table} WHERE id = ?', id):
            item = {}
            for i in range(len(row)):
                item[schema[i]] = row[i]
            break;

        return item


class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path[:4] != '/api':
            return super().do_GET()

        db = Database()
        data = {}
        path_split = self.path.split('?')
        path = path_split[0][4:]
        where = path_split[1].replace('&', ' AND ') if len(path_split) > 1 else 'TRUE'
        paths = path.split('/')

        try:
            if path == '' or path == '/':
                data = db.tables()

            elif len(path.split('/')) == 2:
                table = paths[1]
                data = db.findall(table, where)

            elif len(path.split('/')) == 3:
                table = paths[1]
                id = paths[2]
                data = db.findone(table, id)

            else:
                self.send_response(404)
        except:
            self.send_response(404)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())


    def do_POST(self):
        db = Database()
        path_split = self.path.split('?')
        path = path_split[0][4:]
        where = path_split[1].replace('&', ' AND ') if len(path_split) > 1 else 'TRUE'
        paths = path.split('/')

        self.send_response(200)


def start_server(port):
    server = HTTPServer(('', port), RequestHandler)
    print(f'Server started in port {port}')
    server.serve_forever()


def main():
    start_server(int(sys.argv[2]) if len(sys.argv) > 2 else 8000)


if __name__ == '__main__':
    main()
