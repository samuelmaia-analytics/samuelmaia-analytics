from __future__ import annotations

from config.settings import Settings
from core.governance_policy import build_governance_policy_report


def build_health_report(settings: Settings) -> dict[str, object]:
    paths = {
        "raw_portfolio_path": settings.raw_portfolio_path,
        "semantic_metrics_path": settings.semantic_metrics_path,
        "quality_rules_path": settings.quality_rules_path,
        "project_registry_path": settings.project_registry_path,
    }
    return {
        "status": "ok" if all(path.exists() for path in paths.values()) else "degraded",
        "environment": settings.env,
        "paths": {name: {"path": str(path), "exists": path.exists()} for name, path in paths.items()},
        "warehouse_path": str(settings.warehouse_path),
        "governance_policy_status": build_governance_policy_report(settings)["status"],
    }
