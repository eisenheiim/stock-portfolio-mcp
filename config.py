"""
Configuration module for Financial & Portfolio Tracker MCP Server.
Handles environment variables and server settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# Data Paths
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PORTFOLIO_FILE = os.path.join(DATA_DIR, "portfolio.json")
WATCHLIST_FILE = os.path.join(DATA_DIR, "watchlist.json")
ALERT_STATE_FILE = os.path.join(DATA_DIR, "alert_state.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Email alert settings (optional)
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() in {"1", "true", "yes"}
ALERT_EMAIL_FROM = os.getenv("ALERT_EMAIL_FROM", "")
ALERT_EMAIL_TO = os.getenv("ALERT_EMAIL_TO", "")
# both | breakeven | rise
ALERT_MODE = os.getenv("ALERT_MODE", "both")
# Daily rise % while still below average cost
ALERT_RISE_PCT = float(os.getenv("ALERT_RISE_PCT", "3"))
