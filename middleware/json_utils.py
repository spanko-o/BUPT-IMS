import json
from http.server import BaseHTTPRequestHandler
from middleware.exceptions import BadRequestException


class JSONUtils:
    @staticmethod
    def parse_json(handler: BaseHTTPRequestHandler):
        try:
            content_length = int(handler.headers['Content-Length'])
            post_data = handler.rfile.read(content_length)
            return json.loads(post_data)
        except (json.JSONDecodeError, KeyError):
            raise BadRequestException("Invalid JSON data")
