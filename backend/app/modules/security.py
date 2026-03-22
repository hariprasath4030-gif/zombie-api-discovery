from __future__ import annotations

from typing import Any, Dict


def check_security(api: Dict[str, Any]) -> Dict[str, str]:
    endpoint = api.get("endpoint", "")
    headers = api.get("headers", {}) or {}

    auth = "present" if "authorization" in {k.lower() for k in headers.keys()} else "missing"
    encryption = "enabled" if endpoint.startswith("https://") else "not_detected"
    rate_limit = "present" if "x-ratelimit-limit" in {k.lower() for k in headers.keys()} else "missing"
    exposure = "high" if "/admin" in endpoint.lower() or "/debug" in endpoint.lower() else "normal"

    return {
        "authentication": auth,
        "encryption": encryption,
        "rate_limiting": rate_limit,
        "data_exposure": exposure,
    }
