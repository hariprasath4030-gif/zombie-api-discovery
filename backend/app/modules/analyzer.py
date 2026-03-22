from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List, Tuple


def classify_status(api: Dict[str, Any]) -> Tuple[str, List[str]]:
    notes: List[str] = []
    status_code = api.get("status_code")
    reachable = api.get("is_reachable", False)
    endpoint = api.get("endpoint", "")

    if "deprecated" in endpoint.lower():
        notes.append("Endpoint name indicates deprecated API")
        return "deprecated", notes

    if not reachable and status_code is None:
        notes.append("Endpoint unreachable during scan")
        return "zombie", notes

    if status_code in {404, 410}:
        notes.append("Returned not found/gone")
        return "orphaned", notes

    if status_code and 200 <= status_code < 400:
        notes.append("Responding normally")
        return "active", notes

    notes.append("No strong signal; marked orphaned for review")
    return "orphaned", notes


def build_summary(apis: List[Dict[str, Any]]) -> Dict[str, int]:
    counter = Counter(api["status"] for api in apis)
    return dict(counter)
