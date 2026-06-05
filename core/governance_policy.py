from __future__ import annotations

import json
from typing import Any

from config.settings import Settings


def build_governance_policy_report(settings: Settings) -> dict[str, Any]:
    checks = [
        _check_threshold_order(settings),
        _check_auth_configuration(settings),
        _check_genai_provider_readiness(settings),
        _check_data_governance_inventory(settings),
        _check_retention_policy(settings),
        _check_lgpd_positioning(settings),
    ]
    failed = [check for check in checks if check["status"] == "fail"]
    warned = [check for check in checks if check["status"] == "warn"]
    status = "ok"
    if failed:
        status = "fail"
    elif warned:
        status = "warn"

    return {
        "status": status,
        "checks": checks,
        "summary": _build_summary(status, failed, warned),
    }


def _check_threshold_order(settings: Settings) -> dict[str, str]:
    ordered = (
        settings.change_watch_threshold
        <= settings.change_material_threshold
        <= settings.change_critical_threshold
    )
    return {
        "check": "change_driver_threshold_order",
        "status": "pass" if ordered else "fail",
        "detail": (
            f"watch={settings.change_watch_threshold}, material={settings.change_material_threshold}, "
            f"critical={settings.change_critical_threshold}"
        ),
    }


def _check_auth_configuration(settings: Settings) -> dict[str, str]:
    if settings.jwt_enabled and len(settings.jwt_secret) < 32:
        return {
            "check": "auth_configuration",
            "status": "fail",
            "detail": "JWT is enabled but the secret is shorter than the minimum required length.",
        }
    if not settings.service_api_keys and not settings.jwt_enabled:
        return {
            "check": "auth_configuration",
            "status": "fail",
            "detail": "No API key or JWT mode configured for protected endpoints.",
        }
    return {
        "check": "auth_configuration",
        "status": "pass",
        "detail": "Protected surfaces have an active authentication mode.",
    }


def _check_genai_provider_readiness(settings: Settings) -> dict[str, str]:
    if settings.genai_provider == "openai-compatible":
        if settings.genai_base_url and settings.genai_api_key:
            return {
                "check": "genai_provider_readiness",
                "status": "pass",
                "detail": "OpenAI-compatible provider is configured with base URL and API key.",
            }
        return {
            "check": "genai_provider_readiness",
            "status": "warn",
            "detail": "OpenAI-compatible mode selected without full remote provider configuration; local fallback will be used.",
        }
    return {
        "check": "genai_provider_readiness",
        "status": "pass",
        "detail": "Local deterministic GenAI mode is active.",
    }


def _check_data_governance_inventory(settings: Settings) -> dict[str, str]:
    payload = json.loads(settings.data_governance_path.read_text(encoding="utf-8"))
    inventory = payload.get("data_inventory", [])
    if not inventory:
        return {
            "check": "data_governance_inventory",
            "status": "fail",
            "detail": "No data inventory entries are documented.",
        }
    missing = [
        item.get("dataset", "unknown")
        for item in inventory
        if "classification" not in item
        or "contains_personal_data" not in item
        or "retention_days" not in item
    ]
    if missing:
        return {
            "check": "data_governance_inventory",
            "status": "fail",
            "detail": f"Inventory is missing required governance metadata for: {', '.join(missing)}.",
        }
    return {
        "check": "data_governance_inventory",
        "status": "pass",
        "detail": f"{len(inventory)} dataset(s) have classification, privacy, and retention metadata.",
    }


def _check_retention_policy(settings: Settings) -> dict[str, str]:
    payload = json.loads(settings.data_governance_path.read_text(encoding="utf-8"))
    inventory = payload.get("data_inventory", [])
    invalid = [
        item.get("dataset", "unknown")
        for item in inventory
        if not isinstance(item.get("retention_days"), int)
    ]
    if invalid:
        return {
            "check": "retention_policy",
            "status": "fail",
            "detail": f"Retention is not defined as whole days for: {', '.join(invalid)}.",
        }
    return {
        "check": "retention_policy",
        "status": "pass",
        "detail": "Retention windows are documented for the current data inventory.",
    }


def _check_lgpd_positioning(settings: Settings) -> dict[str, str]:
    payload = json.loads(settings.data_governance_path.read_text(encoding="utf-8"))
    positioning = payload.get("lgpd_positioning", {})
    inventory = payload.get("data_inventory", [])
    if not positioning.get("assessment"):
        return {
            "check": "lgpd_positioning",
            "status": "fail",
            "detail": "LGPD applicability assessment is not documented.",
        }
    has_personal_data = any(item.get("contains_personal_data", False) for item in inventory)
    if has_personal_data and positioning.get(
        "data_subject_request_process", ""
    ).strip().lower().startswith("document before"):
        return {
            "check": "lgpd_positioning",
            "status": "warn",
            "detail": "Personal data is flagged in inventory, but the data subject request process is still placeholder-level.",
        }
    return {
        "check": "lgpd_positioning",
        "status": "pass",
        "detail": "LGPD positioning and privacy baseline are documented for the current inventory.",
    }


def _build_summary(status: str, failed: list[dict[str, str]], warned: list[dict[str, str]]) -> str:
    if status == "fail":
        return f"Governance policy checks failed on {len(failed)} item(s)."
    if status == "warn":
        return f"Governance policy checks passed with {len(warned)} warning(s)."
    return "Governance policy checks passed."
