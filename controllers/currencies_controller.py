from urllib.parse import parse_qs

from dao.currency_dao import CurrencyDAO


class CurrenciesController:
    def __init__(self, handler):
        self.handler = handler

    def get_all(self):
        currencies = CurrencyDAO.get_all()
        result = [currency.to_dict() for currency in currencies]
        self.handler.send_json(200, result)

    def get_by_code(self, code):
        currencies = CurrencyDAO.get_by_code(code)
        if currencies is None:
            self.handler.send_json(404, {"message": "Валюта не найдена"})
        else:
            self.handler.send_json(200, currencies.to_dict())

    def create(self):
        content_length = int(self.handler.headers["Content-Length"])
        body = self.handler.rfile.read(content_length).decode("utf-8")
        params = parse_qs(body)
        name = params.get("name", [None])[0]
        code = params.get("code", [None])[0]
        sign = params.get("sign", [None])[0]
        if name is None or code is None or sign is None:
            self.handler.send_json(400, {"message": "Отсутствует нужное поле формы"})
            return
        try:
            currency = CurrencyDAO.create(name, code, sign)
            self.handler.send_json(201, currency.to_dict())
        except ValueError:
            self.handler.send_json(409, {"message": "Валюта с таким кодом уже существует"})
