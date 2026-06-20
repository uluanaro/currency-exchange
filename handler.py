from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse

from controllers.currencies_controller import CurrenciesController


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/currencies":
            CurrenciesController(self).get_all()
        elif path.startswith("/currency/"):
            code = path[len("/currency/"):]
            CurrenciesController(self).get_by_code(code)
        else:
            self.send_json(404, {"message": "Маршрут не найден"})

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/currencies":
            CurrenciesController(self).create()

    def send_json(self, status_code, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)