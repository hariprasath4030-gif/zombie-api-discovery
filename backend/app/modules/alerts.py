from __future__ import annotations

from typing import Any, Dict, List


def generate_alerts(apis: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    alerts: List[Dict[str, str]] = []

    for api in apis:
        security = api.get("security", {})

        if api.get("status") == "zombie":
            alerts.append(
                {
                    "endpoint": api.get("endpoint", ""),
                    "severity": "high",
                    "reason": "Unreachable API appears defunct",
                    "recommendation": "Decommission endpoint or remove gateway route",
                }
            )

        if security.get("authentication") == "missing":
            alerts.append(
                {
                    "endpoint": api.get("endpoint", ""),
                    "severity": "medium",
                    "reason": "Authentication header not detected",
                    "recommendation": "Enforce API authentication (OAuth2/JWT/mTLS)",
                }
            )

        if security.get("encryption") == "not_detected":
            alerts.append(
                {
                    "endpoint": api.get("endpoint", ""),
                    "severity": "high",
                    "reason": "TLS/HTTPS not detected",
                    "recommendation": "Serve API only over HTTPS",
                }
            )

    deduped = _dedupe_alerts(alerts)
    deduped.sort(key=lambda item: _severity_rank(item.get("severity", "low")))
    return deduped


def suggest_fixes(alerts: List[Dict[str, str]]) -> List[Dict[str, str]]:
    return [
        {
            "endpoint": alert["endpoint"],
            "action": f"Auto-ticket created for: {alert['reason']}",
            "status": "queued",
        }
        for alert in alerts
    ]


def _dedupe_alerts(alerts: List[Dict[str, str]]) -> List[Dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    result: List[Dict[str, str]] = []

    for alert in alerts:
        key = (alert.get("endpoint", ""), alert.get("reason", ""))
        if key in seen:
            continue
        seen.add(key)
        result.append(alert)

    return result


def _severity_rank(severity: str) -> int:
    order = {"high": 0, "medium": 1, "low": 2}
    return order.get(severity, 3)
