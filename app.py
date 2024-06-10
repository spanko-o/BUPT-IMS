from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from urls import url_patterns
from database.models import initialize_database
from applications.Admin.utils.visualization import ksh_analysis

class MainRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self._handle_request()

    def do_GET(self):
        self._handle_request()

    def _handle_request(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        query_params = parse_qs(parsed_path.query) if parsed_path else {}
        headers = {key: self.headers[key] for key in self.headers}

        handler_class = url_patterns.get(path)
        if handler_class:
            handler = handler_class(self, query_params, headers)
            handler.handle_request()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Path not found')


def run(server_class=HTTPServer, handler_class=MainRequestHandler, port=8000):
    initialize_database()
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()


if __name__ == "__main__":
    run()
