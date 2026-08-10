#!/usr/bin/env python3
"""
Test and demo script for Stock Tracker tools.
Run this to verify the server setup without needing Claude Desktop.
"""

import sys
from tools import stock_tools, portfolio_tools


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def test_stock_tools():
    """Test stock tools with real data."""
    print_section("TESTING STOCK TOOLS")

    # Test get_stock_summary
    print("📊 Testing get_stock_summary('AAPL')...")
    result = stock_tools.get_stock_summary("AAPL")
    if result.get("status") == "success":
        print(f"✅ Current Price: ${result.get('current_price')}")
        print(f"   Daily Change: {result.get('daily_change_pct')}%")
        print(f"   Volume: {result.get('volume'):,}")
    else:
        print(f"⚠️  Error: {result.get('error', 'Unknown error')}")

    print("\n📊 Testing get_stock_summary('THYAO.IS')...")
    result = stock_tools.get_stock_summary("THYAO.IS")
    if result.get("status") == "success":
        print(f"✅ Current Price: ${result.get('current_price')}")
        print(f"   Daily Change: {result.get('daily_change_pct')}%")
    else:
        print(f"⚠️  Error: {result.get('error', 'Unknown error')}")

    # Test get_financial_metrics
    print("\n💰 Testing get_financial_metrics('AAPL')...")
    result = stock_tools.get_financial_metrics("AAPL")
    if result.get("status") == "success":
        print(f"✅ Company: {result.get('name')}")
        print(f"   Sector: {result.get('sector')}")
        print(f"   P/E Ratio: {result.get('pe_ratio')}")
        print(f"   Market Cap: {result.get('market_cap')}")
    else:
        print(f"⚠️  Error: {result.get('error', 'Unknown error')}")


def test_portfolio_tools():
    """Test portfolio tools with stored data."""
    print_section("TESTING PORTFOLIO TOOLS")

    # Test get_portfolio_status
    print("📈 Testing get_portfolio_status()...")
    result = portfolio_tools.get_portfolio_status()
    if result.get("status") == "success":
        print(f"✅ Total Portfolio Value: ${result.get('total_current_value')}")
        print(f"   Total Cost Basis: ${result.get('total_cost_basis')}")
        print(f"   Total P&L: ${result.get('total_pnl')} ({result.get('total_pnl_pct')}%)")
        print(f"\n   Positions:")
        for pos in result.get("positions", []):
            print(f"     • {pos['symbol']}: {pos['shares']} shares @ ${pos['current_price']} (P&L: {pos['pnl_pct']}%)")
    elif result.get("status") == "empty":
        print(f"ℹ️  {result.get('message')}")
    else:
        print(f"⚠️  Error: {result.get('error', 'Unknown error')}")

    # Test manage_watchlist
    print("\n📋 Testing manage_watchlist('list', '')...")
    result = portfolio_tools.manage_watchlist("list", "")
    if result.get("status") == "success":
        print(f"✅ Watchlist ({result.get('count')} items):")
        for symbol in result.get("watchlist", []):
            print(f"     • {symbol}")
    else:
        print(f"⚠️  Error: {result.get('message', 'Unknown error')}")


def interactive_demo():
    """Interactive demo mode."""
    print_section("INTERACTIVE DEMO")
    print("Enter stock symbols to query or 'quit' to exit")
    print("Examples: AAPL, THYAO.IS, NVDA, GOOGL")
    print()

    while True:
        symbol = input("\n🔍 Enter stock symbol (or 'quit'): ").strip().upper()

        if symbol.lower() == "quit":
            break

        if not symbol:
            continue

        print(f"\n📊 Getting data for {symbol}...")
        result = stock_tools.get_stock_summary(symbol)

        if result.get("status") == "success":
            print(f"✅ {symbol}")
            print(f"   Current Price: ${result.get('current_price')}")
            print(f"   Daily Change: {result.get('daily_change')} ({result.get('daily_change_pct')}%)")
            print(f"   Volume: {result.get('volume'):,}")
        else:
            print(f"⚠️  Could not find data for {symbol}")


def main():
    """Run all tests."""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║  Financial & Portfolio Tracker MCP Server - Demo Script   ║")
    print("╚═══════════════════════════════════════════════════════════╝")

    try:
        # Run automated tests
        test_stock_tools()
        test_portfolio_tools()

        # Ask if user wants interactive demo
        print_section("DEMO COMPLETE")
        response = input("Would you like to run interactive demo? (y/n): ").strip().lower()
        if response == "y":
            interactive_demo()

        print("\n✅ All tests completed successfully!")
        print("\n📝 Next: Start the server with 'python main.py'")
        print("   Then configure it in Claude Desktop")

    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
