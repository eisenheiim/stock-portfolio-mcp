"""
Email helper for portfolio alerts.
"""

from __future__ import annotations

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from config import (
    ALERT_EMAIL_FROM,
    ALERT_EMAIL_TO,
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_USER,
    SMTP_USE_TLS,
)


class EmailService:
    """Send alert emails over SMTP."""

    @staticmethod
    def is_configured() -> bool:
        return bool(SMTP_HOST and SMTP_USER and SMTP_PASSWORD and ALERT_EMAIL_TO)

    @staticmethod
    def send(subject: str, body_text: str, body_html: str | None = None) -> dict:
        if not EmailService.is_configured():
            return {
                "status": "error",
                "message": (
                    "Email not configured. Set SMTP_HOST, SMTP_USER, SMTP_PASSWORD, "
                    "ALERT_EMAIL_TO in .env"
                ),
            }

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = ALERT_EMAIL_FROM or SMTP_USER
        msg["To"] = ALERT_EMAIL_TO
        msg.attach(MIMEText(body_text, "plain", "utf-8"))
        if body_html:
            msg.attach(MIMEText(body_html, "html", "utf-8"))

        try:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
                if SMTP_USE_TLS:
                    server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.sendmail(msg["From"], [ALERT_EMAIL_TO], msg.as_string())
            return {"status": "success", "to": ALERT_EMAIL_TO, "subject": subject}
        except Exception as exc:
            return {"status": "error", "message": str(exc)}

    @staticmethod
    def send_alert_digest(alerts: List[dict]) -> dict:
        if not alerts:
            return {"status": "skipped", "message": "No alerts to send"}

        lines = []
        html_rows = []
        for alert in alerts:
            line = (
                f"- [{alert['type']}] {alert['symbol']} ({alert.get('broker', '')}) "
                f"| alış {alert['average_cost']} → şu an {alert['current_price']} "
                f"| K/Z {alert['pnl_pct']}% | {alert['message']}"
            )
            lines.append(line)
            html_rows.append(
                "<tr>"
                f"<td>{alert['type']}</td>"
                f"<td>{alert['symbol']}</td>"
                f"<td>{alert.get('broker', '')}</td>"
                f"<td>{alert['average_cost']}</td>"
                f"<td>{alert['current_price']}</td>"
                f"<td>{alert['pnl_pct']}%</td>"
                f"<td>{alert['message']}</td>"
                "</tr>"
            )

        subject = f"Portföy uyarısı: {len(alerts)} hisse"
        body_text = "Zarardaki / toparlanan pozisyon uyarısı\n\n" + "\n".join(lines)
        body_html = (
            "<h2>Portföy uyarısı</h2>"
            "<table border='1' cellpadding='6' cellspacing='0'>"
            "<tr><th>Tip</th><th>Sembol</th><th>Broker</th><th>Alış</th>"
            "<th>Fiyat</th><th>K/Z %</th><th>Mesaj</th></tr>"
            + "".join(html_rows)
            + "</table>"
        )
        return EmailService.send(subject, body_text, body_html)
