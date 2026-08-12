#!/usr/bin/env python3
"""Backward-compatible wrapper. Prefer: python scripts/demo.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))
from demo import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
