from __future__ import annotations

from typing import Any

from core.snapshot_history import load_recent_snapshot_history


def build_metric_history_series(artifacts_dir, limit: int = 20) -> list[dict[str, Any]]:
    history = load_recent_snapshot_history(artifacts_dir, limit=limit)
    series: list[dict[str, Any]] = []
    for item in history:
        snapshot = item["snapshot"]
        observability_event = snapshot.get("observability_event", {})
        semantic_metrics = snapshot.get("semantic_metrics", {})
        series.append(
            {
                "snapshot_path": item["path"],
                "timestamp_utc": observability_event.get("timestamp_utc"),
                "decision_readiness_score": semantic_metrics.get("decision_readiness_score"),
                "quality_pass_rate": semantic_metrics.get("quality_pass_rate"),
                "platform_trust_score": semantic_metrics.get("platform_trust_score"),
                "governance_readiness_score": semantic_metrics.get("governance_readiness_score"),
                "observability_readiness_score": semantic_metrics.get("observability_readiness_score"),
            }
        )
    return series


def build_domain_history_series(artifacts_dir, limit: int = 20) -> list[dict[str, Any]]:
    history = load_recent_snapshot_history(artifacts_dir, limit=limit)
    rows: list[dict[str, Any]] = []
    for item in history:
        snapshot = item["snapshot"]
        timestamp_utc = snapshot.get("observability_event", {}).get("timestamp_utc")
        for domain, metrics in snapshot.get("metric_catalog", {}).get("domain_rollup", {}).items():
            rows.append(
                {
                    "snapshot_path": item["path"],
                    "timestamp_utc": timestamp_utc,
                    "domain": domain,
                    "governance_score": metrics.get("governance_score"),
                    "quality_score": metrics.get("quality_score"),
                    "execution_score": metrics.get("execution_score"),
                    "observability_score": metrics.get("observability_score"),
                    "project_count": metrics.get("project_count"),
                }
            )
    return rows


def build_project_history_series(artifacts_dir, limit: int = 20) -> list[dict[str, Any]]:
    history = load_recent_snapshot_history(artifacts_dir, limit=limit)
    rows: list[dict[str, Any]] = []
    for item in history:
        snapshot = item["snapshot"]
        timestamp_utc = snapshot.get("observability_event", {}).get("timestamp_utc")
        for project in snapshot.get("projects", []):
            rows.append(
                {
                    "snapshot_path": item["path"],
                    "timestamp_utc": timestamp_utc,
                    "project_name": project.get("project_name"),
                    "domain": project.get("domain"),
                    "governance_score": project.get("governance_score"),
                    "quality_score": project.get("quality_score"),
                    "execution_score": project.get("execution_score"),
                    "observability_score": project.get("observability_score"),
                }
            )
    return rows


def build_project_change_summary(artifacts_dir, limit: int = 2) -> dict[str, Any]:
    history = load_recent_snapshot_history(artifacts_dir, limit=limit)
    if len(history) < 2:
        return {
            "summary": "No prior project snapshot available for comparison.",
            "changes": [],
        }

    latest = {item.get("project_name"): item for item in history[-1]["snapshot"].get("projects", [])}
    previous = {item.get("project_name"): item for item in history[-2]["snapshot"].get("projects", [])}

    changes: list[dict[str, Any]] = []
    for project_name in sorted(set(latest) | set(previous)):
        latest_project = latest.get(project_name)
        previous_project = previous.get(project_name)
        if previous_project is None:
            changes.append({"project_name": project_name, "change_type": "added", "detail": "Project appeared in latest snapshot."})
            continue
        if latest_project is None:
            changes.append({"project_name": project_name, "change_type": "removed", "detail": "Project missing from latest snapshot."})
            continue

        deltas = []
        for field in ("governance_score", "quality_score", "execution_score", "observability_score"):
            latest_value = latest_project.get(field)
            previous_value = previous_project.get(field)
            if latest_value != previous_value:
                deltas.append(f"{field}: {previous_value} -> {latest_value}")
        if deltas:
            changes.append({"project_name": project_name, "change_type": "changed", "detail": "; ".join(deltas)})

    summary = "Project-level portfolio surface is stable across the last two snapshots."
    if changes:
        summary = "Project-level comparison detected changes in the latest snapshot."
    return {
        "summary": summary,
        "changes": changes,
    }


def build_repository_change_summary(artifacts_dir, limit: int = 2) -> dict[str, Any]:
    history = load_recent_snapshot_history(artifacts_dir, limit=limit)
    if len(history) < 2:
        return {
            "summary": "No prior repository snapshot available for comparison.",
            "changes": [],
        }

    latest = history[-1]["snapshot"]
    previous = history[-2]["snapshot"]
    latest_map = {item.get("id"): item for item in latest.get("repository_registry", [])}
    previous_map = {item.get("id"): item for item in previous.get("repository_registry", [])}

    changes: list[dict[str, Any]] = []
    for repo_id in sorted(set(latest_map) | set(previous_map)):
        latest_repo = latest_map.get(repo_id, {})
        previous_repo = previous_map.get(repo_id, {})
        if not previous_repo:
            changes.append({"id": repo_id, "change_type": "added", "detail": "Repository appeared in latest snapshot."})
            continue
        if not latest_repo:
            changes.append({"id": repo_id, "change_type": "removed", "detail": "Repository missing from latest snapshot."})
            continue

        deltas = []
        for field in ("markdown_files", "python_files", "tests_present", "exists_locally", "entrypoint_exists"):
            if latest_repo.get(field) != previous_repo.get(field):
                deltas.append(f"{field}: {previous_repo.get(field)} -> {latest_repo.get(field)}")
        if deltas:
            changes.append({"id": repo_id, "change_type": "changed", "detail": "; ".join(deltas)})

    summary = "Repository surface is stable across the last two snapshots."
    if changes:
        summary = "Repository comparison detected changes in the latest snapshot."
    return {
        "summary": summary,
        "changes": changes,
    }
