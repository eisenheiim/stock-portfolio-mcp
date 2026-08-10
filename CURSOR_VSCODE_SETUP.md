# Cursor & VS Code MCP Setup Guide

## Overview

This guide explains how to use the Financial & Portfolio Tracker MCP Server with **Cursor** or **VS Code** with Claude AI integration.

## Prerequisites

- Cursor or VS Code installed
- Python 3.8+ installed
- The MCP server running on your machine

## Setup Steps

### 1. Install and Start the Server

```bash
cd /Users/sude/stockmarket

# Setup dependencies
bash setup.sh
source venv/bin/activate

# Start the server (keep this terminal open)
python main.py
```

You should see:
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

### 2. Configure Cursor or VS Code

#### For Cursor with Claude Integration

**Option A: Direct Configuration File (Recommended)**

1. Open your cursor settings folder:
   ```bash
   open ~/.cursor/
   ```
   Or directly edit: `~/.cursor/settings.json`

2. Add MCP server configuration:
   ```json
   {
     "extensions.ignoreRecommendations": true,
     "mcp": {
       "stock-tracker": {
         "command": "python",
         "args": ["/Users/sude/stockmarket/main.py"],
         "env": {
           "HOST": "0.0.0.0",
           "PORT": "8000"
         }
       }
     }
   }
   ```

**Option B: Via Cursor Settings UI**

1. Open Cursor
2. Press `Cmd + ,` (Settings)
3. Search for "MCP"
4. Add new MCP server:
   - Name: `stock-tracker`
   - Command: `python`
   - Args: `/Users/sude/stockmarket/main.py`
   - Environment: `HOST=0.0.0.0, PORT=8000`

#### For VS Code with Claude Extension

1. Install the **Claude for VS Code** extension (by Anthropic)
2. Open VS Code settings: `Cmd + ,`
3. Search for "Claude MCP"
4. Add to `claude.mcp.servers`:
   ```json
   {
     "stock-tracker": {
       "command": "python",
       "args": ["/Users/sude/stockmarket/main.py"],
       "env": {
         "HOST": "0.0.0.0",
         "PORT": "8000"
       }
     }
   }
   ```

### 3. Restart Cursor/VS Code

Close and reopen Cursor or VS Code for the MCP connection to load.

### 4. Verify Connection

In Cursor or VS Code:
1. Open the Claude chat panel
2. Look for a settings icon or MCP indicator
3. You should see "stock-tracker" listed as an available MCP server

If not appearing:
- Ensure the server is running (`python main.py`)
- Check that the path `/Users/sude/stockmarket/main.py` is correct
- Restart the editor

## Using with Claude in Cursor/VS Code

### In Chat Messages

Simply ask Claude in the chat:

```
"What's the current price of Apple?"
→ Claude will use: get_stock_summary("AAPL")

"Show my portfolio status and P&L"
→ Claude will use: get_portfolio_status()

"Add 100 shares of GARAN.IS at 45.50 to my portfolio"
→ Claude will use: add_portfolio_transaction("GARAN.IS", 100, 45.50)

"What's in my watchlist?"
→ Claude will use: manage_watchlist("list", "")

"Add NVDA to my watchlist"
→ Claude will use: manage_watchlist("add", "NVDA")
```

### In Code Context

The MCP tools are also available in:
- **Code explanations** - Ask Claude to analyze stock-related code
- **Inline chat** (`Cmd + I` in Cursor)
- **Chat panel** - Open with Claude icon
- **Context menu** - Right-click to ask Claude with selected code

### Example Workflow

1. **Open a Python file** in your project
2. **Use inline chat** (`Cmd + I`):
   ```
   "Help me fetch AAPL stock data and add it to my portfolio"
   ```
3. Claude will:
   - Call `get_stock_summary("AAPL")` to get current price
   - Suggest code to add it to portfolio
   - Optionally call `add_portfolio_transaction()` if authorized

## Available MCP Tools

### Stock Information

