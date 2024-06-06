import json
from http.server import BaseHTTPRequestHandler
from middleware.exceptions import APIException


class ResponseUtils:
    @staticmethod
    def send_response(handler: BaseHTTPRequestHandler, status_code: int, response_data: dict):
        handler.send_response(status_code)
        handler.send_header('Content-Type', 'application/json')
        handler.end_headers()
        handler.wfile.write(json.dumps(response_data).encode())

    @staticmethod
    def ok(handler: BaseHTTPRequestHandler, response_data: dict):
        response_data.setdefault('success', True)
        response_data.setdefault('home', 'OK')
        ResponseUtils.send_response(handler, 200, response_data)

    @staticmethod
    def send_error(handler: BaseHTTPRequestHandler, exception: APIException):
        response_data = {'success': False, 'home': exception.detail}
        ResponseUtils.send_response(handler, exception.status_code, response_data)
