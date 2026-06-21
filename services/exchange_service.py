from dao.exchange_rate_dao import ExchangeRateDAO
from decimal import Decimal

class ExchangeService:
    @staticmethod
    def exchange(amount, from_code, to_code):
        exchange_rate = ExchangeRateDAO.get_by_codes(from_code, to_code)
        if exchange_rate is not None:
            final_rate = exchange_rate.rate
            base = exchange_rate.base_currency
            target = exchange_rate.target_currency
        else:
            exchange_rate = ExchangeRateDAO.get_by_codes(to_code, from_code)
            if exchange_rate is not None:
                final_rate = 1 / exchange_rate.rate
                base = exchange_rate.target_currency
                target = exchange_rate.base_currency
            else:
                first_currency = ExchangeRateDAO.get_by_codes("USD", from_code)
                second_currency = ExchangeRateDAO.get_by_codes("USD", to_code)
                if first_currency is None or second_currency is None:
                    raise ValueError("Не удалось найти курс обмена")
                final_rate = second_currency.rate / first_currency.rate
                base = first_currency.target_currency
                target = second_currency.target_currency
        converted = round(Decimal(str(final_rate)) * Decimal(str(amount)), 2)
        return {
                "baseCurrency": base.to_dict(),
                "targetCurrency": target.to_dict(),
                "rate": final_rate,
                "amount": float(amount),
                "convertedAmount": float(converted)
        }

