#!/usr/bin/env python3
"""
Dependency checker for Stock Tracker MCP Server
Verifies all required packages are installed and working.
"""

import sys


def check_imports():
    """Check if all required packages can be imported."""
    required_packages = {
        "fastmcp": "FastMCP framework",
        "yfinance": "Stock data fetching",
        "pydantic": "Data validation",
        "dotenv": "Environment variable management",
        "requests": "HTTP requests library"
    }

    print("Checking Python package imports...\n")
    all_ok = True

    for package, description in required_packages.items():
        try:
            module = __import__(package)
            # Get version if available
            pkg_version = getattr(module, "__version__", "unknown")
            print(f"✅ {package:<15} - {description:<40} ({pkg_version})")
        except ImportError as e:
            print(f"❌ {package:<15} - {description:<40} NOT INSTALLED")
            all_ok = False

    return all_ok


def check_python_version():
    """Check Python version."""
    print("\nChecking Python version...\n")
    current_version = sys.version_info
    required_version = (3, 8)

    version_string = f"{current_version.major}.{current_version.minor}.{current_version.micro}"
    print(f"Python version: {version_string}")

    if (current_version.major, current_version.minor) >= required_version:
        print(f"✅ Python version OK (required: {required_version[0]}.{required_version[1]}+)\n")
        return True
    else:
        print(f"❌ Python version too old (required: {required_version[0]}.{required_version[1]}+)\n")
        return False


def check_environment_file():
    """Check if .env file exists."""
    import os
    print("Checking environment file...\n")

    if os.path.exists(".env"):
        print("✅ .env file exists")
        return True
    elif os.path.exists(".env.example"):
        print("⚠️  .env file not found, but .env.example exists")
        print("   Create .env: cp .env.example .env")
        return False
    else:
        print("❌ Neither .env nor .env.example found")
        return False


def check_data_directory():
    """Check if data directory exists and is writable."""
    import os
    print("\nChecking data directory...\n")

    if os.path.exists("data"):
        if os.path.isdir("data"):
            print("✅ data/ directory exists")
            if os.access("data", os.W_OK):
                print("✅ data/ directory is writable\n")
                return True
            else:
                print("❌ data/ directory is not writable\n")
                return False
        else:
            print("❌ data/ exists but is not a directory\n")
            return False
    else:
        print("⚠️  data/ directory does not exist")
        print("   It will be created on first run\n")
        return True


def check_config():
    """Check configuration files."""
    import os
    print("Checking configuration files...\n")

    config_checks = [
        ("config.py", "Server configuration"),
        ("main.py", "MCP server entry point"),
        ("services/stock_service.py", "Stock service"),
        ("services/portfolio_service.py", "Portfolio service"),
        ("tools/stock_tools.py", "Stock tools"),
        ("tools/portfolio_tools.py", "Portfolio tools"),
    ]

    all_ok = True
    for file_path, description in config_checks:
        if os.path.exists(file_path):
            print(f"✅ {file_path:<35} - {description}")
        else:
            print(f"❌ {file_path:<35} - {description} NOT FOUND")
            all_ok = False

    print()
    return all_ok


def main():
    """Run all checks."""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║   Financial & Portfolio Tracker - Dependency Checker      ║")
    print("╚═══════════════════════════════════════════════════════════╝\n")

    checks = [
        ("Python Version", check_python_version),
        ("Configuration Files", check_config),
        ("Data Directory", check_data_directory),
        ("Environment File", check_environment_file),
        ("Python Packages", check_imports),
    ]

    results = {}
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"⚠️  Error running {check_name}: {e}\n")
            results[check_name] = False

    # Summary
    print("=" * 63)
    print("SUMMARY")
    print("=" * 63 + "\n")

    all_passed = all(results.values())
    passed_count = sum(results.values())
    total_count = len(results)

    for check_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {check_name}")

    print("\n" + "=" * 63)

    if all_passed:
        print("\n🎉 All checks passed! Your environment is ready.")
        print("\nNext steps:")
        print("  1. Review .env file if needed")
        print("  2. Start the server: python main.py")
        print("  3. Configure Claude Desktop (see CLAUDE_SETUP.md)")
        print()
        return 0
    else:
        print(f"\n⚠️  {total_count - passed_count} check(s) failed.")
        print("\nPlease fix the issues above and try again.")
        print("\nFor help:")
        print("  - Read README.md for setup instructions")
        print("  - Run 'bash setup.sh' for automated setup")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
