"""
Portfolio Tools Module
Defines MCP tools for portfolio and watchlist management.
"""

from typing import Any, Dict, List
from services.portfolio_service import PortfolioService


def get_portfolio_status() -> Dict[str, Any]:
    """
    Get comprehensive portfolio status with current values, allocations, and P&L.

    Returns:
        Dictionary containing:
        - status: "success", "empty", or "error"
        - total_cost_basis: Total amount invested
        - total_current_value: Current total portfolio value
        - total_pnl: Total profit/loss in absolute terms
        - total_pnl_pct: Total profit/loss as percentage
        - positions: List of individual position details
        - allocation: Asset allocation percentages
        - last_updated: Timestamp of last update

    Example:
        >>> get_portfolio_status()
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
                    "current_price": 155.50,
                    "current_value": 1555.00,
                    "pnl": 52.50,
                    "pnl_pct": 3.49
                }
            ],
            "allocation": [
                {"symbol": "AAPL", "percentage": 37.47, "value": 1555.00}
            ]
        }
    """
    return PortfolioService.get_portfolio_status()


def add_portfolio_transaction(symbol: str, shares: float, buy_price: float) -> Dict[str, Any]:
    """
    Add a new buy transaction to the portfolio or update average cost for existing holdings.

    Args:
        symbol: Stock ticker symbol (e.g., "AAPL", "THYAO.IS")
        shares: Number of shares to purchase (e.g., 10, 50.5)
        buy_price: Purchase price per share in USD or local currency

    Returns:
        Dictionary containing:
        - status: "success" or "error"
        - message: Description of the transaction
        - symbol: Ticker symbol
        - new_shares: Total shares after transaction
        - average_cost: Updated average cost per share
        - total_cost: Updated total cost basis

    Example:
        >>> add_portfolio_transaction("AAPL", 10, 150.25)
        {
            "status": "success",
            "message": "Added 10 shares of AAPL",
            "symbol": "AAPL",
            "new_shares": 20,
            "average_cost": 150.25,
            "total_cost": 3005.00
        }
    """
    return PortfolioService.add_transaction(symbol, shares, buy_price)


def manage_watchlist(action: str, symbol: str = "") -> Dict[str, Any]:
    """
    Manage the watchlist by adding, removing, or listing symbols.

    Args:
        action: One of "add", "remove", or "list"
        symbol: Stock ticker symbol (required for "add" and "remove", ignored for "list")

    Returns:
        Dictionary containing:
        - status: "success", "info", or "error"
        - message: Description of the action
        - watchlist: Current list of symbols (for all actions)
        - count: Number of symbols in watchlist (for "list" action)

    Example:
        >>> manage_watchlist("add", "NVDA")
        {
            "status": "success",
            "message": "Added NVDA to watchlist",
            "watchlist": ["AAPL", "THYAO.IS", "NVDA"],
            "count": 3
        }

        >>> manage_watchlist("list", "")
        {
            "status": "success",
            "watchlist": ["AAPL", "THYAO.IS", "NVDA"],
            "count": 3
        }
    """
    return PortfolioService.manage_watchlist(action, symbol)
