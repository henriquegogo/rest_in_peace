from wsgiref import simple_server, util
from urllib.parse import parse_qsl
import os, mimetypes, json

class Server:
    host: str
    port: int
    routes = []

    def __init__(self, port: int = 8000):
        self.host = ''
        self.port = port

    def post(self, route: str):
        return lambda func: self.routes.append(('POST', route, func))

    def get(self, route: str):
        return lambda func: self.routes.append(('GET', route, func))

    def put(self, route: str):
        return lambda func: self.routes.append(('PUT', route, func))

    def delete(self, route: str):
        return lambda func: self.routes.append(('DELETE', route, func))

    def run(self):
        def serve_static(env, res):
            static_folder = 'public' + ('/index.html' if env['PATH_INFO'] == '/' else env['PATH_INFO'])

            if '.' in static_folder and os.path.exists(static_folder):
                res('200 OK', [('Content-Type', mimetypes.guess_type(static_folder)[0])])
                return util.FileWrapper(open(static_folder, "rb"))
            elif env['PATH_INFO'] == '/':
                res('302 Found', [('Location', '/schema.json')])
                return ''
            else:
                res('404 Not Found', [])
                return ''

        def server(env, res):
            path_items = [item for item in env['PATH_INFO'].split('/')[1:] if item]

            for method, route, func in self.routes:
                route_items = [item for item in route.split('/')[1:] if item]

                if method == env['REQUEST_METHOD'] and len(path_items) == len(route_items) and all(
                        [path_items[i] == item or item[0] == '{' for i, item in enumerate(route_items)]):
                    params = [path_items[i] for i, item in enumerate(route_items) if item[0] == '{']
                    data = dict(parse_qsl(env['QUERY_STRING'])) if env['QUERY_STRING'] else {}

                    if env['CONTENT_LENGTH']:
                        body_data = env['wsgi.input'].read(int(env['CONTENT_LENGTH'])).decode()
                        data.update(json.loads(body_data) if env['CONTENT_TYPE'] == 'application/json'
                                    else dict(parse_qsl(body_data)))

                    try:
                        res_body = json.dumps(func(*params, data) if bool(data) else func(*params))
                        res_code = '201 Created' if method == 'POST' else \
                            '204 No Content' if method == 'DELETE' else \
                            '200 OK'
                        res(res_code, [('Content-type', 'application/json; charset=utf-8')])
                        return [res_body.encode()]
                    except: pass

            if env['REQUEST_METHOD'] != 'GET':
                res('400 Bad Request', [])
                return ''
            else:
                return serve_static(env, res)

        with simple_server.make_server(self.host, self.port, server) as httpd:
            print(f'INFO: Application running on {self.host}:{self.port} (Press CTRL+C to quit)')
            httpd.serve_forever()
