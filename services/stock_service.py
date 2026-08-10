"""
Stock Service Module
Handles stock data retrieval from yfinance and financial metrics calculation.
"""

import yfinance as yf
from typing import Optional, Dict, Any
from decimal import Decimal


class StockService:
    """Service for fetching and processing stock data."""

    @staticmethod
    def get_stock_summary(symbol: str) -> Dict[str, Any]:
        """
        Fetch stock summary including current price, daily change, and volume.

        Args:
            symbol: Stock ticker symbol (e.g., "AAPL", "THYAO.IS")

        Returns:
            Dictionary containing stock summary data

        Raises:
            ValueError: If symbol is invalid or data cannot be fetched
        """
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d")

            if hist.empty:
                raise ValueError(f"No data found for symbol: {symbol}")

            info = ticker.info
            current_price = info.get("currentPrice") or hist["Close"].iloc[-1]
            previous_close = info.get("previousClose") or hist["Open"].iloc[0]
            volume = int(hist["Volume"].iloc[-1]) if "Volume" in hist.columns else 0

            daily_change = current_price - previous_close
            daily_change_pct = (daily_change / previous_close * 100) if previous_close else 0

            return {
                "symbol": symbol,
                "current_price": round(float(current_price), 2),
                "daily_change": round(float(daily_change), 2),
                "daily_change_pct": round(float(daily_change_pct), 2),
                "volume": volume,
                "previous_close": round(float(previous_close), 2),
                "status": "success"
            }

        except Exception as e:
            return {
                "symbol": symbol,
                "error": str(e),
                "status": "error"
            }

    @staticmethod
    def get_financial_metrics(symbol: str) -> Dict[str, Any]:
        """
        Fetch detailed financial metrics for a stock.

        Args:
            symbol: Stock ticker symbol (e.g., "AAPL", "THYAO.IS")

        Returns:
            Dictionary containing financial metrics

        Raises:
            ValueError: If symbol is invalid or data cannot be fetched
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info

            metrics = {
                "symbol": symbol,
                "name": info.get("longName", "N/A"),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                "market_cap": info.get("marketCap", "N/A"),
                "pe_ratio": round(info.get("trailingPE", 0), 2) if info.get("trailingPE") else "N/A",
                "pb_ratio": round(info.get("priceToBook", 0), 2) if info.get("priceToBook") else "N/A",
                "ev_ebitda": round(info.get("enterpriseToEbitda", 0), 2) if info.get("enterpriseToEbitda") else "N/A",
                "dividend_yield": round(info.get("dividendYield", 0) * 100, 2) if info.get("dividendYield") else "N/A",
                "eps": round(info.get("trailingEps", 0), 2) if info.get("trailingEps") else "N/A",
                "52_week_high": round(info.get("fiftyTwoWeekHigh", 0), 2) if info.get("fiftyTwoWeekHigh") else "N/A",
                "52_week_low": round(info.get("fiftyTwoWeekLow", 0), 2) if info.get("fiftyTwoWeekLow") else "N/A",
                "avg_volume": info.get("averageVolume", "N/A"),
                "status": "success"
            }

            return metrics

        except Exception as e:
            return {
                "symbol": symbol,
                "error": str(e),
                "status": "error"
            }

    @staticmethod
    def get_stock_price(symbol: str) -> Optional[float]:
        """
        Get current stock price for a symbol.

        Args:
            symbol: Stock ticker symbol

        Returns:
            Current price as float, or None if fetch fails
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return float(info.get("currentPrice", 0)) or None
        except Exception:
            return None
