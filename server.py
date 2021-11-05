from wsgiref import simple_server, util
from urllib.parse import parse_qsl
import os, mimetypes, json

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
