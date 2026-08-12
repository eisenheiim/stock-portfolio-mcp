# Cursor & Claude MCP Setup

Connect the stock tracker MCP server to Cursor or Claude Desktop.

## Prerequisites

- Python 3.8+
- Project cloned and dependencies installed (`pip install -r requirements.txt`)
- Virtualenv recommended: `python -m venv venv && source venv/bin/activate`

## MCP server config

Use the **full path** to your venv Python and `main.py`:

```json
{
  "mcpServers": {
    "stock-tracker": {
      "command": "/path/to/stockmcp/venv/bin/python",
      "args": ["/path/to/stockmcp/main.py"],
      "env": {
        "HOST": "0.0.0.0",
        "PORT": "8000"
      }
    }
  }
}
```

Replace `/path/to/stockmcp` with your actual clone path.

## Cursor

1. Open Cursor MCP settings (or edit your MCP config JSON).
2. Add the `stock-tracker` entry above.
3. Restart Cursor.
4. Confirm `stock-tracker` appears under MCP servers.

If you see `spawn python ENOENT`, use the full venv Python path instead of `python`.

## Claude Desktop

**macOS config file:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

Add the same `mcpServers` block. Restart Claude Desktop.

See also: [docs/claude_desktop_config.example.json](claude_desktop_config.example.json)

## Verify

```bash
# From project root
python scripts/demo.py          # test services without MCP client
python main.py                  # start server (stdio — for debugging)
python scripts/check_alerts.py --dry-run   # test email alerts
python scripts/check_dependencies.py       # verify install
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| MCP not listed | Restart editor; check Python path in config |
| No portfolio data | Copy `data/portfolio.example.json` → `data/portfolio.json` |
| Email not sending | Set SMTP vars in `.env`; use Gmail app password |
| BIST symbol fails | Use `.IS` suffix: `BIMAS.IS` not `BIMAS` |

More detail in the main [README](../README.md).
