# Financial & Portfolio Tracker MCP Server
## Complete Project Index

Welcome! This is your complete, production-ready MCP server for tracking stocks and managing investment portfolios with AI assistance via Claude Desktop.

---

## 📖 Start Here

### First Time Setup?
→ **[GETTING_STARTED.md](GETTING_STARTED.md)** - Quick 5-minute setup guide

### Using Cursor or VS Code?
→ **[CURSOR_VSCODE_SETUP.md](CURSOR_VSCODE_SETUP.md)** - Cursor/VS Code MCP configuration

### Want Full Reference?
→ **[README.md](README.md)** - Comprehensive documentation with all tool details

---

## 📁 Project Files

### 🚀 Entry Points
- **[main.py](main.py)** - The MCP server itself (run this: `python main.py`)
- **[demo.py](demo.py)** - Test/demo script (`python demo.py`)
- **[setup.sh](setup.sh)** - Automated setup script (`bash setup.sh`)

### ⚙️ Configuration
- **[config.py](config.py)** - Server configuration and paths
- **[.env.example](.env.example)** - Example environment variables
- **[claude_desktop_config.json](claude_desktop_config.json)** - Claude Desktop config template

### 🔧 Services (Business Logic)
- **[services/stock_service.py](services/stock_service.py)** - yfinance integration for stock data
- **[services/portfolio_service.py](services/portfolio_service.py)** - Portfolio and watchlist management

### 🛠️ Tools (MCP Endpoints)
- **[tools/stock_tools.py](tools/stock_tools.py)** - Stock query tools
- **[tools/portfolio_tools.py](tools/portfolio_tools.py)** - Portfolio management tools

### 📊 Data Storage
- **[data/portfolio.json](data/portfolio.json)** - Your portfolio holdings
- **[data/watchlist.json](data/watchlist.json)** - Your watchlist

### 📦 Dependencies
- **[requirements.txt](requirements.txt)** - Python packages needed
- **[Makefile](Makefile)** - Convenient build commands

### 🧪 Utilities
- **[check_dependencies.py](check_dependencies.py)** - Verify setup is correct

### 📚 Documentation
- **[GETTING_STARTED.md](GETTING_STARTED.md)** ← Start here!
- **[CLAUDE_SETUP.md](CLAUDE_SETUP.md)** - Claude Desktop integration
- **[README.md](README.md)** - Complete user guide
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Technical overview
- **[INDEX.md](INDEX.md)** - This file

---

## 🎯 Quick Reference

### Available Tools (for Claude)

| Tool | Purpose |
|------|---------|
| `get_stock_summary(symbol)` | Get current price, daily change, volume |
| `get_financial_metrics(symbol)` | Get P/E, P/B, market cap, dividend yield |
| `get_portfolio_status()` | Get portfolio value, P&L, allocation |
| `add_portfolio_transaction(symbol, shares, price)` | Add stock to portfolio |
| `manage_watchlist(action, symbol)` | Add/remove/list watchlist stocks |

### Example Prompts for Claude

```
"What's the current price of Apple?"
→ Calls: get_stock_summary("AAPL")

"Show my portfolio status"
→ Calls: get_portfolio_status()

"Add 100 shares of GARAN.IS at 45.50 to my portfolio"
→ Calls: add_portfolio_transaction("GARAN.IS", 100, 45.50)

"Add Tesla to my watchlist"
→ Calls: manage_watchlist("add", "TSLA")
```

---

## ✅ Setup Checklist

- [ ] Run `bash setup.sh`
- [ ] Run `python main.py` (keep terminal open)
- [ ] Edit Claude config file with server path
- [ ] Restart Claude Desktop
- [ ] Run `python demo.py` to verify tools work
- [ ] Ask Claude about stocks!

---

## 🔗 Quick Links

### For Setup
| Document | Purpose |
|----------|---------|
| [GETTING_STARTED.md](GETTING_STARTED.md) | 5-minute quick start |
| [CLAUDE_SETUP.md](CLAUDE_SETUP.md) | Detailed Claude config |
| [setup.sh](setup.sh) | Automated installation |

### For Reference
| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Complete API reference |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Architecture overview |
| [Makefile](Makefile) | Build commands |

### For Testing
| Script | Purpose |
|--------|---------|
| [demo.py](demo.py) | Test all tools interactively |
| [check_dependencies.py](check_dependencies.py) | Verify installation |

---

## 📋 File Organization

