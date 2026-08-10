# Financial & Portfolio Tracker MCP Server

A powerful Model Context Protocol (MCP) server built with FastMCP that enables AI agents (Claude Desktop, Cursor, etc.) to track stocks across global and Turkish exchanges (BIST), manage investment portfolios, and perform financial analysis.

## Features

✨ **Real-time Stock Tracking**
- Live price data from global exchanges (NASDAQ, NYSE, etc.)
- Turkish BIST exchange support (e.g., THYAO.IS, GARAN.IS)
- 52-week highs/lows and volume data

📊 **Portfolio Management**
- Track multiple stock holdings with average cost basis
- Calculate profit/loss (P&L) at portfolio and position level
- Asset allocation analysis
- Transaction history with timestamps

📋 **Watchlist Management**
- Add/remove stocks from custom watchlist
- Quick access to monitored stocks
- Persistent storage

💰 **Financial Analysis**
- P/E and P/B ratios
- EV/EBITDA multiples
- Dividend yields
- Market cap and sector data
- Earnings per share (EPS)

## Project Structure

```
stockmarket/
├── main.py                 # MCP server entry point
├── config.py               # Configuration & environment variables
├── requirements.txt        # Python dependencies
├── .env.example            # Example environment variables
├── claude_desktop_config.json  # Claude Desktop configuration
├── services/
│   ├── __init__.py
│   ├── stock_service.py    # yfinance integration
│   └── portfolio_service.py # Portfolio & watchlist management
├── tools/
│   ├── __init__.py
│   ├── stock_tools.py      # Stock query tools
│   └── portfolio_tools.py   # Portfolio management tools
└── data/
    ├── portfolio.json      # Holdings and transactions
    └── watchlist.json      # Monitored symbols
```

## Installation

### Prerequisites
- Python 3.8+
- pip or uv package manager

### Setup

1. **Clone or navigate to the project:**
   ```bash
   cd /Users/sude/stockmarket
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env if needed (default values work for local development)
   ```

## Quick Start

### Running the Server

```bash
python main.py
```

Expected output:
```
Starting Financial & Portfolio Tracker MCP Server
Host: 0.0.0.0
Port: 8000

Registered Tools:
  - get_stock_summary
  - get_financial_metrics
  - get_portfolio_status
  - add_portfolio_transaction
  - manage_watchlist

Server running... Press Ctrl+C to stop
```

### Configuring Cursor or VS Code

See [CURSOR_VSCODE_SETUP.md](CURSOR_VSCODE_SETUP.md) for detailed setup instructions.

**Quick steps:**
1. Ensure server is running: `python main.py`
2. Open Cursor or VS Code settings
3. Add MCP server config pointing to `/Users/sude/stockmarket/main.py`
4. Restart the editor

## Available Tools

### Stock Information Tools

#### `get_stock_summary(symbol: str)`
Get current stock price, daily changes, and volume.

**Parameters:**
- `symbol` (str): Stock ticker (e.g., "AAPL", "THYAO.IS", "NVDA")

**Returns:**
```json
{
  "symbol": "AAPL",
  "current_price": 150.25,
  "daily_change": 2.15,
  "daily_change_pct": 1.45,
  "volume": 52000000,
  "previous_close": 148.10,
  "status": "success"
}
```

#### `get_financial_metrics(symbol: str)`
Retrieve detailed financial metrics and valuation ratios.

**Parameters:**
- `symbol` (str): Stock ticker

**Returns:**
```json
{
  "symbol": "AAPL",
  "name": "Apple Inc.",
  "sector": "Technology",
  "industry": "Consumer Electronics",
  "market_cap": 3200000000000,
  "pe_ratio": 28.45,
  "pb_ratio": 48.32,
  "ev_ebitda": 22.15,
  "dividend_yield": 0.42,
  "eps": 5.28,
  "52_week_high": 199.62,
  "52_week_low": 124.17,
  "avg_volume": 48000000,
  "status": "success"
}
```

### Portfolio Management Tools

#### `get_portfolio_status()`
Get comprehensive portfolio overview with valuations and P&L.

**Returns:**
```json
{
  "status": "success",
  "total_cost_basis": 3767.50,
  "total_current_value": 4150.00,
  "total_pnl": 382.50,
  "total_pnl_pct": 10.15,
  "positions": [
    {
      "symbol": "AAPL",
      "shares": 10,
      "average_cost": 150.25,
      "total_cost": 1502.50,
      "current_price": 155.50,
      "current_value": 1555.00,
      "pnl": 52.50,
      "pnl_pct": 3.49
    }
  ],
  "allocation": [
    {
      "symbol": "AAPL",
      "percentage": 37.47,
      "value": 1555.00
    }
  ],
  "last_updated": "2026-08-10T10:00:00"
}
```

#### `add_portfolio_transaction(symbol: str, shares: float, buy_price: float)`
Add a new buy transaction or update existing holdings.

**Parameters:**
- `symbol` (str): Stock ticker
- `shares` (float): Number of shares to purchase
- `buy_price` (float): Purchase price per share

