from __future__ import annotations

from typing import Any

from config.settings import Settings


def build_governance_policy_report(settings: Settings) -> dict[str, Any]:
    checks = [
        _check_threshold_order(settings),
        _check_auth_configuration(settings),
        _check_genai_provider_readiness(settings),
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
        settings.change_watch_threshold <= settings.change_material_threshold <= settings.change_critical_threshold
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


def _build_summary(status: str, failed: list[dict[str, str]], warned: list[dict[str, str]]) -> str:
    if status == "fail":
        return f"Governance policy checks failed on {len(failed)} item(s)."
    if status == "warn":
        return f"Governance policy checks passed with {len(warned)} warning(s)."
    return "Governance policy checks passed."
