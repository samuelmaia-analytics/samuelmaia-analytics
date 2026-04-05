from __future__ import annotations

from config.settings import get_settings
from core.data_quality import run_quality_checks
from core.metric_catalog import build_metric_catalog
from core.sample_data import load_portfolio_projects
from core.semantic_metrics import compute_semantic_metrics


def test_semantic_metrics_are_positive() -> None:
    settings = get_settings()
    projects = load_portfolio_projects(settings.raw_portfolio_path)
    quality_report = run_quality_checks(projects, settings.quality_rules_path)
    metrics = compute_semantic_metrics(projects, quality_report, settings.semantic_metrics_path)
    assert metrics["decision_readiness_score"] > 0
    assert metrics["quality_pass_rate"] == 100.0
    assert metrics["platform_trust_score"] > 0
    assert metrics["governance_readiness_score"] > 0


def test_metric_catalog_contains_domain_rollup() -> None:
    settings = get_settings()
    projects = load_portfolio_projects(settings.raw_portfolio_path)
    quality_report = run_quality_checks(projects, settings.quality_rules_path)
    metrics = compute_semantic_metrics(projects, quality_report, settings.semantic_metrics_path)
    catalog = build_metric_catalog(projects, metrics, settings.semantic_metrics_path)
    assert "domain_rollup" in catalog
    assert "revenue_analytics" in catalog["domain_rollup"]
