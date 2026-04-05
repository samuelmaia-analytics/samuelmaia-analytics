from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from config.settings import Settings
from core.snapshot_history import summarize_snapshot_history
from core.trend_series import (
    build_domain_history_series,
    build_metric_history_series,
    build_project_change_summary,
    build_project_history_series,
    build_repository_change_summary,
)


def build_operational_context(settings: Settings) -> dict[str, Any]:
    source_assets = {
        "raw_portfolio": settings.raw_portfolio_path,
        "semantic_metrics_config": settings.semantic_metrics_path,
        "quality_rules_config": settings.quality_rules_path,
        "project_registry": settings.project_registry_path,
    }
    artifact_assets = {
        "portfolio_snapshot": settings.artifacts_dir / "portfolio_snapshot.json",
        "semantic_metrics_snapshot": settings.artifacts_dir / "semantic_metrics_snapshot.json",
        "repository_registry_snapshot": settings.artifacts_dir / "repository_registry_snapshot.json",
        "warehouse": settings.warehouse_path,
    }

    recent_events = _load_recent_events(settings.observability_dir / "events.jsonl")
    return {
        "freshness": {
            "sources": {name: _describe_asset(path) for name, path in source_assets.items()},
            "artifacts": {name: _describe_asset(path) for name, path in artifact_assets.items()},
        },
        "recent_events": recent_events,
        "run_history": _build_run_history(recent_events),
        "snapshot_history": {
            **summarize_snapshot_history(settings.artifacts_dir),
            "metric_history_series": build_metric_history_series(settings.artifacts_dir),
            "domain_history_series": build_domain_history_series(settings.artifacts_dir),
            "project_history_series": build_project_history_series(settings.artifacts_dir),
            "project_change_summary": build_project_change_summary(settings.artifacts_dir),
            "repository_change_summary": build_repository_change_summary(settings.artifacts_dir),
        },
        "lineage": {
            "portfolio_snapshot": [
                "raw_portfolio",
                "quality_rules_config",
                "semantic_metrics_config",
                "project_registry",
            ],
            "semantic_metrics_snapshot": [
                "raw_portfolio",
                "semantic_metrics_config",
                "quality_rules_config",
            ],
            "repository_registry_snapshot": ["project_registry"],
            "warehouse": [
                "portfolio_snapshot",
                "semantic_metrics_snapshot",
                "repository_registry_snapshot",
            ],
        },
    }


def _describe_asset(path: Path) -> dict[str, Any]:
    exists = path.exists()
    metadata: dict[str, Any] = {
        "path": str(path),
        "exists": exists,
        "updated_at_utc": None,
        "age_seconds": None,
        "size_bytes": None,
    }
    if not exists:
        return metadata

    stat = path.stat()
    updated_at = datetime.fromtimestamp(stat.st_mtime, tz=UTC)
    metadata["updated_at_utc"] = updated_at.isoformat()
    metadata["age_seconds"] = round((datetime.now(UTC) - updated_at).total_seconds(), 2)
    metadata["size_bytes"] = stat.st_size
    return metadata


def _load_recent_events(path: Path, limit: int = 5) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines()[-limit:]:
        line = line.strip()
        if not line:
            continue
        events.append(json.loads(line))
    return events


def _build_run_history(events: list[dict[str, Any]]) -> dict[str, Any]:
    snapshot_events = [event for event in events if event.get("event_name") == "portfolio_snapshot_built"]
    if not snapshot_events:
        return {
            "event_count": 0,
            "latest_timestamp_utc": None,
            "previous_timestamp_utc": None,
            "trend_summary": "No comparable run history available yet.",
            "metric_deltas": {},
            "stability": "unknown",
        }

    latest = snapshot_events[-1]
    previous = snapshot_events[-2] if len(snapshot_events) > 1 else None
    latest_payload = latest.get("payload", {})
    previous_payload = previous.get("payload", {}) if previous else {}

    metric_deltas: dict[str, float] = {}
    comparable_metrics = {
        key
        for key, value in latest_payload.items()
        if isinstance(value, (int, float)) and key != "project_count"
    }
    for metric_name in sorted(comparable_metrics):
        previous_value = previous_payload.get(metric_name)
        latest_value = latest_payload.get(metric_name)
        if isinstance(previous_value, (int, float)) and isinstance(latest_value, (int, float)):
            metric_deltas[metric_name] = round(float(latest_value) - float(previous_value), 2)

    stability = "stable"
    if any(abs(delta) >= 5 for delta in metric_deltas.values()):
        stability = "volatile"
    elif any(abs(delta) > 0 for delta in metric_deltas.values()):
        stability = "changing"

    return {
        "event_count": len(snapshot_events),
        "latest_timestamp_utc": latest.get("timestamp_utc"),
        "previous_timestamp_utc": previous.get("timestamp_utc") if previous else None,
        "trend_summary": _trend_summary(metric_deltas, stability),
        "metric_deltas": metric_deltas,
        "stability": stability,
    }


def _trend_summary(metric_deltas: dict[str, float], stability: str) -> str:
    if not metric_deltas:
        return "Only one comparable run is available, so no metric delta was calculated."
    directional = []
    for metric_name, delta in metric_deltas.items():
        if delta > 0:
            directional.append(f"{metric_name} improved by {delta:.2f}")
        elif delta < 0:
            directional.append(f"{metric_name} declined by {abs(delta):.2f}")
    if not directional:
        return "Recent runs are fully stable across tracked metrics."
    return f"Recent run history is {stability}: " + "; ".join(directional[:3]) + "."