**`get_stock_summary(symbol: str)`**
- Returns: Current price, daily change %, volume
- Example: `"What's the price of AAPL?"`

**`get_financial_metrics(symbol: str)`**
- Returns: P/E, P/B, market cap, dividend yield, 52-week range
- Example: `"Show me MSFT's financial metrics"`

### Portfolio Management

**`get_portfolio_status()`**
- Returns: Total portfolio value, P&L, positions, allocation
- Example: `"Show my portfolio status"`

**`add_portfolio_transaction(symbol, shares, buy_price)`**
- Adds stock holdings
- Example: `"Add 50 AAPL at $150 to my portfolio"`

### Watchlist

**`manage_watchlist(action, symbol)`**
- Actions: "add", "remove", "list"
- Example: `"Add TSLA to my watchlist"`

## Troubleshooting

### MCP Server Not Appearing

**Check 1: Is the server running?**
```bash
ps aux | grep "python main.py"
```
If not, start it:
```bash
cd /Users/sude/stockmarket
source venv/bin/activate
python main.py
```

**Check 2: Is the configuration path correct?**
Verify the path exists:
```bash
ls -la /Users/sude/stockmarket/main.py
```

**Check 3: Restart the editor**
- Fully close Cursor/VS Code
- Reopen it
- Wait for Claude extension to load

### Tools Not Responding

**Check 1: Is Claude connected?**
- Look for Claude icon/indicator in the editor
- Verify you're signed in with an Anthropic account

**Check 2: Check server logs**
- Look at the terminal where `python main.py` is running
- Check for error messages

**Check 3: Test manually**
```bash
cd /Users/sude/stockmarket
python demo.py
```

### "Invalid symbol" Error

- Verify the stock symbol is correct
- Turkish BIST stocks end with `.IS` (e.g., `THYAO.IS`, `GARAN.IS`)
- US stocks have no suffix (e.g., `AAPL`, `MSFT`, `NVDA`)

## Advanced Configuration

### Custom Port

Edit `.env`:
```env
HOST=0.0.0.0
PORT=8001
```

Update both the MCP config and `.env` to match.

### Virtual Environment Path

If using a different venv location:
```json
{
  "stock-tracker": {
    "command": "/path/to/your/venv/bin/python",
    "args": ["/Users/sude/stockmarket/main.py"]
  }
}
```

## Multiple MCP Servers

You can add other MCP servers alongside stock-tracker:

```json
{
  "mcp": {
    "stock-tracker": { ... },
    "other-server": { ... }
  }
}
```

## Testing Locally (Without Claude)

Test the tools directly:

```bash
python demo.py
```

This runs tests without needing Cursor/VS Code.

## Tips & Tricks

### Use in Code Comments
```python
# @claude: What's the current price of AAPL?
# → Claude can use MCP tools to answer
```

### Combine with Code
Ask Claude to write code that uses your portfolio data:
```
"Write a Python script that fetches my portfolio and calculates sector allocation"
```

### Monitor Your Portfolio
```
"Monitor my portfolio P&L and alert me if any position loses 5%"
```

### Financial Analysis
```
"Compare the P/E ratios of these 5 stocks I'm watching"
```

## Performance Notes

- Server runs locally on port 8000 - fast response times
- Stock prices fetched from yfinance - subject to rate limits
- JSON data persisted locally - no cloud dependency
- No authentication required for local use

## Next Steps

1. ✅ Start the server: `python main.py`
2. ✅ Configure Cursor/VS Code with MCP settings
3. ✅ Restart the editor
4. ✅ Open Claude chat and ask about stocks!

## Support

- **Setup Issues** → See [GETTING_STARTED.md](GETTING_STARTED.md)
- **API Reference** → Check [README.md](README.md)
- **General Help** → Read [INDEX.md](INDEX.md)
- **Test Setup** → Run `python demo.py`

---

**Ready to use Claude with your stock tracker in Cursor/VS Code!**
