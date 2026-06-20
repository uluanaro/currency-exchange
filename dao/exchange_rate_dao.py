from database import get_connection
from models.currency import Currency
from models.exchange_rate import ExchangeRate


class ExchangeRateDAO:
    @staticmethod
    def get_all():
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""SELECT
                                er.ID,
                                er.Rate,
                                bc.ID, bc.Code, bc.FullName, bc.Sign,
                                tc.ID, tc.Code, tc.FullName, tc.Sign
                            FROM ExchangeRates er
                            JOIN Currencies bc ON er.BaseCurrencyId = bc.ID
                            JOIN Currencies tc ON er.TargetCurrencyId = tc.ID""")
            rows = cursor.fetchall()
            rates = []
            for row in rows:
                id = row[0]
                rate = row[1]
                base_currency = Currency(row[2], row[4], row[3], row[5])
                target_currency = Currency(row[6], row[8], row[7], row[9])
                ex_rate = ExchangeRate(id, base_currency, target_currency, rate)
                rates.append(ex_rate)
            return rates
        finally:
            connection.close()

    @staticmethod
    def get_by_codes(base_code, target_code):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""SELECT
                                    er.ID,
                                    er.Rate,
                                    bc.ID, bc.Code, bc.FullName, bc.Sign,
                                    tc.ID, tc.Code, tc.FullName, tc.Sign
                                FROM ExchangeRates er
                                JOIN Currencies bc ON er.BaseCurrencyId = bc.ID
                                JOIN Currencies tc ON er.TargetCurrencyId = tc.ID
                                WHERE bc.Code = ? AND tc.Code = ?""", (base_code, target_code))
            row = cursor.fetchone()
            if row is None:
                return None
            id = row[0]
            rate = row[1]
            base_currency = Currency(row[2], row[4], row[3], row[5])
            target_currency = Currency(row[6], row[8], row[7], row[9])
            return ExchangeRate(id, base_currency, target_currency, rate)
        finally:
            connection.close()