**Returns:**
```json
{
  "status": "success",
  "message": "Added 10 shares of AAPL",
  "symbol": "AAPL",
  "new_shares": 20,
  "average_cost": 150.25,
  "total_cost": 3005.00
}
```

#### `manage_watchlist(action: str, symbol: str = "")`
Manage watchlist with add, remove, or list actions.

**Parameters:**
- `action` (str): "add", "remove", or "list"
- `symbol` (str): Stock ticker (optional for "list")

**Returns:**
```json
{
  "status": "success",
  "message": "Added NVDA to watchlist",
  "watchlist": ["AAPL", "THYAO.IS", "NVDA"],
  "count": 3
}
```

## Data Files

### `data/portfolio.json`
Stores all portfolio holdings and transaction history.

```json
{
  "holdings": {
    "AAPL": {
      "shares": 10,
      "average_cost": 150.25,
      "total_cost": 1502.50,
      "purchase_dates": ["2025-01-15"]
    }
  },
  "last_updated": "2026-08-10T10:00:00"
}
```

### `data/watchlist.json`
Maintains the list of monitored stocks.

```json
{
  "symbols": ["NVDA", "GOOGL", "MSFT", "GARAN.IS"],
  "last_updated": "2026-08-10T10:00:00"
}
```

## Configuration

### Environment Variables

Create a `.env` file or set these environment variables:

```env
# Server host and port
HOST=0.0.0.0
PORT=8000
```

**Cloud Deployment Examples:**

For Render or similar platforms:
```env
HOST=0.0.0.0
PORT=${PORT}  # Render automatically assigns
```

## Usage Examples with Claude

Once configured, you can ask Claude to:

### Stock Analysis
- "What's the current price of AAPL?"
- "Show me the P/E ratio and market cap of NVDA"
- "Get the 52-week high and low for THYAO.IS"

### Portfolio Management
- "What's my current portfolio status and total P&L?"
- "Add 50 shares of GARAN.IS at 1.25 TRY to my portfolio"
- "Show me my asset allocation"

### Watchlist Operations
- "Add MSFT to my watchlist"
- "Show me all stocks in my watchlist"
- "Remove GOOGL from my watchlist"

### Financial Analysis
- "Compare the P/E ratios of AAPL and MSFT"
- "What's the dividend yield on my AAPL holdings?"
- "Analyze my portfolio's sector allocation"

## Error Handling

The server includes robust error handling:

- **Invalid symbols**: Returns error message with "No data found for symbol"
- **Network issues**: Gracefully handles yfinance connection failures
- **Missing data**: Defaults to "N/A" for unavailable metrics
- **File I/O**: Logs errors and maintains data integrity

Example error response:
```json
{
  "symbol": "INVALID",
  "error": "No data found for symbol: INVALID",
  "status": "error"
}
```

## Troubleshooting

### Server won't start
```bash
# Check if port is already in use
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Use a different port
export PORT=8001
python main.py
```

### Claude Desktop can't connect
- Verify the path in `claude_desktop_config.json` is correct
- Ensure the server is running on the configured port
- Restart Claude Desktop after configuration changes

### Stock symbol not found
- Verify the symbol is correct (e.g., THYAO.IS for Turkish stock)
- Check if the exchange uses a different ticker format
- Ensure internet connection is available

### Data file errors
- Check file permissions in the `data/` directory
- Ensure `data/` folder exists (created automatically on first run)
- Delete corrupted JSON files and let them regenerate

## Development

### Adding New Tools

1. Create a new function in `services/` or add to existing service
2. Define tool wrapper in `tools/`
3. Register in `main.py`:
   ```python
   @mcp.tool()
   def my_new_tool(param: str) -> dict:
       """Tool description"""
       return my_service.function(param)
   ```

### Testing Tools Locally

```python
# test.py
from tools import stock_tools, portfolio_tools

# Test stock summary
result = stock_tools.get_stock_summary("AAPL")
print(result)

# Test portfolio status
status = portfolio_tools.get_portfolio_status()
print(status)
```

Run with: `python test.py`

## Performance Considerations

- **API Rate Limiting**: yfinance has reasonable rate limits; avoid excessive requests
- **Caching**: Consider caching stock prices if calling frequently
- **Data Persistence**: JSON files work well for small portfolios; consider database for larger scale
- **Concurrent Requests**: FastMCP handles concurrent requests safely

## Future Enhancements

- [ ] Database backend (PostgreSQL/SQLite) for better scalability
- [ ] Advanced portfolio analytics (Sharpe ratio, correlation analysis)
- [ ] Price alerts and notifications
- [ ] Tax-loss harvesting calculations
- [ ] Multi-currency support
- [ ] Technical indicators and charting
- [ ] Historical performance tracking
- [ ] Integration with broker APIs (Interactive Brokers, etc.)

## License

This project is provided as-is for educational and personal use.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review yfinance documentation: https://github.com/ranaroussi/yfinance
3. Check FastMCP documentation: https://github.com/jlowin/fastmcp

## Disclaimer

This tool is for informational and portfolio tracking purposes only. It should not be considered financial advice. Always consult with a qualified financial advisor before making investment decisions.
