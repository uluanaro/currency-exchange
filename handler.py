from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse

from controllers.currencies_controller import CurrenciesController
from controllers.exchange_controller import ExchangeController
from controllers.exchange_rates_controller import ExchangeRatesController


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            path = urlparse(self.path).path
            if path == "/currencies":
                CurrenciesController(self).get_all()
            elif path.startswith("/currency/"):
                code = path[len("/currency/"):]
                if not code:
                    self.send_json(400, {"message": "Код валюты отсутствует в адресе"})
                else:
                    CurrenciesController(self).get_by_code(code)
            elif path == "/exchangeRates":
                ExchangeRatesController(self).get_all()
            elif path.startswith("/exchangeRate/"):
                pair = path[len("/exchangeRate/"):]
                if not pair:
                    self.send_json(400, {"message": "Код валюты отсутствует в адресе"})
                else:
                    ExchangeRatesController(self).get_by_codes(pair)
            elif path == "/exchange":
                ExchangeController(self).exchange()
            else:
                self.send_json(404, {"message": "Маршрут не найден"})
        except Exception as e:
            self.send_json(500, {"message": f"Внутренняя ошибка сервера: {str(e)}"})

    def do_POST(self):
        try:
            path = urlparse(self.path).path
            if path == "/currencies":
                CurrenciesController(self).create()
            elif path == "/exchangeRates":
                ExchangeRatesController(self).create()
        except Exception as e:
            self.send_json(500, {"message": f"Внутренняя ошибка сервера: {str(e)}"})

    def send_json(self, status_code, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_PATCH(self):
        try:
            path = urlparse(self.path).path
            if path.startswith("/exchangeRate/"):
                pair = path[len("/exchangeRate/"):]
                ExchangeRatesController(self).update(pair)
            else:
                self.send_json(404, {"message": "Маршрут не найден"})
        except Exception as e:
            self.send_json(500, {"message": f"Внутренняя ошибка сервера: {str(e)}"})