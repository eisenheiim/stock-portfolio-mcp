#!/usr/bin/env python3
"""Verify project install. Run: python scripts/check_dependencies.py"""

import os
import sys

import _bootstrap  # noqa: F401


def check_imports():
    required = {
        "fastmcp": "FastMCP framework",
        "yfinance": "Stock data fetching",
        "pydantic": "Data validation",
        "dotenv": "Environment variables",
        "requests": "HTTP client",
    }
    print("Checking Python packages...\n")
    ok = True
    for package, desc in required.items():
        try:
            mod = __import__(package)
            ver = getattr(mod, "__version__", "unknown")
            print(f"  OK  {package:<12} {desc} ({ver})")
        except ImportError:
            print(f"  FAIL {package:<12} {desc}")
            ok = False
    print()
    return ok


def check_files():
    print("Checking project files...\n")
    paths = [
        "main.py",
        "config.py",
        "services/stock_service.py",
        "services/portfolio_service.py",
        "services/alert_service.py",
        "scripts/check_alerts.py",
        "scripts/demo.py",
        "data/portfolio.example.json",
    ]
    ok = True
    for path in paths:
        if os.path.exists(path):
            print(f"  OK  {path}")
        else:
            print(f"  FAIL {path}")
            ok = False
    print()
    return ok


def main():
    print("\nStock Tracker — dependency check\n")
    py_ok = sys.version_info >= (3, 8)
    print(f"Python {sys.version_info.major}.{sys.version_info.minor} — {'OK' if py_ok else 'FAIL (need 3.8+)'}\n")
    files_ok = check_files()
    imports_ok = check_imports()
    env_ok = os.path.exists(".env") or os.path.exists(".env.example")
    print(f".env — {'OK' if os.path.exists('.env') else 'missing (copy from .env.example)'}\n")

    if py_ok and files_ok and imports_ok:
        print("All checks passed.\nNext: python main.py  |  Setup: docs/setup.md\n")
        return 0
    print("Some checks failed. Run: bash setup.sh\n")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
