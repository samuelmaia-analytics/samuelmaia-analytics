from __future__ import annotations

from pathlib import Path

from core.snapshot_history import persist_snapshot_history, summarize_snapshot_history


def test_snapshot_history_persists_and_compares(tmp_path: Path) -> None:
    artifacts_dir = tmp_path / "processed"
    first = {
        "projects": [{"project_name": "A"}],
        "repository_registry": [{"id": "repo-a"}],
        "quality_report": {"pass_rate": 95.0},
        "metric_catalog": {"definitions": [{"name": "decision_readiness_score"}]},
        "genai_outputs": {"narrative_kpi_insights": {}},
    }
    second = {
        "projects": [{"project_name": "A"}, {"project_name": "B"}],
        "repository_registry": [{"id": "repo-a"}, {"id": "repo-b"}],
        "quality_report": {"pass_rate": 100.0},
        "metric_catalog": {"definitions": [{"name": "decision_readiness_score"}, {"name": "platform_trust_score"}]},
        "genai_outputs": {"narrative_kpi_insights": {}, "executive_summary": {}},
    }

    persist_snapshot_history(first, artifacts_dir, "2026-04-05T22:00:00+00:00")
    persist_snapshot_history(second, artifacts_dir, "2026-04-05T22:10:00+00:00")
    summary = summarize_snapshot_history(artifacts_dir)

    assert summary["snapshot_count"] == 2
    assert summary["changes"]["project_count_delta"] == 1
    assert summary["changes"]["quality_pass_rate_delta"] == 5.0
    assert summary["changes"]["added_repositories"] == ["repo-b"]
