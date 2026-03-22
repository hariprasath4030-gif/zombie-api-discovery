from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import AlertResponse, DiscoveryRequest, DiscoveryResponse
from app.modules.alerts import generate_alerts, suggest_fixes
from app.modules.analyzer import build_summary, classify_status
from app.modules.discovery import discover_apis
from app.modules.security import check_security
from app.storage import load_results, save_results

app = FastAPI(title="Zombie API Discovery & Defence")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _looks_like_swagger_doc(value: str) -> bool:
    lowered = value.lower()
    return any(token in lowered for token in ("swagger", "openapi", "api-docs"))


def _normalize_discovery_input(payload: DiscoveryRequest) -> tuple[list[str], list[str], list[str]]:
    urls = [item.strip() for item in payload.urls if item and item.strip()]
    swagger_urls = [item.strip() for item in payload.swagger_urls if item and item.strip()]
    log_paths = [item.strip() for item in payload.log_paths if item and item.strip()]

    normalized_urls = list(urls)
    normalized_swagger: list[str] = []

    for value in swagger_urls:
        if _looks_like_swagger_doc(value):
            normalized_swagger.append(value)
        else:
            normalized_urls.append(value)

    final_urls: list[str] = []
    for value in normalized_urls:
        if _looks_like_swagger_doc(value):
            normalized_swagger.append(value)
        else:
            final_urls.append(value)

    deduped_urls = list(dict.fromkeys(final_urls))
    deduped_swagger = list(dict.fromkeys(normalized_swagger))
    deduped_logs = list(dict.fromkeys(log_paths))

    return deduped_urls, deduped_swagger, deduped_logs


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/api/discover", response_model=DiscoveryResponse)
def api_discover(payload: DiscoveryRequest) -> DiscoveryResponse:
    urls, swagger_urls, log_paths = _normalize_discovery_input(payload)
    discovered = discover_apis(urls, swagger_urls, log_paths)

    enriched = []
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

    response = {
        "total": len(enriched),
        "summary": build_summary(enriched),
        "apis": enriched,
    }
    save_results(response)
    return response


@app.get("/api/results", response_model=DiscoveryResponse)
def api_results() -> DiscoveryResponse:
    results = load_results()
    return DiscoveryResponse(**results)


@app.get("/api/alerts", response_model=AlertResponse)
def api_alerts() -> AlertResponse:
    apis = load_results().get("apis", [])
    alerts = generate_alerts(apis)
    return AlertResponse(total=len(alerts), alerts=alerts)


@app.post("/api/fix")
def api_fix() -> Dict[str, object]:
    apis = load_results().get("apis", [])
    alerts = generate_alerts(apis)
    fixes = suggest_fixes(alerts)
    return {"total": len(fixes), "fixes": fixes}


@app.get("/api/report")
def api_report() -> Dict[str, object]:
    results = load_results()
    apis = results.get("apis", [])
    alerts = generate_alerts(apis)
    fixes = suggest_fixes(alerts)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_apis": results.get("total", 0),
        "summary": results.get("summary", {}),
        "alerts_total": len(alerts),
        "fixes_total": len(fixes),
        "alerts": alerts,
        "fixes": fixes,
        "apis": apis,
    }
