import sqlite3

from database import get_connection
from models.currency import Currency
from models.exchange_rate import ExchangeRate
from dao.currency_dao import CurrencyDAO


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

    @staticmethod
    def create(base_currency_code, target_currency_code, rate):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            base_currency = CurrencyDAO.get_by_code(base_currency_code)
            if base_currency is None:
                raise ValueError("Базовая валюта не найдена")
            target_currency = CurrencyDAO.get_by_code(target_currency_code)
            if target_currency is None:
                raise ValueError("Целевая валюта не найдена")
            cursor.execute("""INSERT INTO ExchangeRates (BaseCurrencyId, TargetCurrencyId, Rate) VALUES (?, ?, ?)""", (base_currency.id, target_currency.id, rate))
            connection.commit()
            return ExchangeRateDAO.get_by_codes(base_currency_code, target_currency_code)
        except sqlite3.IntegrityError:
            raise ValueError("Такая валютная пара уже существует")
        finally:
            connection.close()

    @staticmethod
    def update(base_currency_code, target_currency_code, rate):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            base_currency = CurrencyDAO.get_by_code(base_currency_code)
            if base_currency is None:
                raise ValueError("Базовая валюта не найдена")
            target_currency = CurrencyDAO.get_by_code(target_currency_code)
            if target_currency is None:
                raise ValueError("Целевая валюта не найдена")
            cursor.execute("UPDATE ExchangeRates SET Rate = ? WHERE BaseCurrencyId = ? AND TargetCurrencyId = ?", (rate, base_currency.id, target_currency.id))
            connection.commit()
            rows_affected = cursor.rowcount
            if rows_affected == 0:
                raise ValueError("Валютная пара не найдена")
            return ExchangeRateDAO.get_by_codes(base_currency_code, target_currency_code)
        finally:
            connection.close()
