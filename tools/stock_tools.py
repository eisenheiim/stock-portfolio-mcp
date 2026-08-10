"""
Stock Tools Module
Defines MCP tools for stock queries and analysis.
"""

from typing import Any, Dict
from services.stock_service import StockService


def get_stock_summary(symbol: str) -> Dict[str, Any]:
    """
    Get current stock summary including price, daily change, and volume.

    Args:
        symbol: Stock ticker symbol (e.g., "AAPL", "THYAO.IS", "NVDA")

    Returns:
        Dictionary containing:
        - symbol: Ticker symbol
        - current_price: Current trading price
        - daily_change: Price change from previous close
        - daily_change_pct: Percentage change
        - volume: Trading volume
        - previous_close: Previous closing price
        - status: "success" or "error"

    Example:
        >>> get_stock_summary("AAPL")
        {
            "symbol": "AAPL",
            "current_price": 150.25,
            "daily_change": 2.15,
            "daily_change_pct": 1.45,
            "volume": 52000000,
            "previous_close": 148.10,
            "status": "success"
        }
    """
    return StockService.get_stock_summary(symbol)


def get_financial_metrics(symbol: str) -> Dict[str, Any]:
    """
    Get detailed financial metrics and ratios for a stock.

    Args:
        symbol: Stock ticker symbol (e.g., "AAPL", "THYAO.IS")

    Returns:
        Dictionary containing:
        - symbol: Ticker symbol
        - name: Company name
        - sector: Industry sector
        - industry: Specific industry
        - market_cap: Market capitalization
        - pe_ratio: Price-to-Earnings ratio
        - pb_ratio: Price-to-Book ratio
        - ev_ebitda: Enterprise Value to EBITDA ratio
        - dividend_yield: Dividend yield percentage
        - eps: Earnings per share
        - 52_week_high: 52-week high price
        - 52_week_low: 52-week low price
        - avg_volume: Average trading volume
        - status: "success" or "error"

    Example:
        >>> get_financial_metrics("AAPL")
        {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "sector": "Technology",
            "pe_ratio": 28.45,
            "market_cap": 3200000000000,
            "status": "success"
        }
    """
    return StockService.get_financial_metrics(symbol)
