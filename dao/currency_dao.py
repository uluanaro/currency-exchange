import sqlite3

from database import get_connection
from models.currency import Currency

class CurrencyDAO():
    @staticmethod
    def get_all():
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT ID, Code, FullName, Sign FROM Currencies")
            rows = cursor.fetchall()
            currencies = []
            for row in rows:
                currency = Currency(row[0], row[2], row[1], row[3])
                currencies.append(currency)
            return currencies
        finally:
            connection.close()


    @staticmethod
    def get_by_code(code):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT ID, Code, FullName, Sign FROM Currencies WHERE Code = ?", (code,))
            row = cursor.fetchone()
            if row is None:
                return None
            return Currency(row[0], row[2], row[1], row[3])
        finally:
            connection.close()

    @staticmethod
    def create(name, code, sign):
        connection = get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO Currencies (Code, FullName, Sign) VALUES (?, ?, ?)", (code, name, sign))
            connection.commit()
            return Currency(cursor.lastrowid, name, code, sign)
        except sqlite3.IntegrityError:
            raise ValueError(f"Валюта с кодом {code} уже существует")
        finally:
            connection.close()