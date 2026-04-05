from __future__ import annotations

from dataclasses import replace

from config.settings import get_settings
from core.pipeline import build_portfolio_snapshot


def test_pipeline_builds_snapshot(tmp_path) -> None:
    settings = get_settings()
    test_settings = replace(
        settings,
        artifacts_dir=tmp_path / "processed",
        observability_dir=tmp_path / "observability",
        warehouse_path=tmp_path / "warehouse" / "portfolio_platform.db",
    )
    snapshot = build_portfolio_snapshot(test_settings)
    assert "semantic_metrics" in snapshot
    assert "operational_context" in snapshot
    assert "genai_outputs" in snapshot
    assert "executive_summary" in snapshot["genai_outputs"]
    assert (test_settings.artifacts_dir / "portfolio_snapshot.json").exists()
    history_dir = test_settings.artifacts_dir / "history"
    assert history_dir.exists()
    assert list(history_dir.glob("portfolio_snapshot_*.json"))
    assert (test_settings.artifacts_dir / "semantic_metrics_snapshot.json").exists()
    assert test_settings.warehouse_path.exists()
