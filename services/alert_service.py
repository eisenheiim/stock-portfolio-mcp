"""
Portfolio recovery / rise / sudden-spike alerts.
"""

from __future__ import annotations

import json
import os
from datetime import date, datetime
from typing import Any, Dict, List, Set

from config import (
    ALERT_MODE,
    ALERT_NEAR_LOW_PCT,
    ALERT_RISE_PCT,
    ALERT_SPIKE_LOOKBACK_DAYS,
    ALERT_SPIKE_PCT,
    ALERT_STATE_FILE,
)
from services.email_service import EmailService
from services.portfolio_service import PortfolioService
from services.stock_service import StockService


class AlertService:
    """Detect loss-recovery, rising-while-red, and sudden spike events."""

    @staticmethod
    def _enabled_modes(mode: str) -> Set[str]:
        raw = (mode or "all").lower().strip()
        if raw in {"all", "both"}:
            # both kept for backward compat; includes spike
            return {"breakeven", "rise", "spike"}
        return {part.strip() for part in raw.split(",") if part.strip()}

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
        enabled = AlertService._enabled_modes(ALERT_MODE)
        summary_cache: Dict[str, Dict[str, Any]] = {}

        for position in status.get("positions", []):
            key = AlertService._position_key(position)
            avg = float(position.get("average_cost") or 0)
            price = float(position.get("current_price") or 0)
            pnl_pct = float(position.get("pnl_pct") or 0)
            symbol = position.get("symbol")
            asset_type = position.get("asset_type", "stock")
            if avg <= 0 or price <= 0 or not symbol:
                continue

            in_loss_now = price < avg
            prev = pos_state.get(key, {})
            was_in_loss = bool(prev.get("in_loss"))

            pos_state[key] = {
                **prev,
                "in_loss": in_loss_now,
                "symbol": symbol,
                "broker": position.get("broker"),
                "last_price": price,
                "average_cost": avg,
            }

            # 1) Recovered to break-even / profit
            if "breakeven" in enabled and was_in_loss and not in_loss_now:
                if prev.get("last_breakeven_alert") != today:
                    alerts.append({
                        "type": "breakeven",
                        "symbol": symbol,
                        "broker": position.get("broker"),
                        "currency": position.get("currency", "TRY"),
                        "average_cost": avg,
                        "current_price": price,
                        "pnl_pct": pnl_pct,
                        "message": "Zarardan çıktı / alış fiyatına ulaştı",
                    })
                    pos_state[key]["last_breakeven_alert"] = today

            needs_quote = asset_type != "fund" and (
                ("rise" in enabled and in_loss_now) or ("spike" in enabled)
            )
            summary = None
            if needs_quote:
                if symbol not in summary_cache:
                    summary_cache[symbol] = StockService.get_stock_summary(symbol)
                summary = summary_cache[symbol]

            # 2) Still in loss, but rising today
            if "rise" in enabled and in_loss_now and summary and summary.get("status") == "success":
                daily_pct = float(summary.get("daily_change_pct") or 0)
                if daily_pct >= ALERT_RISE_PCT and prev.get("last_rise_alert_date") != today:
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

            # 3) Sudden spike from a recent low
            if "spike" in enabled and asset_type != "fund":
                spike = StockService.detect_sudden_spike(
                    symbol,
                    spike_pct=ALERT_SPIKE_PCT,
                    lookback_days=ALERT_SPIKE_LOOKBACK_DAYS,
                    near_low_pct=ALERT_NEAR_LOW_PCT,
                    summary=summary,
                )
                if spike.get("is_spike") and prev.get("last_spike_alert_date") != today:
                    alerts.append({
                        "type": "spike",
                        "symbol": symbol,
                        "broker": position.get("broker"),
                        "currency": position.get("currency", "TRY"),
                        "average_cost": avg,
                        "current_price": price,
                        "pnl_pct": pnl_pct,
                        "message": (
                            f"Düşükten ani sıçrayış: bugün %{spike['daily_change_pct']:.2f} "
                            f"(son {spike['lookback_days']}g dip {spike['recent_low']}, "
                            f"önceki kapanış {spike['previous_close']})"
                        ),
                    })
                    pos_state[key]["last_spike_alert_date"] = today

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
            "mode": ALERT_MODE,
            "enabled": sorted(enabled),
            "rise_threshold_pct": ALERT_RISE_PCT,
            "spike_threshold_pct": ALERT_SPIKE_PCT,
            "near_low_pct": ALERT_NEAR_LOW_PCT,
            "spike_lookback_days": ALERT_SPIKE_LOOKBACK_DAYS,
        }
