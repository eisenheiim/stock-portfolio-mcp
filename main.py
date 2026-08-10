#!/usr/bin/env python3
"""
Financial & Portfolio Tracker MCP Server
Main entry point for the FastMCP server.
Initializes the server and binds all available tools.
"""

import os
import sys
from fastmcp import FastMCP

# Import tools
from tools import stock_tools, portfolio_tools
from config import HOST, PORT


# Initialize FastMCP server
mcp = FastMCP("stock-tracker")


# Register Stock Tools
@mcp.tool()
def get_stock_summary(symbol: str) -> dict:
    """
    Get LIVE stock/fund price at the moment of the request (no cached prices).
    Uses Yahoo Finance for equities/ETFs and TEFAS for Turkish mutual funds.

    Args:
        symbol: Stock ticker (e.g. "AAPL", "BIMAS.IS") or TEFAS fund code (e.g. "TP2", "AIS")

    Returns:
        Live summary with current_price, daily_change, volume, source, and as_of date
    """
    return stock_tools.get_stock_summary(symbol)


@mcp.tool()
def get_financial_metrics(symbol: str) -> dict:
    """
    Get detailed financial metrics and ratios for a stock.

    Args:
        symbol: Stock ticker symbol (e.g., "AAPL", "THYAO.IS")

    Returns:
        Financial metrics including P/E, P/B, market cap, and sector info
    """
    return stock_tools.get_financial_metrics(symbol)


# Register Portfolio Tools
@mcp.tool()
def get_portfolio_status() -> dict:
    """
    Get portfolio status with LIVE prices fetched at request time for every holding.
    Revalues all positions (BIST stocks via Yahoo, Turkish funds via TEFAS) when called.

    Returns:
        Portfolio status including total value, positions, P&L, allocation, and price sources
    """
    return portfolio_tools.get_portfolio_status()


@mcp.tool()
def add_portfolio_transaction(symbol: str, shares: float, buy_price: float) -> dict:
    """
    Add a new buy transaction to the portfolio.

    Args:
        symbol: Stock ticker symbol (e.g., "AAPL", "THYAO.IS")
        shares: Number of shares to purchase
        buy_price: Purchase price per share

    Returns:
        Confirmation with updated holding information
    """
    return portfolio_tools.add_portfolio_transaction(symbol, shares, buy_price)


@mcp.tool()
def manage_watchlist(action: str, symbol: str = "") -> dict:
    """
    Manage the watchlist by adding, removing, or listing symbols.

    Args:
        action: One of "add", "remove", or "list"
        symbol: Stock ticker symbol (required for "add"/"remove", optional for "list")

    Returns:
        Watchlist status and current list of symbols
    """
    return portfolio_tools.manage_watchlist(action, symbol)


def main():
    """Start the MCP server."""
    try:
        print(f"Starting Financial & Portfolio Tracker MCP Server")
        print(f"Host: {HOST}")
        print(f"Port: {PORT}")
        print("\nRegistered Tools:")
        print("  - get_stock_summary")
        print("  - get_financial_metrics")
        print("  - get_portfolio_status")
        print("  - add_portfolio_transaction")
        print("  - manage_watchlist")
        print("\nServer running... Press Ctrl+C to stop")
        transport = os.getenv("MCP_TRANSPORT", "stdio").lower()
        if transport in {"http", "streamable-http", "sse"}:
            print(f"Using {transport} transport")
            mcp.run(
                transport=transport,
                host=HOST,
                port=PORT,
                show_banner=False,
            )
        else:
            print("Using stdio transport")
            mcp.run(show_banner=False)
    except KeyboardInterrupt:
        print("\nShutting down server...")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
