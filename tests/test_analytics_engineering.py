from __future__ import annotations

from dataclasses import replace

from config.settings import get_settings
from core.analytics_engineering import run_analytics_engineering_checks
from core.pipeline import build_portfolio_snapshot


def test_analytics_engineering_runner_passes_on_local_warehouse(tmp_path) -> None:
    settings = get_settings()
    test_settings = replace(
        settings,
        artifacts_dir=tmp_path / "processed",
        observability_dir=tmp_path / "observability",
        warehouse_path=tmp_path / "warehouse" / "portfolio_platform.db",
    )
    build_portfolio_snapshot(test_settings)
    report = run_analytics_engineering_checks(test_settings)
    assert report["status"] == "ok"
    assert report["models_built"] >= 10
    assert report["failed_tests"] == 0
