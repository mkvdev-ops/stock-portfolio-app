from fastapi import FastAPI
from pydantic import BaseModel
from database import get_connection, create_tables
from price_service import get_price

app = FastAPI()

create_tables()

class Holding(BaseModel):
    name: str
    ticker: str
    shares: float
    buy_price: float

class PriceUpdate(BaseModel):
    current_price: float

@app.get("/")
def read_root():
    return {"message": "Portfolio app is running"}

@app.post("/holdings")
def add_holding(holding: Holding):
    invested_value = round(holding.shares * holding.buy_price, 2)

    current_price = get_price(holding.ticker)
    current_value = round(holding.shares * current_price, 2)
    profit_loss = round(current_value - invested_value, 2)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO holdings (
            name, ticker, shares, buy_price, invested_value,
            current_price, current_value, profit_loss
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        holding.name,
        holding.ticker,
        holding.shares,
        holding.buy_price,
        invested_value,
        current_price,
        current_value,
        profit_loss
    ))

    connection.commit()
    new_id = cursor.lastrowid
    connection.close()

    return {
        "id": new_id,
        "name": holding.name,
        "ticker": holding.ticker,
        "shares": holding.shares,
        "buy_price": holding.buy_price,
        "invested_value": invested_value,
        "current_price": current_price,
        "current_value": current_value,
        "profit_loss": profit_loss
    }

@app.get("/holdings")
def get_holdings():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM holdings")
    rows = cursor.fetchall()
    connection.close()

    return [dict(row) for row in rows]

@app.get("/portfolio")
def get_portfolio():
    holdings = get_holdings()
    total_invested = sum(h["invested_value"] for h in holdings)

    return {
        "total_invested": round(total_invested, 2),
        "number_of_holdings": len(holdings)
    }

@app.get("/portfolio/details")
def get_portfolio_details():
    holdings = get_holdings()
    total_invested = sum(h["invested_value"] for h in holdings)

    return {
        "summary": {
            "total_invested": round(total_invested, 2),
            "number_of_holdings": len(holdings)
        },
        "holdings": holdings
    }

@app.put("/holdings/{holding_id}/price")
def update_price(holding_id: int, price_update: PriceUpdate):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM holdings WHERE id = ?", (holding_id,))
    row = cursor.fetchone()

    if row is None:
        connection.close()
        return {"error": "Holding not found"}

    holding = dict(row)

    current_price = price_update.current_price
    current_value = round(holding["shares"] * current_price, 2)
    profit_loss = round(current_value - holding["invested_value"], 2)

    cursor.execute("""
        UPDATE holdings
        SET current_price = ?, current_value = ?, profit_loss = ?
        WHERE id = ?
    """, (current_price, current_value, profit_loss, holding_id))

    connection.commit()
    connection.close()

    return {
        "id": holding_id,
        "current_price": current_price,
        "current_value": current_value,
        "profit_loss": profit_loss
    }