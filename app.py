from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from urls import url_patterns


class MainRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        handler_class = url_patterns.get(path)
        if handler_class:
            handler = handler_class(self)
            handler.handle_post()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Path not found')

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        handler_class = url_patterns.get(path)
        if handler_class:
            handler = handler_class(self)
            handler.handle_get()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Path not found')


def run(server_class=HTTPServer, handler_class=MainRequestHandler, port=8000):
    # database initialization
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()


if __name__ == "__main__":
    run()
