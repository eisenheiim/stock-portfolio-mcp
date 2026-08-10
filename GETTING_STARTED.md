# Getting Started Guide

## 🎯 What You Have

A complete, production-ready **Financial & Portfolio Tracker MCP Server** that lets Claude AI (in Claude Desktop, Cursor, etc.) help you track stocks and manage your investment portfolio.

## ⚡ Quick Start (5 minutes)

### 1. Install Everything
```bash
cd /Users/sude/stockmarket
bash setup.sh
```

This will:
- ✅ Create a Python virtual environment
- ✅ Install all dependencies
- ✅ Set up the `.env` file
- ✅ Create the data directory

### 2. Run the Server
```bash
source venv/bin/activate
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

**Leave this terminal running.** The server stays active.

### 3. Configure Cursor or VS Code

See [CURSOR_VSCODE_SETUP.md](CURSOR_VSCODE_SETUP.md) for detailed setup instructions.

**Quick setup:**
1. Open Cursor or VS Code settings
2. Add MCP server configuration with path: `/Users/sude/stockmarket/main.py`
3. Restart the editor
4. Done! ✅

---

## 📚 Documentation Overview

### For Setup
- **[CLAUDE_SETUP.md](CLAUDE_SETUP.md)** - Detailed Claude Desktop configuration
- **[setup.sh](setup.sh)** - Automated setup script
- **[check_dependencies.py](check_dependencies.py)** - Verify everything is installed

### For Reference
- **[README.md](README.md)** - Complete user guide and API reference
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project structure and features

### For Testing
- **[demo.py](demo.py)** - Interactive test script to verify tools work

---

## 🧪 Verify Setup Works

### Option 1: Run the Demo
```bash
python demo.py
```

This tests:
- ✅ Stock price fetching (AAPL, THYAO.IS)
- ✅ Financial metrics retrieval
- ✅ Portfolio status calculation
- ✅ Watchlist management

### Option 2: Check Dependencies
```bash
python check_dependencies.py
```

### Option 3: Test with Python
```python
from tools import stock_tools

# Test getting a stock price
result = stock_tools.get_stock_summary("AAPL")
print(result)
```

---

## 🔧 Common Tasks

### Change Server Port
Edit `.env`:
```env
HOST=0.0.0.0
PORT=8001
```

Update Claude config to match, then restart.

### Add Initial Stocks to Portfolio
Edit `data/portfolio.json`:
```json
{
  "holdings": {
    "AAPL": {
      "shares": 100,
      "average_cost": 150.00,
      "total_cost": 15000.00,
      "purchase_dates": ["2025-01-01"]
    }
  }
}
```

### View Your Watchlist
Ask Claude: "What's in my watchlist?"

Or edit `data/watchlist.json` directly.

---

## 📱 Using with Claude

### Stock Queries
```
"What's the P/E ratio of Tesla?"
"Show me 52-week high and low for NVDA"
"Compare Apple and Microsoft prices"
```

### Portfolio Management
```
"What's my current portfolio value?"
"Add 50 shares of GARAN.IS at 45.30"
"Calculate my asset allocation"
```

### Watchlist Operations
```
"Add Bitcoin to my watchlist"
"Remove MSFT from my watchlist"
"List all stocks in my watchlist"
```

### Analysis
```
"Which of my positions is performing best?"
"What's my total P&L?"
"Which stocks in my portfolio have the highest P/E?"
```

---

## ❓ Troubleshooting

### "Tool not found" in Claude
1. ✅ Is the server running? Check terminal with `python main.py`
2. ✅ Did you restart Claude Desktop after config change?
3. ✅ Is the config file path correct?

**Fix:** Restart the server, restart Claude Desktop

### "Invalid symbol" error
- Check the symbol is correct
- BIST (Turkish) stocks end with `.IS` (e.g., `THYAO.IS`, `GARAN.IS`)
- US stocks don't have suffix (e.g., `AAPL`, `NVDA`, `MSFT`)

### Server won't start
```bash
# Check if port 8000 is already in use
lsof -i :8000

# If it is, use a different port in .env
# Or kill the existing process
```

### "Network error" from stock tools
- Check your internet connection
- yfinance might be rate-limited; wait a moment and try again

---

## 🎓 Project Structure

```
stockmarket/
├── main.py              ← Start here (the server)
├── config.py            ← Settings
├── demo.py              ← Test tools
├── check_dependencies.py ← Verify setup
│
├── services/            ← Business logic
│   ├── stock_service.py
│   └── portfolio_service.py
│
├── tools/               ← What Claude can call
│   ├── stock_tools.py
│   └── portfolio_tools.py
│
└── data/                ← Your data
    ├── portfolio.json
    └── watchlist.json
```

---

## 📋 Checklist for First Use

- [ ] Run `bash setup.sh`
- [ ] Run `python main.py` (leave it running)
- [ ] Configure Claude Desktop config file
- [ ] Restart Claude Desktop
- [ ] Test with `python demo.py` in a new terminal
- [ ] Ask Claude a question about stocks
- [ ] Add a stock to your portfolio
- [ ] Check your portfolio status

---

## 🚀 What's Next?

### Try These Examples

1. **Check a Stock:**
   ```
   "What's the current price of AAPL and what's the daily change?"
   ```

2. **Add to Portfolio:**
   ```
   "Add 10 shares of Microsoft at $380 per share to my portfolio"
   ```

3. **View Status:**
   ```
   "Show me my complete portfolio status with P&L"
   ```

4. **Manage Watchlist:**
   ```
   "Add Google and Amazon to my watchlist"
   ```

5. **Financial Analysis:**
   ```
   "Compare the P/E ratios of Apple, Microsoft, and Google"
   ```

---

## 🆘 Need Help?

1. **Setup Issues** → Read [CLAUDE_SETUP.md](CLAUDE_SETUP.md)
2. **Tool Reference** → Check [README.md](README.md)
3. **Technical Details** → See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
4. **Test Manually** → Run `python demo.py`

---

## ✨ Key Features

✅ Real-time stock prices from global and Turkish exchanges  
✅ Portfolio tracking with average cost calculation  
✅ Profit/loss calculations at position and portfolio level  
✅ Asset allocation analysis  
✅ Watchlist management  
✅ Financial metrics (P/E, P/B, market cap, etc.)  
✅ Persistent storage via JSON files  
✅ Error-resistant with clear error messages  

---

## 🎉 You're All Set!

Your MCP server is ready. Start using it with Claude Desktop and enjoy AI-powered stock and portfolio tracking!

**Questions?** Check the relevant documentation file or run the demo script.
