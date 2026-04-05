from __future__ import annotations

import json
from pathlib import Path

from core.models import PortfolioProject


def compute_semantic_metrics(
    projects: list[PortfolioProject],
    quality_report: dict[str, object],
    metrics_path: Path,
) -> dict[str, float]:
    _ = json.loads(metrics_path.read_text(encoding="utf-8"))
    if not projects:
        return {
            "decision_readiness_score": 0.0,
            "quality_pass_rate": 0.0,
            "platform_trust_score": 0.0,
            "governance_readiness_score": 0.0,
            "observability_readiness_score": 0.0,
        }

    governance_score = sum(item.governance_score for item in projects) / len(projects)
    execution_score = sum(item.execution_score for item in projects) / len(projects)
    observability_score = sum(item.observability_score for item in projects) / len(projects)
    quality_pass_rate = float(quality_report["pass_rate"])
    decision_readiness_score = 0.35 * governance_score + 0.35 * quality_pass_rate + 0.30 * execution_score
    platform_trust_score = 0.5 * governance_score + 0.5 * observability_score
    return {
        "decision_readiness_score": round(decision_readiness_score, 2),
        "quality_pass_rate": round(quality_pass_rate, 2),
        "platform_trust_score": round(platform_trust_score, 2),
        "governance_readiness_score": round(governance_score, 2),
        "observability_readiness_score": round(observability_score, 2),
    }
