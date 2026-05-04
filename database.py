import sqlite3

DB_NAME = "portfolio.db"

def get_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection

def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS holdings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            ticker TEXT NOT NULL,
            shares REAL NOT NULL,
            buy_price REAL NOT NULL,
            invested_value REAL NOT NULL,
            current_price REAL,
            current_value REAL,
            profit_loss REAL
        )
    """)

    for column in ["current_price", "current_value", "profit_loss"]:
        try:
            cursor.execute(f"ALTER TABLE holdings ADD COLUMN {column} REAL")
        except sqlite3.OperationalError:
            pass

    connection.commit()
    connection.close()