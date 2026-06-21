from urllib.parse import parse_qs

from dao.exchange_rate_dao import ExchangeRateDAO


class ExchangeRatesController:
    def __init__(self, handler):
        self.handler = handler

    def get_all(self):
        rates = ExchangeRateDAO.get_all()
        result = [rate.to_dict() for rate in rates]
        self.handler.send_json(200, result)

    def get_by_codes(self, pair):
        first_currency = pair[:3]
        second_currency = pair[3:]
        rates = ExchangeRateDAO.get_by_codes(first_currency, second_currency)
        if rates is None:
            self.handler.send_json(404, {"message": "Валюта не найдена"})
        else:
            self.handler.send_json(200, rates.to_dict())

    def create(self):
        content_length = int(self.handler.headers["Content-Length"])
        body = self.handler.rfile.read(content_length).decode("utf-8")
        params = parse_qs(body)
        base_currency_code = params.get("baseCurrencyCode", [None])[0]
        target_currency_code = params.get("targetCurrencyCode", [None])[0]
        rate = params.get("rate", [None])[0]
        if base_currency_code is None or target_currency_code is None or rate is None:
            self.handler.send_json(400, {"message": "Отсутствует нужное поле формы"})
            return
        try:
            exchange_rate = ExchangeRateDAO.create(base_currency_code, target_currency_code, rate)
            self.handler.send_json(201, exchange_rate.to_dict())
        except ValueError:
            self.handler.send_json(409, {"message": "Валюта с таким кодом уже существует"})

    def update(self, pair):
        first_currency = pair[:3]
        second_currency = pair[3:]
        content_length = int(self.handler.headers["Content-Length"])
        body = self.handler.rfile.read(content_length).decode("utf-8")
        params = parse_qs(body)
        rate = params.get("rate", [None])[0]
        if rate is None:
            self.handler.send_json(400, {"message": "Отсутствует нужное поле формы"})
            return
        try:
            exchange_rate = ExchangeRateDAO.update(first_currency, second_currency, rate)
            self.handler.send_json(200, exchange_rate.to_dict())
        except ValueError:
            self.handler.send_json(404, {"message": "Валюта с таким кодом не существует"})




