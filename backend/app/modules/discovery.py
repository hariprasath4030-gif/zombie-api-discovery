from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import requests


def scan_urls(urls: List[str]) -> List[Dict[str, Any]]:
    discovered: List[Dict[str, Any]] = []
    for url in urls:
        endpoint = url.rstrip("/")
        try:
            response = requests.get(endpoint, timeout=4)
            discovered.append(
                {
                    "source": "url_scan",
                    "endpoint": endpoint,
                    "method": "GET",
                    "status_code": response.status_code,
                    "is_reachable": response.ok,
                    "headers": dict(response.headers),
                }
            )
        except requests.RequestException:
            discovered.append(
                {
                    "source": "url_scan",
                    "endpoint": endpoint,
                    "method": "GET",
                    "status_code": None,
                    "is_reachable": False,
                    "headers": {},
                }
            )
    return discovered


def scan_swagger(swagger_urls: List[str]) -> List[Dict[str, Any]]:
    discovered: List[Dict[str, Any]] = []
    for swagger_url in swagger_urls:
        try:
            response = requests.get(swagger_url, timeout=6)
            response.raise_for_status()
            document = response.json()
            paths = document.get("paths", {})
            for path, methods in paths.items():
                if not isinstance(methods, dict):
                    continue
                for method in methods.keys():
                    discovered.append(
                        {
                            "source": "swagger",
                            "endpoint": path,
                            "method": method.upper(),
                            "status_code": 200,
                            "is_reachable": True,
                            "headers": {},
                        }
                    )
        except (requests.RequestException, json.JSONDecodeError):
            discovered.append(
                {
                    "source": "swagger",
                    "endpoint": swagger_url,
                    "method": "GET",
                    "status_code": None,
                    "is_reachable": False,
                    "headers": {},
                }
            )
    return discovered


def scan_logs(log_paths: List[str]) -> List[Dict[str, Any]]:
    discovered: List[Dict[str, Any]] = []
    for log_path in log_paths:
        path = Path(log_path)
        if not path.exists() or not path.is_file():
            continue

        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if line.startswith("/"):
                discovered.append(
                    {
                        "source": "log",
                        "endpoint": line,
                        "method": "GET",
                        "status_code": None,
                        "is_reachable": False,
                        "headers": {},
                    }
                )
    return discovered


def discover_apis(urls: List[str], swagger_urls: List[str], log_paths: List[str]) -> List[Dict[str, Any]]:
    combined = scan_urls(urls) + scan_swagger(swagger_urls) + scan_logs(log_paths)

    unique = {}
    for item in combined:
        unique_key = (item["endpoint"], item["method"])
        if unique_key not in unique:
            unique[unique_key] = item
    return list(unique.values())
