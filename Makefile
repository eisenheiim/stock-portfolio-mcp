.PHONY: help install run demo alerts clean setup

help:
	@echo "Stock Tracker MCP — Makefile"
	@echo ""
	@echo "  make setup      Create venv and install dependencies"
	@echo "  make install    Install dependencies only"
	@echo "  make run        Start MCP server"
	@echo "  make demo       Run demo script"
	@echo "  make alerts     Check alerts (dry-run)"
	@echo "  make clean      Remove cache files"
	@echo ""

setup:
	bash setup.sh

install:
	pip install -r requirements.txt

run:
	python main.py

demo:
	python scripts/demo.py

alerts:
	python scripts/check_alerts.py --dry-run

check:
	python scripts/check_dependencies.py

clean:
	rm -rf __pycache__ .pytest_cache
	find . -type d -name __pycache__ -not -path './venv/*' -exec rm -rf {} + 2>/dev/null || true

.DEFAULT_GOAL := help