```
/Users/sude/stockmarket/
│
├── 📚 Documentation (Start with these!)
│   ├── INDEX.md                      ← You are here
│   ├── GETTING_STARTED.md            ← Quick start (5 min)
│   ├── CLAUDE_SETUP.md               ← Claude Desktop setup
│   ├── README.md                     ← Full reference
│   └── PROJECT_SUMMARY.md            ← Technical overview
│
├── 🚀 Server & Execution
│   ├── main.py                       ← Run this: python main.py
│   ├── config.py                     ← Configuration
│   ├── setup.sh                      ← Setup automation
│   ├── Makefile                      ← Build commands
│   └── check_dependencies.py         ← Verify setup
│
├── 🧪 Testing
│   └── demo.py                       ← Test script: python demo.py
│
├── 🛠️ Business Logic
│   └── services/
│       ├── stock_service.py          ← Stock data fetching
│       └── portfolio_service.py      ← Portfolio management
│
├── 📡 MCP Tools
│   └── tools/
│       ├── stock_tools.py            ← Stock query endpoints
│       └── portfolio_tools.py        ← Portfolio endpoints
│
├── 💾 Data Storage
│   └── data/
│       ├── portfolio.json            ← Your holdings
│       └── watchlist.json            ← Your watchlist
│
└── ⚙️ Configuration
    ├── requirements.txt              ← Python dependencies
    ├── .env.example                  ← Environment template
    ├── claude_desktop_config.json    ← Claude config template
    ├── .gitignore                    ← Git ignore rules
    └── __init__.py                   ← Package marker
```

---

## 🎓 How to Use This Project

### For First-Time Users
1. Read [GETTING_STARTED.md](GETTING_STARTED.md) (5 minutes)
2. Run `bash setup.sh`
3. Run `python demo.py`
4. Follow [CLAUDE_SETUP.md](CLAUDE_SETUP.md) to configure Claude
5. Start asking Claude about stocks!

### For Developers
1. Review [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for architecture
2. Check [services/](services/) and [tools/](tools/) source code
3. Run `python demo.py` to understand tool behavior
4. Modify and extend as needed

### For Reference
1. Check [README.md](README.md) for complete API documentation
2. See [Makefile](Makefile) for available commands
3. Use `python check_dependencies.py` to verify setup

---

## 🚀 Quick Commands

```bash
# Setup
bash setup.sh
source venv/bin/activate

# Run
python main.py                  # Start server
python demo.py                  # Test tools
python check_dependencies.py    # Verify setup

# Build
make setup                       # Full setup
make run                         # Run server
make demo                        # Run demo
make clean                       # Cleanup
make help                        # Show all commands
```

---

## 📞 Troubleshooting

**Problem:** "Tool not found" in Claude  
**Solution:** Server running? Claude restarted? See [CLAUDE_SETUP.md](CLAUDE_SETUP.md)

**Problem:** Setup fails  
**Solution:** Run `python check_dependencies.py` to diagnose. See [GETTING_STARTED.md](GETTING_STARTED.md)

**Problem:** Stock symbol not found  
**Solution:** Check ticker format (BIST stocks end with `.IS`). See [README.md](README.md)

**Problem:** Module import errors  
**Solution:** Run `bash setup.sh` again. See [GETTING_STARTED.md](GETTING_STARTED.md)

---

## ✨ Key Features

- ✅ Real-time stock prices from global & BIST exchanges
- ✅ Portfolio tracking with average cost calculation
- ✅ P&L calculations at position & portfolio level
- ✅ Asset allocation analysis
- ✅ Watchlist management
- ✅ Financial metrics (P/E, P/B, dividend yield, etc.)
- ✅ Persistent JSON storage
- ✅ Error-resistant with clear messages
- ✅ Type-hinted, documented code
- ✅ Production-ready architecture

---

## 📦 What's Included

- **Complete source code** with comprehensive documentation
- **All dependencies** listed in requirements.txt
- **Automated setup** with bash script
- **Test/demo script** for verification
- **Sample data** files (portfolio.json, watchlist.json)
- **Configuration templates** for Claude Desktop
- **Full documentation** (4 guides + API reference)

---

## 🎉 Ready to Go!

You have everything needed to:
1. ✅ Track stocks in real-time
2. ✅ Manage your investment portfolio
3. ✅ Analyze financial metrics
4. ✅ Use AI assistance via Claude Desktop

**Next Step:** Open [GETTING_STARTED.md](GETTING_STARTED.md) and follow the 5-minute setup!

---

## 📝 Document Quick Links

| Need | Document |
|------|----------|
| Quick start | [GETTING_STARTED.md](GETTING_STARTED.md) |
| Claude config | [CLAUDE_SETUP.md](CLAUDE_SETUP.md) |
| Full reference | [README.md](README.md) |
| Tech details | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) |
| This guide | [INDEX.md](INDEX.md) |

---

**Version:** 1.0.0  
**Created:** August 10, 2026  
**Python:** 3.8+  
**Status:** ✅ Production Ready
