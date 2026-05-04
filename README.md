📊 Stock Portfolio App

A backend API for tracking stock and ETF portfolios, built with FastAPI and SQLite.

## 🚀 Features

- Add and manage holdings
- Automatic calculation of:
  - Invested value
  - Current value
  - Profit / Loss
- Portfolio summary (total invested, number of holdings)
- Price service layer (ready for real market data integration)

## 🧱 Tech Stack

- Python
- FastAPI
- SQLite
- Git / GitHub

## 📦 Project Structure


stock-portfolio-app/
├── main.py
├── database.py
├── price_service.py
├── README.md


## ▶️ Run the app

```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8010

Open in browser:

http://127.0.0.1:8010/docs
📡 API Endpoints
Add holding
POST /holdings
Get holdings
GET /holdings
Update price
PUT /holdings/{holding_id}/price
Portfolio summary
GET /portfolio
Portfolio details
GET /portfolio/details
🔧 Example Request
{
  "name": "Apple",
  "ticker": "AAPL",
  "shares": 5,
  "buy_price": 180
}
🧠 Future Improvements
Live price integration (Inderes MCP)
Frontend UI
Portfolio allocation charts
Authentication
📌 Status

🚧 In development

Built as a learning project for portfolio management and backend development.


---

## 👉 Then run

```powershell
git add README.md
git commit -m "Add README"
git push