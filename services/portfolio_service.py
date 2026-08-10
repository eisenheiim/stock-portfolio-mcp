"""
Portfolio Service Module
Handles portfolio and watchlist management with JSON persistence.
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from config import PORTFOLIO_FILE, WATCHLIST_FILE
from services.stock_service import StockService


class PortfolioService:
    """Service for managing portfolio and watchlist data."""

    @staticmethod
    def _ensure_portfolio_exists() -> None:
        """Ensure portfolio.json exists with default structure."""
        if not os.path.exists(PORTFOLIO_FILE):
            default_portfolio = {
                "holdings": {
                    "AAPL": {
                        "shares": 10,
                        "average_cost": 150.25,
                        "total_cost": 1502.50,
                        "purchase_dates": ["2025-01-15", "2025-02-20"]
                    },
                    "THYAO.IS": {
                        "shares": 50,
                        "average_cost": 45.30,
                        "total_cost": 2265.00,
                        "purchase_dates": ["2025-01-10"]
                    }
                },
                "last_updated": datetime.now().isoformat()
            }
            with open(PORTFOLIO_FILE, "w") as f:
                json.dump(default_portfolio, f, indent=2)

    @staticmethod
    def _ensure_watchlist_exists() -> None:
        """Ensure watchlist.json exists with default structure."""
        if not os.path.exists(WATCHLIST_FILE):
            default_watchlist = {
                "symbols": ["NVDA", "GOOGL", "MSFT", "GARAN.IS"],
                "last_updated": datetime.now().isoformat()
            }
            with open(WATCHLIST_FILE, "w") as f:
                json.dump(default_watchlist, f, indent=2)

    @staticmethod
    def load_portfolio() -> Dict[str, Any]:
        """
        Load portfolio from JSON file.

        Returns:
            Portfolio dictionary with holdings
        """
        PortfolioService._ensure_portfolio_exists()
        try:
            with open(PORTFOLIO_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            return {
                "error": f"Failed to load portfolio: {str(e)}",
                "holdings": {}
            }

    @staticmethod
    def save_portfolio(portfolio: Dict[str, Any]) -> bool:
        """
        Save portfolio to JSON file.

        Args:
            portfolio: Portfolio dictionary

        Returns:
            True if successful, False otherwise
        """
        try:
            portfolio["last_updated"] = datetime.now().isoformat()
            with open(PORTFOLIO_FILE, "w") as f:
                json.dump(portfolio, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving portfolio: {str(e)}")
            return False

    @staticmethod
    def load_watchlist() -> List[str]:
        """
        Load watchlist from JSON file.

        Returns:
            List of stock symbols
        """
        PortfolioService._ensure_watchlist_exists()
        try:
            with open(WATCHLIST_FILE, "r") as f:
                data = json.load(f)
                return data.get("symbols", [])
        except Exception as e:
            print(f"Error loading watchlist: {str(e)}")
            return []

    @staticmethod
    def save_watchlist(symbols: List[str]) -> bool:
        """
        Save watchlist to JSON file.

        Args:
            symbols: List of stock symbols

        Returns:
            True if successful, False otherwise
        """
        try:
            watchlist = {
                "symbols": symbols,
                "last_updated": datetime.now().isoformat()
            }
            with open(WATCHLIST_FILE, "w") as f:
                json.dump(watchlist, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving watchlist: {str(e)}")
            return False

    @staticmethod
    def get_portfolio_status() -> Dict[str, Any]:
        """
        Get comprehensive portfolio status with current values and PNL.

        Returns:
            Dictionary containing portfolio status, valuations, and P&L
        """
        try:
            portfolio = PortfolioService.load_portfolio()
            holdings = portfolio.get("holdings", {})

            if not holdings:
                return {
                    "status": "empty",
                    "message": "Portfolio is empty",
                    "total_cost_basis": 0,
                    "total_current_value": 0,
                    "total_pnl": 0,
                    "total_pnl_pct": 0,
                    "positions": []
                }

            positions = []
            total_cost_basis = 0
            total_current_value = 0

            for symbol, holding in holdings.items():
                shares = holding.get("shares", 0)
                average_cost = holding.get("average_cost", 0)
                total_cost = holding.get("total_cost", shares * average_cost)

                current_price = StockService.get_stock_price(symbol)

                if current_price is None:
                    continue

                current_value = shares * current_price
                position_pnl = current_value - total_cost
                position_pnl_pct = (position_pnl / total_cost * 100) if total_cost else 0

                positions.append({
                    "symbol": symbol,
                    "shares": shares,
                    "average_cost": round(average_cost, 2),
                    "total_cost": round(total_cost, 2),
                    "current_price": round(current_price, 2),
                    "current_value": round(current_value, 2),
                    "pnl": round(position_pnl, 2),
                    "pnl_pct": round(position_pnl_pct, 2)
                })

                total_cost_basis += total_cost
                total_current_value += current_value

            total_pnl = total_current_value - total_cost_basis
            total_pnl_pct = (total_pnl / total_cost_basis * 100) if total_cost_basis else 0

            # Calculate asset allocation
            allocation = []
            for position in positions:
                pct = (position["current_value"] / total_current_value * 100) if total_current_value else 0
                allocation.append({
                    "symbol": position["symbol"],
                    "percentage": round(pct, 2),
                    "value": position["current_value"]
                })

            return {
                "status": "success",
                "total_cost_basis": round(total_cost_basis, 2),
                "total_current_value": round(total_current_value, 2),
                "total_pnl": round(total_pnl, 2),
                "total_pnl_pct": round(total_pnl_pct, 2),
                "positions": positions,
                "allocation": allocation,
                "last_updated": portfolio.get("last_updated", "N/A")
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "positions": []
            }

    @staticmethod
    def add_transaction(symbol: str, shares: float, buy_price: float) -> Dict[str, Any]:
        """
        Add a buy transaction to portfolio or update existing holding.

        Args:
            symbol: Stock ticker symbol
            shares: Number of shares to purchase
            buy_price: Purchase price per share

        Returns:
            Result dictionary with status and updated holding info
        """
        try:
            portfolio = PortfolioService.load_portfolio()
            holdings = portfolio.get("holdings", {})

            if symbol not in holdings:
                holdings[symbol] = {
                    "shares": 0,
                    "average_cost": 0,
                    "total_cost": 0,
                    "purchase_dates": []
                }

            holding = holdings[symbol]
            old_shares = holding.get("shares", 0)
            old_total_cost = holding.get("total_cost", 0)
            new_transaction_cost = shares * buy_price

            new_total_shares = old_shares + shares
            new_total_cost = old_total_cost + new_transaction_cost
            new_average_cost = new_total_cost / new_total_shares if new_total_shares > 0 else 0

            holding["shares"] = new_total_shares
            holding["average_cost"] = new_average_cost
            holding["total_cost"] = new_total_cost
            holding["purchase_dates"].append(datetime.now().isoformat())

            portfolio["holdings"] = holdings

            if PortfolioService.save_portfolio(portfolio):
                return {
                    "status": "success",
                    "message": f"Added {shares} shares of {symbol}",
                    "symbol": symbol,
                    "new_shares": new_total_shares,
                    "average_cost": round(new_average_cost, 2),
                    "total_cost": round(new_total_cost, 2)
                }
            else:
                return {
                    "status": "error",
                    "message": "Failed to save portfolio"
                }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    @staticmethod
    def manage_watchlist(action: str, symbol: str) -> Dict[str, Any]:
        """
        Manage watchlist by adding, removing, or listing symbols.

        Args:
            action: "add", "remove", or "list"
            symbol: Stock symbol (ignored for "list" action)

        Returns:
            Result dictionary with updated watchlist or current list
        """
        try:
            symbols = PortfolioService.load_watchlist()

            if action.lower() == "add":
                if symbol not in symbols:
                    symbols.append(symbol)
                    if PortfolioService.save_watchlist(symbols):
                        return {
                            "status": "success",
                            "message": f"Added {symbol} to watchlist",
                            "watchlist": symbols
                        }
                    else:
                        return {
                            "status": "error",
                            "message": "Failed to save watchlist"
                        }
                else:
                    return {
                        "status": "info",
                        "message": f"{symbol} is already in watchlist",
                        "watchlist": symbols
                    }

            elif action.lower() == "remove":
                if symbol in symbols:
                    symbols.remove(symbol)
                    if PortfolioService.save_watchlist(symbols):
                        return {
                            "status": "success",
                            "message": f"Removed {symbol} from watchlist",
                            "watchlist": symbols
                        }
                    else:
                        return {
                            "status": "error",
                            "message": "Failed to save watchlist"
                        }
                else:
                    return {
                        "status": "info",
                        "message": f"{symbol} not found in watchlist",
                        "watchlist": symbols
                    }

            elif action.lower() == "list":
                return {
                    "status": "success",
                    "watchlist": symbols,
                    "count": len(symbols)
                }

            else:
                return {
                    "status": "error",
                    "message": "Invalid action. Use 'add', 'remove', or 'list'."
                }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
