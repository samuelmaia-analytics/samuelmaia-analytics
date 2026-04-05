from __future__ import annotations

import json

from config.settings import Settings, get_settings
from core.ai import build_genai_suite
from core.change_drivers import build_change_drivers
from core.contracts import validate_contract
from core.data_quality import run_quality_checks
from core.metric_catalog import build_metric_catalog, export_metric_catalog
from core.metadata_sync import sync_repository_metadata
from core.observability import emit_observability_event
from core.operational_context import build_operational_context
from core.snapshot_history import persist_snapshot_history
from core.writeback import write_sqlite_exports
from core.sample_data import load_portfolio_projects
from core.semantic_metrics import compute_semantic_metrics


def build_portfolio_snapshot(settings: Settings) -> dict[str, object]:
    projects = load_portfolio_projects(settings.raw_portfolio_path)
    projects_payload = [project.__dict__ for project in projects]
    quality_report = run_quality_checks(projects, settings.quality_rules_path)
    semantic_metrics = compute_semantic_metrics(projects, quality_report, settings.semantic_metrics_path)
    metric_catalog = build_metric_catalog(projects, semantic_metrics, settings.semantic_metrics_path)
    repository_registry = sync_repository_metadata(settings)
    operational_context = build_operational_context(settings)
    genai_outputs = build_genai_suite(
        settings=settings,
        projects=projects_payload,
        quality_report=quality_report,
        semantic_metrics=semantic_metrics,
        metric_catalog=metric_catalog,
        repository_registry=repository_registry,
        operational_context=operational_context,
    )
    observability_event = emit_observability_event(
        "portfolio_snapshot_built",
        {
            "project_count": len(projects),
            "decision_readiness_score": semantic_metrics["decision_readiness_score"],
            "quality_pass_rate": semantic_metrics["quality_pass_rate"],
            "platform_trust_score": semantic_metrics["platform_trust_score"],
            "governance_readiness_score": semantic_metrics["governance_readiness_score"],
            "observability_readiness_score": semantic_metrics["observability_readiness_score"],
        },
        settings.observability_dir,
    )

    snapshot = {
        "projects": projects_payload,
        "repository_registry": repository_registry,
        "quality_report": quality_report,
        "semantic_metrics": semantic_metrics,
        "metric_catalog": metric_catalog,
        "operational_context": operational_context,
        "genai_outputs": genai_outputs,
        "genai_insight": genai_outputs["narrative_kpi_insights"],
        "observability_event": observability_event,
    }
    snapshot["change_drivers"] = build_change_drivers(snapshot, settings)
    snapshot_contract_errors = validate_contract(
        snapshot,
        settings.semantic_metrics_path.parents[1] / "contracts" / "v1" / "portfolio_snapshot.schema.json",
    )
    metrics_contract_errors = validate_contract(
        metric_catalog,
        settings.semantic_metrics_path.parents[1] / "contracts" / "v1" / "semantic_metrics_snapshot.schema.json",
    )
    if snapshot_contract_errors:
        raise ValueError(f"Portfolio snapshot contract validation failed: {snapshot_contract_errors}")
    if metrics_contract_errors:
        raise ValueError(f"Semantic metrics contract validation failed: {metrics_contract_errors}")
    settings.artifacts_dir.mkdir(parents=True, exist_ok=True)
    (settings.artifacts_dir / "portfolio_snapshot.json").write_text(
        json.dumps(snapshot, indent=2),
        encoding="utf-8",
    )
    persist_snapshot_history(snapshot, settings.artifacts_dir, snapshot["observability_event"]["timestamp_utc"])
    export_metric_catalog(metric_catalog, settings.artifacts_dir / "semantic_metrics_snapshot.json")
    write_sqlite_exports(snapshot, settings.warehouse_path)
    return snapshot


def main() -> None:
    snapshot = build_portfolio_snapshot(get_settings())
    print(json.dumps(snapshot["semantic_metrics"], indent=2))


if __name__ == "__main__":
    main()
