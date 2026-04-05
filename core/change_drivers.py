from __future__ import annotations

from typing import Any

from config.settings import Settings


def build_change_drivers(snapshot: dict[str, Any], settings: Settings) -> dict[str, Any]:
    operational = snapshot.get("operational_context", {})
    snapshot_history = operational.get("snapshot_history", {})
    run_history = operational.get("run_history", {})

    project_changes = snapshot_history.get("project_change_summary", {}).get("changes", [])
    repository_changes = snapshot_history.get("repository_change_summary", {}).get("changes", [])
    metric_deltas = run_history.get("metric_deltas", {})

    primary_metric_driver = _primary_metric_driver(metric_deltas, settings)
    primary_project_driver = _first_change(project_changes, settings)
    primary_repository_driver = _first_change(repository_changes, settings)

    drivers = []
    if primary_metric_driver:
        drivers.append(primary_metric_driver)
    if primary_project_driver:
        drivers.append(primary_project_driver)
    if primary_repository_driver:
        drivers.append(primary_repository_driver)

    summary = "No major change driver detected across the latest historical comparison."
    if drivers:
        summary = "Primary change drivers were identified across metrics, projects, or repository surface."

    return {
        "summary": summary,
        "drivers": drivers,
        "recommended_action": _recommended_action(run_history, project_changes, repository_changes, drivers),
    }


def _primary_metric_driver(metric_deltas: dict[str, float], settings: Settings) -> dict[str, Any] | None:
    non_zero = [(name, delta) for name, delta in metric_deltas.items() if delta]
    if not non_zero:
        return None
    metric_name, delta = max(non_zero, key=lambda item: abs(item[1]))
    direction = "improved" if delta > 0 else "declined"
    materiality = _classify_materiality(abs(delta), settings)
    return {
        "driver_type": "metric",
        "name": metric_name,
        "impact": direction,
        "detail": f"{metric_name} {direction} by {abs(delta):.2f}.",
        "materiality": materiality,
    }


def _first_change(changes: list[dict[str, Any]], settings: Settings) -> dict[str, Any] | None:
    if not changes:
        return None
    item = changes[0]
    name = item.get("project_name") or item.get("id") or "unknown"
    kind = "project" if "project_name" in item else "repository"
    materiality = _materiality_from_change(item, settings)
    return {
        "driver_type": kind,
        "name": name,
        "impact": item.get("change_type", "changed"),
        "detail": item.get("detail", ""),
        "materiality": materiality,
    }


def _recommended_action(
    run_history: dict[str, Any],
    project_changes: list[dict[str, Any]],
    repository_changes: list[dict[str, Any]],
    drivers: list[dict[str, Any]],
) -> str:
    stability = run_history.get("stability", "unknown")
    highest_materiality = _highest_materiality(drivers)
    primary_project_name = project_changes[0].get("project_name") if project_changes else None
    if highest_materiality == "critical":
        return "Critical movement detected. Review metric deltas, impacted projects, and downstream stakeholder surfaces immediately."
    if highest_materiality == "material":
        if primary_project_name:
            return f"Material movement detected. Validate {primary_project_name} as the main project-level contributor and confirm whether downstream consumers should be notified."
        return "Material movement detected. Validate the main project-level contributor and confirm whether downstream consumers should be notified."
    if stability == "volatile":
        return "Review the latest metric deltas and validate which project-level changes drove the volatility."
    if project_changes:
        first = project_changes[0]
        return f"Inspect project-level change for {first.get('project_name', 'unknown project')} before wider escalation."
    if repository_changes:
        first = repository_changes[0]
        return f"Inspect repository-level change for {first.get('id', 'unknown repository')} to confirm metadata drift."
    return "Continue monitoring historical snapshots and validate changes against business-facing outputs."


def _classify_materiality(delta: float, settings: Settings) -> str:
    if delta >= settings.change_critical_threshold:
        return "critical"
    if delta >= settings.change_material_threshold:
        return "material"
    if delta >= settings.change_watch_threshold:
        return "watch"
    return "stable"


def _materiality_from_change(change: dict[str, Any], settings: Settings) -> str:
    detail = str(change.get("detail", ""))
    if change.get("change_type") in {"added", "removed"}:
        return "material"
    import re

    numbers = [float(match) for match in re.findall(r"-?\d+(?:\.\d+)?", detail)]
    if len(numbers) >= 2:
        return _classify_materiality(abs(numbers[-1] - numbers[-2]), settings)
    return "watch"


def _highest_materiality(drivers: list[dict[str, Any]]) -> str:
    rank = {"stable": 0, "watch": 1, "material": 2, "critical": 3}
    highest = "stable"
    for driver in drivers:
        level = str(driver.get("materiality", "stable"))
        if rank.get(level, 0) > rank[highest]:
            highest = level
    return highest
