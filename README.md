# Stock Tracker MCP Server

FastMCP server for live stock quotes, multi-broker portfolio tracking, and email alerts. Works with Cursor, Claude Desktop, and other MCP clients.

Supports US equities (e.g. `AAPL`), BIST tickers (e.g. `BIMAS.IS`), and Turkish fund codes (e.g. `TP2`).

## Features

- **Live prices** via Yahoo Finance (equities/ETFs); TEFAS best-effort for Turkish funds
- **Broker-split portfolio** — same symbol can exist under Garanti, Midas, Vakıf, etc.
- **Multi-currency** — TRY and USD positions tracked separately (`by_currency`)
- **Watchlist** add / remove / list
- **Financial metrics** — P/E, P/B, market cap, 52-week range, etc.
- **Email alerts**
  - `breakeven` — losing position recovers to cost
  - `rise` — still in loss but up sharply today
  - `spike` — was near a recent low, then jumped suddenly

Personal holdings stay local: `data/portfolio.json` and `data/watchlist.json` are gitignored. Copy the example templates to start.

## Project layout

```
stockmarket/
├── main.py
├── config.py
├── check_alerts.py              # CLI for email alerts
├── requirements.txt
├── .env.example
├── services/
│   ├── stock_service.py
│   ├── portfolio_service.py
│   ├── alert_service.py
│   └── email_service.py
├── tools/
│   ├── stock_tools.py
│   └── portfolio_tools.py
└── data/
    ├── portfolio.example.json
    ├── watchlist.example.json
    ├── portfolio.json           # local only (gitignored)
    └── watchlist.json           # local only (gitignored)
```

## Setup

```bash
git clone https://github.com/eisenheiim/stockmcp.git
cd stockmcp
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
cp data/portfolio.example.json data/portfolio.json
cp data/watchlist.example.json data/watchlist.json
```

Edit `.env` for SMTP if you want alerts (Gmail app password recommended).

## Run the MCP server

```bash
./venv/bin/python main.py
```

Point Cursor / Claude at this `main.py` (see [CURSOR_VSCODE_SETUP.md](CURSOR_VSCODE_SETUP.md) and [CLAUDE_SETUP.md](CLAUDE_SETUP.md)).

### MCP tools

| Tool | Purpose |
|------|---------|
| `get_stock_summary` | Live price, daily change, volume |
| `get_financial_metrics` | Valuation / company metrics |
| `get_portfolio_status` | Live P&L, allocation, `by_broker`, `by_currency` |
| `add_portfolio_transaction` | Record a buy |
| `manage_watchlist` | `add` / `remove` / `list` |

BIST symbols need the `.IS` suffix (`THYAO.IS`). US symbols do not (`AAPL`, `V`).

## Portfolio format

Positions are a list (broker + symbol), not a flat symbol map:

```json
{
  "positions": [
    {
      "broker": "Midas Menkul Değerler A.Ş.",
      "account": "2308005",
      "symbol": "AAPL",
      "shares": 0.07,
      "average_cost": 309.02,
      "total_cost": 21.81,
      "currency": "USD",
      "asset_type": "stock",
      "name": "Apple Inc."
    }
  ]
}
```

- `average_cost` should be your real buy price; `total_cost` = `shares × average_cost`
- Main portfolio totals are **TRY-only**; USD is under `by_currency`

## Email alerts

```bash
# Mark current losers once (no email)
./venv/bin/python check_alerts.py --seed

# Preview without sending
./venv/bin/python check_alerts.py --dry-run

# Check + send mail if anything triggered
./venv/bin/python check_alerts.py
```

### Alert types

| Type | When |
|------|------|
| `breakeven` | Position was below cost, now at/above cost |
| `rise` | Still below cost, daily move ≥ `ALERT_RISE_PCT` (default 3%) |
| `spike` | Previous close near N-day low, today ≥ `ALERT_SPIKE_PCT` (default 5%) |

### `.env` keys

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=you@gmail.com
SMTP_PASSWORD=your-app-password
ALERT_EMAIL_TO=you@gmail.com
ALERT_MODE=all
ALERT_RISE_PCT=3
ALERT_SPIKE_PCT=5
ALERT_SPIKE_LOOKBACK_DAYS=10
ALERT_NEAR_LOW_PCT=3
```

`ALERT_MODE`: `all` / `both` (breakeven+rise+spike), or a comma list like `rise,spike`.

### Cron (weekdays, market hours)

```cron
*/30 10-18 * * 1-5 cd /path/to/stockmcp && ./venv/bin/python check_alerts.py
```

Install with `crontab -e` (paste the line in the editor; do not put it on the same shell command as `crontab -e`).

## Example prompts

- “What’s the live price of BIMAS.IS?”
- “Show my portfolio P&L by broker”
- “Add NVDA to my watchlist”
- “How is AAPL doing in my Midas account?”

## Privacy

Do **not** commit real `portfolio.json`, `watchlist.json`, `.env`, or `alert_state.json`. Templates and `.env.example` are safe to share.

## License

Use freely for personal portfolio tracking.
