import json
from http.server import BaseHTTPRequestHandler
from middleware.exceptions import APIException


class ResponseUtils:
    @staticmethod
    def _set_cors_headers(handler: BaseHTTPRequestHandler):
        handler.send_header("Access-Control-Allow-Origin", "http://localhost:3000")
        handler.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        handler.send_header("Access-Control-Allow-Headers", "x-api-key, Content-Type")
        handler.send_header("Access-Control-Allow-Credentials", "true")
        handler.send_header("Access-Control-Max-Age", "3600")

    @staticmethod
    def send_response(handler: BaseHTTPRequestHandler, status_code: int, response_data: dict):
        handler.send_response(status_code)
        ResponseUtils._set_cors_headers(handler)  # 设置CORS头信息
        handler.send_header('Content-Type', 'application/json')
        handler.end_headers()
        handler.wfile.write(json.dumps(response_data).encode())

    @staticmethod
    def ok(handler: BaseHTTPRequestHandler, response_data: dict):
        response_data.setdefault('success', True)
        response_data.setdefault('message', 'OK')
        ResponseUtils.send_response(handler, 200, response_data)

    @staticmethod
    def send_error(handler: BaseHTTPRequestHandler, exception: APIException):
        response_data = {'success': False, 'message': exception.detail}
        ResponseUtils.send_response(handler, exception.status_code, response_data)
