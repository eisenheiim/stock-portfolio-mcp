# Stock Tracker MCP Server

FastMCP server for live stock quotes, multi-broker portfolio tracking, and email alerts. Works with Cursor, Claude Desktop, and other MCP clients.

Supports US equities (`AAPL`), BIST tickers (`BIMAS.IS`), and Turkish fund codes (`TP2`).

## Features

- **Live prices** via Yahoo Finance; TEFAS best-effort for Turkish funds
- **Broker-split portfolio** — same symbol across Garanti, Midas, Vakıf, etc.
- **Multi-currency** — TRY and USD tracked separately (`by_currency`)
- **Watchlist** add / remove / list
- **Financial metrics** — P/E, P/B, market cap, 52-week range
- **Email alerts** — breakeven, rise (while in loss), spike (from recent low)

Personal holdings stay local: `data/portfolio.json` and `data/watchlist.json` are gitignored.

## Project layout

```
stockmcp/
├── main.py                 # MCP server entry (keep path for Cursor config)
├── config.py
├── requirements.txt
├── services/               # business logic
│   ├── stock_service.py
│   ├── portfolio_service.py
│   ├── alert_service.py
│   └── email_service.py
├── scripts/                # CLI utilities
│   ├── check_alerts.py     # email alerts (cron)
│   ├── demo.py             # quick test
│   └── check_dependencies.py
├── docs/
│   └── setup.md            # Cursor / Claude setup
└── data/
    ├── portfolio.example.json
    └── watchlist.example.json
```

Root wrappers (`check_alerts.py`, `demo.py`) exist for backward compatibility; prefer `scripts/`.

## Quick start

```bash
git clone https://github.com/eisenheiim/stockmcp.git
cd stockmcp
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
cp data/portfolio.example.json data/portfolio.json
cp data/watchlist.example.json data/watchlist.json
```

Edit `.env` for SMTP if you want email alerts.

## MCP server

```bash
python main.py
```

Connect in Cursor or Claude — see **[docs/setup.md](docs/setup.md)**.

| Tool | Purpose |
|------|---------|
| `get_stock_summary` | Live price, daily change, volume |
| `get_financial_metrics` | Valuation / company metrics |
| `get_portfolio_status` | Live P&L, `by_broker`, `by_currency` |
| `add_portfolio_transaction` | Record a buy |
| `manage_watchlist` | `add` / `remove` / `list` |

## Portfolio format

```json
{
  "positions": [
    {
      "broker": "Midas Menkul Değerler A.Ş.",
      "symbol": "AAPL",
      "shares": 0.07,
      "average_cost": 309.02,
      "total_cost": 21.81,
      "currency": "USD",
      "asset_type": "stock"
    }
  ]
}
```

`total_cost` = `shares × average_cost`. Main totals are TRY-only; USD under `by_currency`.

## Email alerts

```bash
python scripts/check_alerts.py --seed      # once: mark current losers
python scripts/check_alerts.py --dry-run   # preview
python scripts/check_alerts.py             # check + send mail
```

| Type | When |
|------|------|
| `breakeven` | Was below cost, now at/above cost |
| `rise` | Still in loss, daily move ≥ `ALERT_RISE_PCT` (default 3%) |
| `spike` | Near N-day low, then jumps ≥ `ALERT_SPIKE_PCT` (default 5%) |

US stocks (AAPL, V) are included. Funds are skipped for spike/rise.

### Cron

```cron
*/30 10-18 * * 1-5 cd /path/to/stockmcp && ./venv/bin/python scripts/check_alerts.py
```

## Dev commands

```bash
make demo      # test services
make alerts    # dry-run alert check
make check     # verify install
```

## Privacy

Do **not** commit `.env`, `portfolio.json`, `watchlist.json`, or `alert_state.json`.

## License

Use freely for personal portfolio tracking.
