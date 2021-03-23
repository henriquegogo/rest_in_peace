from http.server import HTTPServer, BaseHTTPRequestHandler
import sqlite3, json


class Database():
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()


    def create(self):
        self.cursor.execute('CREATE TABLE clientes (nome text, endereco text)')
        self.connection.commit()


    def seed(self):
        self.cursor.execute('INSERT INTO clientes VALUES(?, ?)', ('Henrique', 'Av Herois do Acre'))
        self.cursor.execute('INSERT INTO clientes VALUES(?, ?)', ('Daiane', 'Av Herois do Acre'))
        self.connection.commit()


    def close(self):
        self.connection.close()


    def tables(self):
        tables = []
        for row in self.cursor.execute('SELECT name FROM sqlite_master WHERE type="table"'):
            tables.append(row[0])

        return tables

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


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        db = Database()
        data = {}

        if self.path == '/':
            data = db.tables()

        elif len(self.path.split('/')) == 2:
            table = self.path[1:]
            data = db.findall(table)

        else:
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
    #db = Database()
    #db.seed()
    #db.close()
    start_server(8000)


if __name__ == '__main__':
    main()
