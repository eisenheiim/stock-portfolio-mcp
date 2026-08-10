"""
Portfolio recovery / rise alerts for positions currently at a loss.
"""

from __future__ import annotations

import json
import os
from datetime import date, datetime
from typing import Any, Dict, List

from config import ALERT_MODE, ALERT_RISE_PCT, ALERT_STATE_FILE
from services.email_service import EmailService
from services.portfolio_service import PortfolioService
from services.stock_service import StockService


class AlertService:
    """Detect loss-recovery and rising-while-red events, then email."""

    @staticmethod
    def _position_key(position: Dict[str, Any]) -> str:
        broker = position.get("broker") or "Unknown"
        symbol = position.get("symbol") or "?"
        currency = position.get("currency") or "TRY"
        return f"{broker}|{symbol}|{currency}"

    @staticmethod
    def _load_state() -> Dict[str, Any]:
        if not os.path.exists(ALERT_STATE_FILE):
            return {"positions": {}, "last_run": None}
        try:
            with open(ALERT_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"positions": {}, "last_run": None}

    @staticmethod
    def _save_state(state: Dict[str, Any]) -> None:
        state["last_run"] = datetime.now().isoformat()
        os.makedirs(os.path.dirname(ALERT_STATE_FILE), exist_ok=True)
        with open(ALERT_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

    @staticmethod
    def check_and_notify(send_email: bool = True) -> Dict[str, Any]:
        status = PortfolioService.get_portfolio_status()
        if status.get("status") != "success":
            return {
                "status": "error",
                "message": status.get("message") or status.get("error") or "No portfolio",
                "alerts": [],
            }

        state = AlertService._load_state()
        pos_state: Dict[str, Any] = state.setdefault("positions", {})
        alerts: List[Dict[str, Any]] = []
        today = date.today().isoformat()
        mode = (ALERT_MODE or "both").lower()

        for position in status.get("positions", []):
            key = AlertService._position_key(position)
            avg = float(position.get("average_cost") or 0)
            price = float(position.get("current_price") or 0)
            pnl_pct = float(position.get("pnl_pct") or 0)
            if avg <= 0 or price <= 0:
                continue

            in_loss_now = price < avg
            prev = pos_state.get(key, {})
            was_in_loss = bool(prev.get("in_loss"))

            # Track underwater positions.
            if in_loss_now:
                pos_state[key] = {
                    **prev,
                    "in_loss": True,
                    "symbol": position.get("symbol"),
                    "broker": position.get("broker"),
                    "last_price": price,
                    "average_cost": avg,
                }
            else:
                pos_state[key] = {
                    **prev,
                    "in_loss": False,
                    "symbol": position.get("symbol"),
                    "broker": position.get("broker"),
                    "last_price": price,
                    "average_cost": avg,
                }

            # 1) Recovered to break-even / profit
            if mode in {"both", "breakeven"} and was_in_loss and not in_loss_now:
                last_be = prev.get("last_breakeven_alert")
                if last_be != today:
                    alerts.append({
                        "type": "breakeven",
                        "symbol": position.get("symbol"),
                        "broker": position.get("broker"),
                        "currency": position.get("currency", "TRY"),
                        "average_cost": avg,
                        "current_price": price,
                        "pnl_pct": pnl_pct,
                        "message": "Zarardan çıktı / alış fiyatına ulaştı",
                    })
                    pos_state[key]["last_breakeven_alert"] = today

            # 2) Still in loss, but rising today
            if mode in {"both", "rise"} and in_loss_now:
                symbol = position.get("symbol")
                asset_type = position.get("asset_type", "stock")
                daily_pct = None
                if asset_type != "fund":
                    summary = StockService.get_stock_summary(symbol)
                    if summary.get("status") == "success":
                        daily_pct = float(summary.get("daily_change_pct") or 0)

                if daily_pct is not None and daily_pct >= ALERT_RISE_PCT:
                    last_rise = prev.get("last_rise_alert_date")
                    if last_rise != today:
                        alerts.append({
                            "type": "rise",
                            "symbol": symbol,
                            "broker": position.get("broker"),
                            "currency": position.get("currency", "TRY"),
                            "average_cost": avg,
                            "current_price": price,
                            "pnl_pct": pnl_pct,
                            "message": (
                                f"Hâlâ zararda ama bugün %{daily_pct:.2f} yükseldi "
                                f"(eşik %{ALERT_RISE_PCT})"
                            ),
                        })
                        pos_state[key]["last_rise_alert_date"] = today

        AlertService._save_state(state)

        email_result = {"status": "skipped", "message": "send_email=False"}
        if send_email and alerts:
            email_result = EmailService.send_alert_digest(alerts)
        elif send_email and not alerts:
            email_result = {"status": "skipped", "message": "No new alerts"}

        return {
            "status": "success",
            "alert_count": len(alerts),
            "alerts": alerts,
            "email": email_result,
            "mode": mode,
            "rise_threshold_pct": ALERT_RISE_PCT,
        }
