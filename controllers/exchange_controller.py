from urllib.parse import urlparse, parse_qs
from services.exchange_service import ExchangeService


class ExchangeController:
    def __init__(self, handler):
        self.handler = handler

    def exchange(self):
        parsed = urlparse(self.handler.path)
        params = parse_qs(parsed.query)
        from_code = params.get("from", [None])[0]
        to_code = params.get("to", [None])[0]
        amount = params.get("amount", [None])[0]
        if from_code is None or to_code is None or amount is None:
            self.handler.send_json(400, {"message": "Отсутствует нужное поле формы"})
            return
        try:
            exchange_rate = ExchangeService.exchange(amount, from_code, to_code)
            self.handler.send_json(200, exchange_rate)
        except ValueError:
            self.handler.send_json(404, {"message": "Курс обмена не найден"})
