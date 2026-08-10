#!/usr/bin/env python3
"""
Check portfolio for loss-recovery / rising-while-red alerts and email them.

Usage:
  ./venv/bin/python check_alerts.py           # check + email
  ./venv/bin/python check_alerts.py --dry-run # print only, no email
  ./venv/bin/python check_alerts.py --seed    # mark current losers without mailing

Schedule (every 30 min on macOS launchd or cron), e.g. cron:
  */30 10-18 * * 1-5 cd /Users/sude/stockmarket && ./venv/bin/python check_alerts.py
"""

from __future__ import annotations

import argparse
import json
import sys

from services.alert_service import AlertService
from services.email_service import EmailService
from services.portfolio_service import PortfolioService


def seed_loss_state() -> dict:
    """Mark currently underwater positions as in_loss without sending mail."""
    status = PortfolioService.get_portfolio_status()
    if status.get("status") != "success":
        return {"status": "error", "message": status.get("message") or status.get("error")}

    state = AlertService._load_state()
    positions = state.setdefault("positions", {})
    marked = 0
    for position in status.get("positions", []):
        avg = float(position.get("average_cost") or 0)
        price = float(position.get("current_price") or 0)
        if avg <= 0 or price <= 0:
            continue
        key = AlertService._position_key(position)
        in_loss = price < avg
        prev = positions.get(key, {})
        positions[key] = {
            **prev,
            "in_loss": in_loss,
            "symbol": position.get("symbol"),
            "broker": position.get("broker"),
            "last_price": price,
            "average_cost": avg,
        }
        if in_loss:
            marked += 1
    AlertService._save_state(state)
    return {"status": "success", "marked_in_loss": marked, "total": len(status.get("positions", []))}


def main() -> int:
    parser = argparse.ArgumentParser(description="Portfolio loss recovery email alerts")
    parser.add_argument("--dry-run", action="store_true", help="Do not send email")
    parser.add_argument(
        "--seed",
        action="store_true",
        help="Record current losing positions without emailing (run once first)",
    )
    args = parser.parse_args()

    if args.seed:
        result = seed_loss_state()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result.get("status") == "success" else 1

    if not args.dry_run and not EmailService.is_configured():
        print(
            "Email ayarları eksik. .env içine SMTP_HOST, SMTP_USER, SMTP_PASSWORD, "
            "ALERT_EMAIL_TO ekle.\n"
            "Önce denemek için: ./venv/bin/python check_alerts.py --dry-run",
            file=sys.stderr,
        )
        result = AlertService.check_and_notify(send_email=False)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 2

    result = AlertService.check_and_notify(send_email=not args.dry_run)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("status") == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
