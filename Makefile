.PHONY: help install run demo test clean setup

help:
	@echo "Financial & Portfolio Tracker MCP Server - Makefile"
	@echo "===================================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make setup      - Create venv and install dependencies"
	@echo "  make install    - Install dependencies only"
	@echo "  make run        - Start the MCP server"
	@echo "  make demo       - Run demo/test script"
	@echo "  make clean      - Remove venv and cache files"
	@echo "  make help       - Show this help message"
	@echo ""

setup:
	@echo "Setting up project..."
	bash setup.sh

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

run:
	@echo "Starting Financial & Portfolio Tracker MCP Server..."
	python main.py

demo:
	@echo "Running demo script..."
	python demo.py

test:
	@echo "Running tests..."
	python demo.py

clean:
	@echo "Cleaning up..."
	rm -rf venv __pycache__ .pytest_cache *.pyc
	find . -type d -name __pycache__ -exec rm -rf {} +
	@echo "Cleanup complete"

.DEFAULT_GOAL := help
