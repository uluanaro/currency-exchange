import sqlite3

def init_db():
    connection = sqlite3.connect('database.db')
    connection.execute("PRAGMA foreign_keys = ON")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Currencies (
        ID       INTEGER PRIMARY KEY AUTOINCREMENT,
        Code     VARCHAR(10) UNIQUE NOT NULL,
        FullName VARCHAR(100) NOT NULL,
        Sign     VARCHAR(10) NOT NULL
    );""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS ExchangeRates (
        ID               INTEGER PRIMARY KEY AUTOINCREMENT,
        BaseCurrencyId   INTEGER NOT NULL REFERENCES Currencies(ID),
        TargetCurrencyId INTEGER NOT NULL REFERENCES Currencies(ID),
        Rate             DECIMAL(6) NOT NULL,
        UNIQUE(BaseCurrencyId, TargetCurrencyId)
    );""")
    connection.commit()
    connection.close()

def get_connection():
    connection = sqlite3.connect('database.db')
    connection.execute("PRAGMA foreign_keys = ON")
    return connection