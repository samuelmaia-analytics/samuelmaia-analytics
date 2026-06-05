from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_data_governance_summary(config_path: Path) -> dict[str, Any]:
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    inventory = payload.get("data_inventory", [])
    contains_personal_data = any(item.get("contains_personal_data", False) for item in inventory)
    contains_sensitive_personal_data = any(
        item.get("contains_sensitive_personal_data", False) for item in inventory
    )
    retention_days = [
        item.get("retention_days") for item in inventory if item.get("retention_days") is not None
    ]

    return {
        "policy_version": payload.get("policy_version", "unknown"),
        "review_frequency": payload.get("review_frequency", "unspecified"),
        "datasets": len(inventory),
        "contains_personal_data": contains_personal_data,
        "contains_sensitive_personal_data": contains_sensitive_personal_data,
        "minimum_retention_days": min(retention_days) if retention_days else None,
        "classifications": sorted({item.get("classification", "unknown") for item in inventory}),
        "controls": payload.get("controls", {}),
        "lgpd_positioning": payload.get("lgpd_positioning", {}),
        "inventory": inventory,
    }
