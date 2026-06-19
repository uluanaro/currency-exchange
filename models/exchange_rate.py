from models.currency import Currency


class ExchangeRate():
    def __init__(self, id, base_currency, target_currency, rate):
        self.id = id
        self.base_currency = base_currency
        self.target_currency = target_currency
        self.rate = rate

    def to_dict(self):
        return {
            "id": self.id,
            "baseCurrency": self.base_currency.to_dict(),
            "targetCurrency": self.target_currency.to_dict(),
            "rate": self.rate
            }