#!/usr/bin/env python3
"""
Test and demo script for Stock Tracker MCP tools.
Run from project root: python scripts/demo.py
"""

import sys

import _bootstrap  # noqa: F401

from services.portfolio_service import PortfolioService
from services.stock_service import StockService


def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def test_stock_tools():
    print_section("TESTING STOCK TOOLS")

    print("Testing get_stock_summary('AAPL')...")
    result = StockService.get_stock_summary("AAPL")
    if result.get("status") == "success":
        print(f"  Current Price: ${result.get('current_price')}")
        print(f"  Daily Change: {result.get('daily_change_pct')}%")
    else:
        print(f"  Error: {result.get('error', 'Unknown error')}")

    print("\nTesting get_stock_summary('THYAO.IS')...")
    result = StockService.get_stock_summary("THYAO.IS")
    if result.get("status") == "success":
        print(f"  Current Price: {result.get('current_price')} TRY")
        print(f"  Daily Change: {result.get('daily_change_pct')}%")
    else:
        print(f"  Error: {result.get('error', 'Unknown error')}")

    print("\nTesting get_financial_metrics('AAPL')...")
    result = StockService.get_financial_metrics("AAPL")
    if result.get("status") == "success":
        print(f"  Company: {result.get('name')}")
        print(f"  P/E Ratio: {result.get('pe_ratio')}")
    else:
        print(f"  Error: {result.get('error', 'Unknown error')}")


def test_portfolio_tools():
    print_section("TESTING PORTFOLIO TOOLS")

    print("Testing get_portfolio_status()...")
    result = PortfolioService.get_portfolio_status()
    if result.get("status") == "success":
        print(f"  Total Value: {result.get('total_current_value')}")
        print(f"  Total P&L: {result.get('total_pnl')} ({result.get('total_pnl_pct')}%)")
        for pos in result.get("positions", [])[:5]:
            print(f"    {pos['symbol']}: {pos['shares']} @ {pos['current_price']}")
        if len(result.get("positions", [])) > 5:
            print(f"    ... and {len(result['positions']) - 5} more")
    elif result.get("status") == "empty":
        print(f"  {result.get('message')}")
    else:
        print(f"  Error: {result.get('error', 'Unknown error')}")

    print("\nTesting manage_watchlist('list')...")
    result = PortfolioService.manage_watchlist("list", "")
    if result.get("status") == "success":
        print(f"  Watchlist ({result.get('count')} items): {', '.join(result.get('watchlist', []))}")
    else:
        print(f"  Error: {result.get('message', 'Unknown error')}")


def main():
    print("\nStock Tracker MCP — Demo\n")
    try:
        test_stock_tools()
        test_portfolio_tools()
        print("\nDemo complete. Start MCP server: python main.py")
        print("Setup guide: docs/setup.md\n")
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
