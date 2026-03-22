from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

DATA_FILE = Path(__file__).resolve().parent / "data" / "api_results.json"


def save_results(payload: Dict[str, Any]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_results() -> Dict[str, Any]:
    if not DATA_FILE.exists():
        return {"total": 0, "summary": {}, "apis": []}
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def load_apis() -> List[Dict[str, Any]]:
    return load_results().get("apis", [])
