#!/bin/bash
# Quick start script for Financial & Portfolio Tracker MCP Server

echo "🚀 Financial & Portfolio Tracker MCP Server Setup"
echo "=================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate

echo "📥 Installing dependencies..."
pip install -q -r requirements.txt
echo "✅ Dependencies installed"

echo ""
echo "⚙️  Setting up configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ .env file created from .env.example"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "📂 Checking data directory..."
mkdir -p data
echo "✅ Data directory ready"

echo ""
echo "🎯 Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Review .env file if needed"
echo "  2. Start the server: python main.py"
echo "  3. Configure Claude Desktop with the provided config"
echo ""
echo "To start the server, run:"
echo "  source venv/bin/activate"
echo "  python main.py"
