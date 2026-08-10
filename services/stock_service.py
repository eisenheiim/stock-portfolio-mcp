"""
Stock Service Module
Handles stock data retrieval from yfinance and TEFAS fund prices.
Always fetches fresh market data at call time (no local price cache).
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any, Dict, Optional

import requests
import yfinance as yf


# Known Turkish mutual-fund codes in this project (TEFAS / non-Yahoo).
TEFAS_FUND_CODES = {
    "AIS", "TP2", "BGP", "IRF", "AFT", "IJB", "VK8",
}


class StockService:
    """Service for fetching and processing stock and fund data."""

    @staticmethod
    def _is_tefas_fund(symbol: str) -> bool:
        clean = symbol.strip().upper().replace(".IS", "")
        return clean in TEFAS_FUND_CODES or (
            "." not in symbol and len(symbol) <= 5 and symbol.isalpha()
            and symbol.upper() in TEFAS_FUND_CODES
        )

    @staticmethod
    def _normalize_symbol(symbol: str) -> str:
        return symbol.strip().upper()

    @staticmethod
    def _price_from_yahoo(symbol: str) -> Optional[Dict[str, Any]]:
        """Fetch the freshest available Yahoo quote for a symbol."""
        ticker = yf.Ticker(symbol)
        info = ticker.info or {}
        hist = ticker.history(period="5d")

        current_price = (
            info.get("currentPrice")
            or info.get("regularMarketPrice")
            or info.get("navPrice")
        )
        previous_close = info.get("previousClose") or info.get("regularMarketPreviousClose")
        volume = info.get("volume") or info.get("regularMarketVolume") or 0

        if hist is not None and not hist.empty:
            last_close = float(hist["Close"].iloc[-1])
            if current_price is None:
                current_price = last_close
            if previous_close is None and len(hist) >= 2:
                previous_close = float(hist["Close"].iloc[-2])
            elif previous_close is None:
                previous_close = float(hist["Open"].iloc[-1])
            if "Volume" in hist.columns and not volume:
                volume = int(hist["Volume"].iloc[-1])

        if current_price is None:
            return None

        current_price = float(current_price)
        previous_close = float(previous_close) if previous_close else current_price
        daily_change = current_price - previous_close
        daily_change_pct = (daily_change / previous_close * 100) if previous_close else 0.0

        return {
            "symbol": symbol,
            "current_price": round(current_price, 4),
            "daily_change": round(daily_change, 4),
            "daily_change_pct": round(daily_change_pct, 2),
            "volume": int(volume) if volume else 0,
            "previous_close": round(previous_close, 4),
            "source": "yahoo",
            "as_of": date.today().isoformat(),
            "status": "success",
        }

    @staticmethod
    def _price_from_tefas(fund_code: str) -> Optional[Dict[str, Any]]:
        """
        Fetch latest TEFAS fund price via the public API.
        Fast-fail: short timeout and few attempts so portfolio valuation stays responsive.
        """
        code = fund_code.strip().upper().replace(".IS", "")
        url = "https://www.tefas.gov.tr/api/funds/fonGnlBlgSiraliGetir"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Origin": "https://www.tefas.gov.tr",
            "Referer": "https://www.tefas.gov.tr/",
        }

        # Only try today and previous weekday once each for YAT (covers almost all holdings).
        for days_back in (0, 1, 3):
            d = (date.today() - timedelta(days=days_back)).strftime("%Y-%m-%d")
            payload = {
                "fonTip": "YAT",
                "fonKod": code,
                "baslangicTarih": d,
                "bitisTarih": d,
            }
            try:
                response = requests.post(
                    url, json=payload, headers=headers, timeout=3
                )
                if response.status_code != 200:
                    continue
                data = response.json()
                rows = data.get("resultList") if isinstance(data, dict) else data
                if not rows:
                    continue
                row = rows[-1] if isinstance(rows, list) else rows
                price = (
                    row.get("fiyat")
                    or row.get("price")
                    or row.get("birimPayFiyat")
                )
                if price is None:
                    continue
                price = float(price)
                return {
                    "symbol": code,
                    "current_price": round(price, 6),
                    "daily_change": 0.0,
                    "daily_change_pct": 0.0,
                    "volume": 0,
                    "previous_close": round(price, 6),
                    "source": "tefas",
                    "as_of": d,
                    "name": row.get("fonAd") or row.get("fund_name"),
                    "status": "success",
                }
            except Exception:
                # Network/TEFAS issues should not block portfolio valuation.
                return None
        return None

    @staticmethod
    def get_stock_summary(symbol: str) -> Dict[str, Any]:
        """
        Fetch live stock/fund summary at request time.

        Args:
            symbol: Stock ticker (e.g. "AAPL", "THYAO.IS") or TEFAS fund code (e.g. "TP2")
        """
        symbol = StockService._normalize_symbol(symbol)
        try:
            if StockService._is_tefas_fund(symbol):
                result = StockService._price_from_tefas(symbol)
                if result:
                    return result
                return {
                    "symbol": symbol,
                    "error": (
                        f"Live TEFAS price unavailable for {symbol}. "
                        "Portfolio will use last report price until TEFAS responds."
                    ),
                    "status": "error",
                }

            result = StockService._price_from_yahoo(symbol)
            if result:
                return result
            raise ValueError(f"No data found for symbol: {symbol}")

        except Exception as e:
            return {
                "symbol": symbol,
                "error": str(e),
                "status": "error",
            }

    @staticmethod
    def get_financial_metrics(symbol: str) -> Dict[str, Any]:
        """Fetch detailed financial metrics for a stock."""
        symbol = StockService._normalize_symbol(symbol)
        try:
            if StockService._is_tefas_fund(symbol):
                summary = StockService.get_stock_summary(symbol)
                if summary.get("status") != "success":
                    return {
                        "symbol": symbol,
                        "error": summary.get("error", "Fund metrics unavailable"),
                        "status": "error",
                    }
                return {
                    "symbol": symbol,
                    "name": summary.get("name", symbol),
                    "sector": "Investment Fund",
                    "industry": "TEFAS Fund",
                    "market_cap": "N/A",
                    "pe_ratio": "N/A",
                    "pb_ratio": "N/A",
                    "ev_ebitda": "N/A",
                    "dividend_yield": "N/A",
                    "eps": "N/A",
                    "52_week_high": "N/A",
                    "52_week_low": "N/A",
                    "avg_volume": "N/A",
                    "current_price": summary.get("current_price"),
                    "source": summary.get("source"),
                    "as_of": summary.get("as_of"),
                    "status": "success",
                }

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
                "source": "yahoo",
                "as_of": date.today().isoformat(),
                "status": "success",
            }
            return metrics

        except Exception as e:
            return {
                "symbol": symbol,
                "error": str(e),
                "status": "error",
            }

    @staticmethod
    def get_stock_price(symbol: str) -> Optional[float]:
        """
        Get current live price for a symbol.
        Prefer Yahoo for equities/ETFs; TEFAS for Turkish funds.
        """
        summary = StockService.get_stock_summary(symbol)
        if summary.get("status") == "success":
            return float(summary["current_price"])
        return None
