def get_price(ticker: str) -> float:
    mock_prices = {
        "MSFT": 350,
        "AAPL": 190,
        "IWDA": 80,
        "IS3N": 46
    }

    return mock_prices.get(ticker, 100)