from __future__ import annotations

from pathlib import Path

from core.snapshot_history import persist_snapshot_history
from core.trend_series import (
    build_domain_history_series,
    build_metric_history_series,
    build_project_change_summary,
    build_project_history_series,
    build_repository_change_summary,
)


def test_trend_series_builds_rows_from_snapshot_history(tmp_path: Path) -> None:
    artifacts_dir = tmp_path / "processed"
    persist_snapshot_history(
        {
            "semantic_metrics": {
                "decision_readiness_score": 89.0,
                "quality_pass_rate": 98.0,
                "platform_trust_score": 80.0,
                "governance_readiness_score": 85.0,
                "observability_readiness_score": 79.0,
            },
            "observability_event": {"timestamp_utc": "2026-04-05T22:00:00+00:00"},
        },
        artifacts_dir,
        "2026-04-05T22:00:00+00:00",
    )
    persist_snapshot_history(
        {
            "semantic_metrics": {
                "decision_readiness_score": 91.0,
                "quality_pass_rate": 100.0,
                "platform_trust_score": 83.0,
                "governance_readiness_score": 87.0,
                "observability_readiness_score": 81.0,
            },
            "observability_event": {"timestamp_utc": "2026-04-05T22:10:00+00:00"},
        },
        artifacts_dir,
        "2026-04-05T22:10:00+00:00",
    )

    series = build_metric_history_series(artifacts_dir)

    assert len(series) == 2
    assert series[-1]["decision_readiness_score"] == 91.0


def test_domain_history_and_repository_changes_are_built(tmp_path: Path) -> None:
    artifacts_dir = tmp_path / "processed"
    persist_snapshot_history(
        {
            "metric_catalog": {
                "domain_rollup": {
                    "analytics_engineering": {
                        "governance_score": 90.0,
                        "quality_score": 92.0,
                        "execution_score": 88.0,
                        "observability_score": 80.0,
                        "project_count": 1.0,
                    }
                }
            },
            "projects": [{"project_name": "Revenue Intelligence Platform", "domain": "analytics_engineering", "governance_score": 90.0, "quality_score": 92.0, "execution_score": 88.0, "observability_score": 80.0}],
            "repository_registry": [{"id": "repo-a", "markdown_files": 4, "python_files": 10, "tests_present": True, "exists_locally": True, "entrypoint_exists": True}],
            "observability_event": {"timestamp_utc": "2026-04-05T22:00:00+00:00"},
        },
        artifacts_dir,
        "2026-04-05T22:00:00+00:00",
    )
    persist_snapshot_history(
        {
            "metric_catalog": {
                "domain_rollup": {
                    "analytics_engineering": {
                        "governance_score": 91.0,
                        "quality_score": 93.0,
                        "execution_score": 89.0,
                        "observability_score": 82.0,
                        "project_count": 1.0,
                    }
                }
            },
            "projects": [{"project_name": "Revenue Intelligence Platform", "domain": "analytics_engineering", "governance_score": 91.0, "quality_score": 93.0, "execution_score": 89.0, "observability_score": 82.0}],
            "repository_registry": [{"id": "repo-a", "markdown_files": 5, "python_files": 10, "tests_present": True, "exists_locally": True, "entrypoint_exists": True}],
            "observability_event": {"timestamp_utc": "2026-04-05T22:10:00+00:00"},
        },
        artifacts_dir,
        "2026-04-05T22:10:00+00:00",
    )

    domain_series = build_domain_history_series(artifacts_dir)
    project_series = build_project_history_series(artifacts_dir)
    project_changes = build_project_change_summary(artifacts_dir)
    repo_changes = build_repository_change_summary(artifacts_dir)

    assert len(domain_series) == 2
    assert len(project_series) == 2
    assert domain_series[-1]["domain"] == "analytics_engineering"
    assert project_series[-1]["project_name"] == "Revenue Intelligence Platform"
    assert project_changes["changes"][0]["change_type"] == "changed"
    assert repo_changes["changes"][0]["change_type"] == "changed"
