from __future__ import annotations

import json
import os
from datetime import datetime, timezone

from app.modules.alerts import generate_alerts, suggest_fixes
from app.modules.analyzer import build_summary, classify_status
from app.modules.discovery import discover_apis
from app.modules.security import check_security
from app.storage import save_results


def _parse_csv_env(name: str, default: str) -> list[str]:
    raw = os.getenv(name, default)
    return [item.strip() for item in raw.split(",") if item.strip()]


def run() -> None:
    urls = _parse_csv_env(
        "SCAN_URLS",
        "https://jsonplaceholder.typicode.com/posts,https://jsonplaceholder.typicode.com/users",
    )
    swagger_urls = _parse_csv_env("SCAN_SWAGGER_URLS", "https://petstore3.swagger.io/api/v3/openapi.json")
    log_paths = _parse_csv_env("SCAN_LOG_PATHS", "")

    discovered = discover_apis(urls, swagger_urls, log_paths)
    enriched: list[dict[str, object]] = []

    for api in discovered:
        status, notes = classify_status(api)
        security = check_security(api)
        enriched.append(
            {
                "source": api["source"],
                "endpoint": api["endpoint"],
                "method": api["method"],
                "status_code": api["status_code"],
                "is_reachable": api["is_reachable"],
                "status": status,
                "security": security,
                "notes": notes,
            }
        )

    results = {
        "total": len(enriched),
        "summary": build_summary(enriched),
        "apis": enriched,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    save_results(results)

    alerts = generate_alerts(enriched)
    fixes = suggest_fixes(alerts)
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_apis": len(enriched),
        "summary": results["summary"],
        "alerts_total": len(alerts),
        "fixes_total": len(fixes),
        "alerts": alerts,
        "fixes": fixes,
    }

    with open("scheduled-report.json", "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)

    print(json.dumps({"total_apis": report["total_apis"], "summary": report["summary"]}))


if __name__ == "__main__":
    run()
