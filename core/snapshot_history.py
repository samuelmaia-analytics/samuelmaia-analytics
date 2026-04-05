from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def persist_snapshot_history(snapshot: dict[str, Any], artifacts_dir: Path, timestamp_utc: str) -> Path:
    history_dir = artifacts_dir / "history"
    history_dir.mkdir(parents=True, exist_ok=True)
    timestamp = _sanitize_timestamp(timestamp_utc)
    output_path = history_dir / f"portfolio_snapshot_{timestamp}.json"
    output_path.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    return output_path


def load_recent_snapshot_history(artifacts_dir: Path, limit: int = 2) -> list[dict[str, Any]]:
    history_dir = artifacts_dir / "history"
    if not history_dir.exists():
        return []

    snapshots: list[dict[str, Any]] = []
    for path in sorted(history_dir.glob("portfolio_snapshot_*.json"))[-limit:]:
        payload = json.loads(path.read_text(encoding="utf-8"))
        snapshots.append({"path": str(path), "snapshot": payload})
    return snapshots


def summarize_snapshot_history(artifacts_dir: Path) -> dict[str, Any]:
    snapshots = load_recent_snapshot_history(artifacts_dir, limit=2)
    if not snapshots:
        return {
            "history_dir": str(artifacts_dir / "history"),
            "snapshot_count": 0,
            "latest_snapshot_path": None,
            "previous_snapshot_path": None,
            "comparison_summary": "No historical snapshots available yet.",
            "changes": {},
        }

    latest = snapshots[-1]
    previous = snapshots[-2] if len(snapshots) > 1 else None
    changes = _compare_snapshots(
        latest["snapshot"],
        previous["snapshot"] if previous else None,
    )
    return {
        "history_dir": str(artifacts_dir / "history"),
        "snapshot_count": len(list((artifacts_dir / "history").glob("portfolio_snapshot_*.json"))),
        "latest_snapshot_path": latest["path"],
        "previous_snapshot_path": previous["path"] if previous else None,
        "comparison_summary": _summarize_changes(changes),
        "changes": changes,
    }


def _compare_snapshots(latest: dict[str, Any], previous: dict[str, Any] | None) -> dict[str, Any]:
    if previous is None:
        return {
            "project_count_delta": 0,
            "quality_pass_rate_delta": 0.0,
            "metric_definition_count_delta": 0,
            "repository_count_delta": 0,
            "genai_use_case_count_delta": 0,
            "added_repositories": [],
            "removed_repositories": [],
        }

    latest_metric_defs = _metric_definitions(latest)
    previous_metric_defs = _metric_definitions(previous)
    latest_repo_ids = {item.get("id") for item in latest.get("repository_registry", [])}
    previous_repo_ids = {item.get("id") for item in previous.get("repository_registry", [])}
    latest_genai = latest.get("genai_outputs", {})
    previous_genai = previous.get("genai_outputs", {})

    latest_quality = latest.get("quality_report", {}).get("pass_rate", 0.0)
    previous_quality = previous.get("quality_report", {}).get("pass_rate", 0.0)

    return {
        "project_count_delta": len(latest.get("projects", [])) - len(previous.get("projects", [])),
        "quality_pass_rate_delta": round(float(latest_quality) - float(previous_quality), 2),
        "metric_definition_count_delta": len(latest_metric_defs) - len(previous_metric_defs),
        "repository_count_delta": len(latest_repo_ids) - len(previous_repo_ids),
        "genai_use_case_count_delta": len(latest_genai) - len(previous_genai),
        "added_repositories": sorted(str(item) for item in latest_repo_ids - previous_repo_ids if item),
        "removed_repositories": sorted(str(item) for item in previous_repo_ids - latest_repo_ids if item),
    }


def _metric_definitions(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    metric_catalog = snapshot.get("metric_catalog", {})
    definitions = metric_catalog.get("definitions")
    if isinstance(definitions, list):
        return definitions
    metrics = metric_catalog.get("metrics")
    if isinstance(metrics, list):
        return metrics
    return []


def _summarize_changes(changes: dict[str, Any]) -> str:
    signals: list[str] = []
    if changes["project_count_delta"]:
        signals.append(f"project count delta {changes['project_count_delta']}")
    if changes["quality_pass_rate_delta"]:
        direction = "improved" if changes["quality_pass_rate_delta"] > 0 else "declined"
        signals.append(f"quality pass rate {direction} by {abs(changes['quality_pass_rate_delta']):.2f}")
    if changes["metric_definition_count_delta"]:
        signals.append(f"metric definitions delta {changes['metric_definition_count_delta']}")
    if changes["repository_count_delta"]:
        signals.append(f"repository count delta {changes['repository_count_delta']}")
    if changes["genai_use_case_count_delta"]:
        signals.append(f"GenAI use case delta {changes['genai_use_case_count_delta']}")
    if changes["added_repositories"]:
        signals.append("added repositories: " + ", ".join(changes["added_repositories"][:3]))
    if changes["removed_repositories"]:
        signals.append("removed repositories: " + ", ".join(changes["removed_repositories"][:3]))
    if not signals:
        return "Latest snapshot is structurally stable versus the previous historical snapshot."
    return "Historical comparison shows " + "; ".join(signals) + "."


def _sanitize_timestamp(timestamp_utc: str) -> str:
    if timestamp_utc:
        return timestamp_utc.replace(":", "").replace("-", "").replace("+", "_").replace(".", "_")
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
