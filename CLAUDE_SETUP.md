# Claude Desktop Integration Guide

## Overview

This guide explains how to configure the Financial & Portfolio Tracker MCP Server with Claude Desktop.

## Prerequisites

- Claude Desktop installed ([download here](https://claude.ai/download))
- Python 3.8+ installed
- The MCP server running on your machine

## Step-by-Step Setup

### 1. Install and Start the Server

```bash
cd /Users/sude/stockmarket

# Option A: Using setup script (recommended)
bash setup.sh
source venv/bin/activate
python main.py

# Option B: Manual setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
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

### 2. Locate Claude Desktop Config File

Open and edit the Claude Desktop configuration file:

**macOS:**
```bash
open ~/Library/Application\ Support/Claude/
```
File: `claude_desktop_config.json`

**Windows:**
File: `%APPDATA%\Claude\claude_desktop_config.json`

**Linux:**
File: `~/.config/Claude/claude_desktop_config.json`

### 3. Add MCP Server Configuration

Add or update the `mcpServers` section in your config:

```json
{
  "mcpServers": {
    "stock-tracker": {
      "command": "python",
      "args": [
        "/Users/sude/stockmarket/main.py"
      ],
      "env": {
        "HOST": "0.0.0.0",
        "PORT": "8000"
      }
    }
  }
}
```

**Important:** Replace `/Users/sude/stockmarket/main.py` with your actual path.

### 4. Complete Config Example

Here's a complete config example with the MCP server:

```json
{
  "mcpServers": {
    "stock-tracker": {
      "command": "python",
      "args": [
        "/Users/sude/stockmarket/main.py"
      ],
      "env": {
        "HOST": "0.0.0.0",
        "PORT": "8000"
      }
    }
  }
}
```

### 5. Restart Claude Desktop

1. **Quit Claude Desktop** completely (Cmd+Q or close from menu)
2. **Reopen Claude Desktop**
3. Wait for it to fully load

### 6. Verify Connection

In Claude Desktop:

1. Open a new conversation
2. Look for a "⚙️" icon in the message input area (indicates MCP connections)
3. Click it to see connected MCP servers - "stock-tracker" should appear

If it doesn't appear:
- Ensure the server is running (`python main.py` in terminal)
- Check the config file path and syntax
- Verify the Python path is correct

## Using with Claude

Once connected, you can ask Claude:

### Stock Queries
- "What's the current price of Apple (AAPL)?"
- "Show me the financial metrics for NVDA"
- "Get the 52-week high and low for THYAO.IS"

### Portfolio Operations
- "What's my current portfolio status?"
- "Add 100 shares of GARAN.IS at 45.50 to my portfolio"
- "Show my portfolio allocation"

### Watchlist Management
- "Add Microsoft to my watchlist"
- "What stocks are in my watchlist?"
- "Remove Google from my watchlist"

### Analysis
- "Compare P/E ratios between Apple and Microsoft"
- "What's my total portfolio P&L?"
- "Which of my positions is performing best?"

## Troubleshooting

### MCP Server doesn't appear in Claude Desktop

**Check 1: Server is running**
```bash
ps aux | grep "python main.py"
```
If not running, start it:
```bash
python main.py
```

**Check 2: Config file is valid JSON**
- Open the config file in VS Code
- Use Cmd+K Cmd+0 (macOS) or Ctrl+K Ctrl+0 (Windows) to format JSON
- Check for syntax errors

**Check 3: Path is correct**
```bash
# Verify the file exists
ls -la /Users/sude/stockmarket/main.py
```

**Check 4: Python is accessible**
```bash
# Check Python path
which python3
python3 --version
```

### Tools are available but return errors

**Common issues:**
1. **"Invalid symbol"** - Stock doesn't exist or uses different ticker (e.g., check Turkish stocks with .IS suffix)
2. **"Network error"** - Check internet connection or yfinance service availability
3. **"File not found"** - Data directory didn't initialize; restart the server

## Advanced Configuration

### Running on Different Port

Edit `.env`:
```env
HOST=0.0.0.0
PORT=8001
```

Update Claude config:
```json
{
  "env": {
    "PORT": "8001"
  }
}
```

### Using Different Python Interpreter

If you have multiple Python versions:

```json
{
  "command": "/Users/sude/stockmarket/venv/bin/python",
  "args": [
    "/Users/sude/stockmarket/main.py"
  ]
}
```

### Cloud Deployment (Render, Heroku)

For deployed servers, use the server URL:

```json
{
  "stock-tracker": {
    "command": "python",
    "args": [
      "/path/to/main.py"
    ],
    "env": {
      "HOST": "0.0.0.0",
      "PORT": "${PORT}"
    }
  }
}
```

## Multiple MCP Servers

You can configure multiple MCP servers:

```json
{
  "mcpServers": {
    "stock-tracker": {
      "command": "python",
      "args": ["/Users/sude/stockmarket/main.py"]
    },
    "other-server": {
      "command": "python",
      "args": ["/path/to/other/server.py"]
    }
  }
}
```

## Performance Tips

1. **Keep server running** - Don't restart between Claude conversations
2. **Cache results** - Claude caches recent queries naturally
3. **Batch requests** - Ask for multiple stocks at once when possible
4. **Monitor port** - Ensure no other services use port 8000

## Debug Mode

For debugging Claude's MCP connection:

**macOS:**
```bash
# View Claude Desktop logs
log stream --predicate 'eventMessage contains "mcp"' --level debug
```

**Windows:**
```bash
# Check Event Viewer > Windows Logs > Application
```

## Getting Help

If you encounter issues:

1. **Check server logs** - Look at terminal where `python main.py` is running
2. **Verify tools work** - Run `python demo.py` to test without Claude
3. **Check Python environment** - Ensure all packages are installed:
   ```bash
   pip list | grep -E "fastmcp|yfinance|pydantic"
   ```

## Additional Resources

- [MCP Documentation](https://modelcontextprotocol.io)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [yfinance Documentation](https://github.com/ranaroussi/yfinance)
- [Claude Desktop Help](https://support.anthropic.com/en/articles/claude-desktop-help)
