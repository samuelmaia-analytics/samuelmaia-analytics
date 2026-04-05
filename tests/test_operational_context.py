from __future__ import annotations

from dataclasses import replace

from config.settings import get_settings
from core.operational_context import build_operational_context
from core.snapshot_history import persist_snapshot_history


def test_operational_context_includes_freshness_and_lineage(tmp_path) -> None:
    settings = replace(
        get_settings(),
        artifacts_dir=tmp_path / "processed",
        observability_dir=tmp_path / "observability",
        warehouse_path=tmp_path / "warehouse" / "portfolio_platform.db",
    )
    settings.artifacts_dir.mkdir(parents=True, exist_ok=True)
    settings.observability_dir.mkdir(parents=True, exist_ok=True)
    (settings.artifacts_dir / "portfolio_snapshot.json").write_text("{}", encoding="utf-8")
    persist_snapshot_history({}, settings.artifacts_dir, "2026-04-05T22:00:00+00:00")
    (settings.observability_dir / "events.jsonl").write_text(
        '{"event_name":"portfolio_snapshot_built","timestamp_utc":"2026-04-05T22:00:00+00:00","payload":{"project_count":4}}\n',
        encoding="utf-8",
    )

    context = build_operational_context(settings)

    assert "freshness" in context
    assert "lineage" in context
    assert "run_history" in context
    assert "snapshot_history" in context
    assert context["freshness"]["artifacts"]["portfolio_snapshot"]["exists"] is True
    assert context["recent_events"][0]["event_name"] == "portfolio_snapshot_built"


def test_operational_context_builds_run_history_deltas(tmp_path) -> None:
    settings = replace(
        get_settings(),
        artifacts_dir=tmp_path / "processed",
        observability_dir=tmp_path / "observability",
        warehouse_path=tmp_path / "warehouse" / "portfolio_platform.db",
    )
    settings.observability_dir.mkdir(parents=True, exist_ok=True)
    (settings.observability_dir / "events.jsonl").write_text(
        "\n".join(
            [
                '{"event_name":"portfolio_snapshot_built","timestamp_utc":"2026-04-05T22:00:00+00:00","payload":{"project_count":4,"decision_readiness_score":89.0,"platform_trust_score":81.0}}',
                '{"event_name":"portfolio_snapshot_built","timestamp_utc":"2026-04-05T22:10:00+00:00","payload":{"project_count":4,"decision_readiness_score":91.5,"platform_trust_score":83.0}}',
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    context = build_operational_context(settings)

    assert context["run_history"]["event_count"] == 2
    assert context["run_history"]["metric_deltas"]["decision_readiness_score"] == 2.5
    assert context["run_history"]["stability"] == "changing"
