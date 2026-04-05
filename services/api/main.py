from __future__ import annotations

from typing import Annotated

from fastapi import Depends, FastAPI

from config.settings import get_settings
from core.catalog import load_business_glossary, load_dataset_catalog
from core.analytics_engineering import run_analytics_engineering_checks
from core.governance_policy import build_governance_policy_report
from core.pipeline import build_portfolio_snapshot
from core.runtime_config import build_runtime_config_summary
from services.api.security import require_scope


app = FastAPI(
    title="Samuel Maia Analytics Portfolio API",
    version="0.1.0",
    description="Enterprise-style API base for portfolio analytics, quality, metrics, and GenAI insights.",
)

SnapshotScope = Annotated[str, Depends(require_scope("snapshot"))]
MetricsScope = Annotated[str, Depends(require_scope("metrics"))]
InsightsScope = Annotated[str, Depends(require_scope("insights"))]
RepositoriesScope = Annotated[str, Depends(require_scope("repositories"))]


@app.get("/health")
def health() -> dict[str, str]:
    settings = get_settings()
    return {"status": "ok", "environment": settings.env}


@app.get("/snapshot")
def snapshot(_api_key: SnapshotScope) -> dict[str, object]:
    return build_portfolio_snapshot(get_settings())


@app.get("/governance/runtime-config")
def governance_runtime_config(_api_key: SnapshotScope) -> dict[str, object]:
    return build_runtime_config_summary(get_settings())


@app.get("/governance/policy-checks")
def governance_policy_checks(_api_key: SnapshotScope) -> dict[str, object]:
    return build_governance_policy_report(get_settings())


@app.get("/governance/analytics-engineering")
def governance_analytics_engineering(_api_key: SnapshotScope) -> dict[str, object]:
    return run_analytics_engineering_checks(get_settings())


@app.get("/quality/status")
def quality_status(_api_key: SnapshotScope) -> dict[str, object]:
    snapshot_payload = build_portfolio_snapshot(get_settings())
    return snapshot_payload["quality_report"]


@app.get("/catalog/datasets")
def catalog_datasets(_api_key: SnapshotScope) -> dict[str, object]:
    return load_dataset_catalog(get_settings())


@app.get("/catalog/glossary")
def catalog_glossary(_api_key: SnapshotScope) -> dict[str, object]:
    return load_business_glossary(get_settings())


@app.get("/catalog/metrics")
def catalog_metrics(_api_key: SnapshotScope) -> dict[str, object]:
    snapshot_payload = build_portfolio_snapshot(get_settings())
    return snapshot_payload["metric_catalog"]


@app.get("/metrics")
def metrics(_api_key: MetricsScope) -> dict[str, object]:
    snapshot_payload = build_portfolio_snapshot(get_settings())
    return {
        "headline": snapshot_payload["semantic_metrics"],
        "catalog": snapshot_payload["metric_catalog"],
    }


@app.get("/metrics/history")
def metrics_history(_api_key: MetricsScope) -> dict[str, object]:
    snapshot_payload = build_portfolio_snapshot(get_settings())
    return {
        "series": snapshot_payload["operational_context"]["snapshot_history"].get("metric_history_series", []),
        "summary": snapshot_payload["operational_context"]["snapshot_history"].get("comparison_summary"),
    }


@app.get("/metrics/domain-history")
def metrics_domain_history(_api_key: MetricsScope) -> dict[str, object]:
    snapshot_payload = build_portfolio_snapshot(get_settings())
    return {
        "series": snapshot_payload["operational_context"]["snapshot_history"].get("domain_history_series", []),
    }


@app.get("/metrics/project-history")
def metrics_project_history(_api_key: MetricsScope) -> dict[str, object]:
    snapshot_payload = build_portfolio_snapshot(get_settings())
    history = snapshot_payload["operational_context"]["snapshot_history"]
    return {
        "series": history.get("project_history_series", []),
        "changes": history.get("project_change_summary", {}),
    }


@app.get("/insights")
def insights(_api_key: InsightsScope) -> dict[str, str]:
    snapshot_payload = build_portfolio_snapshot(get_settings())
    return snapshot_payload["genai_insight"]


@app.get("/genai")
def genai_suite(_api_key: InsightsScope) -> dict[str, object]:
    snapshot_payload = build_portfolio_snapshot(get_settings())
    return {"artifacts": snapshot_payload["genai_outputs"]}


@app.get("/change-drivers")
def change_drivers(_api_key: InsightsScope) -> dict[str, object]:
    snapshot_payload = build_portfolio_snapshot(get_settings())
    return snapshot_payload["change_drivers"]


@app.get("/repositories")
def repositories(_api_key: RepositoriesScope) -> dict[str, object]:
    snapshot_payload = build_portfolio_snapshot(get_settings())
    return {
        "projects": snapshot_payload["repository_registry"],
        "changes": snapshot_payload["operational_context"]["snapshot_history"].get("repository_change_summary", {}),
    }
