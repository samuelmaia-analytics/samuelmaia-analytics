from __future__ import annotations

import json
from pathlib import Path

from core.models import PortfolioProject


def build_metric_catalog(
    projects: list[PortfolioProject],
    semantic_metrics: dict[str, float],
    metrics_path: Path,
) -> dict[str, object]:
    catalog = json.loads(metrics_path.read_text(encoding="utf-8"))
    domain_rollup: dict[str, dict[str, float]] = {}
    for project in projects:
        domain_rollup.setdefault(
            project.domain,
            {
                "governance_score": 0.0,
                "quality_score": 0.0,
                "execution_score": 0.0,
                "observability_score": 0.0,
                "project_count": 0.0,
            },
        )
        bucket = domain_rollup[project.domain]
        bucket["governance_score"] += project.governance_score
        bucket["quality_score"] += project.quality_score
        bucket["execution_score"] += project.execution_score
        bucket["observability_score"] += project.observability_score
        bucket["project_count"] += 1

    for bucket in domain_rollup.values():
        count = bucket["project_count"] or 1
        for field_name in ("governance_score", "quality_score", "execution_score", "observability_score"):
            bucket[field_name] = round(bucket[field_name] / count, 2)

    return {
        "definitions": catalog["metrics"],
        "dimensions": catalog.get("dimensions", []),
        "headline_metrics": semantic_metrics,
        "domain_rollup": domain_rollup,
    }


def export_metric_catalog(metric_catalog: dict[str, object], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(metric_catalog, indent=2), encoding="utf-8")

