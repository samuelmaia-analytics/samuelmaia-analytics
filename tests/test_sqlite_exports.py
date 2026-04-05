from __future__ import annotations

import sqlite3
from dataclasses import replace

from config.settings import get_settings
from core.pipeline import build_portfolio_snapshot


def test_sqlite_exports_create_expected_tables(tmp_path) -> None:
    settings = get_settings()
    test_settings = replace(
        settings,
        artifacts_dir=tmp_path / "processed",
        observability_dir=tmp_path / "observability",
        warehouse_path=tmp_path / "warehouse" / "portfolio_platform.db",
    )
    build_portfolio_snapshot(test_settings)
    with sqlite3.connect(test_settings.warehouse_path) as conn:
        tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type IN ('table', 'view')")}
        history_rows = list(conn.execute("SELECT timestamp_utc, decision_readiness_score FROM metric_history"))
        domain_rows = list(conn.execute("SELECT timestamp_utc, domain FROM domain_history"))
        project_rows = list(conn.execute("SELECT timestamp_utc, project_name FROM project_history"))
    assert "portfolio_projects" in tables
    assert "repository_registry" in tables
    assert "metric_history" in tables
    assert "domain_history" in tables
    assert "project_history" in tables
    assert "v_portfolio_scores" in tables
    assert "v_metric_history_latest" in tables
    assert "v_domain_history_latest" in tables
    assert "v_project_history_latest" in tables
    assert history_rows
    assert domain_rows
    assert project_rows
