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

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)
