from __future__ import annotations

import json
from pathlib import Path

from core.models import PortfolioProject, QualityCheckResult


def run_quality_checks(projects: list[PortfolioProject], rules_path: Path) -> dict[str, object]:
    rules = json.loads(rules_path.read_text(encoding="utf-8"))
    score_min = rules["score_bounds"]["min"]
    score_max = rules["score_bounds"]["max"]
    results: list[QualityCheckResult] = []

    results.append(
        QualityCheckResult(
            rule="non_empty_dataset",
            status="pass" if projects else "fail",
            detail=f"projects={len(projects)}",
        )
    )

    for project in projects:
        for field_name in ("governance_score", "quality_score", "execution_score", "observability_score"):
            value = getattr(project, field_name)
            status = "pass" if score_min <= value <= score_max else "fail"
            results.append(
                QualityCheckResult(
                    rule=f"{project.project_name}:{field_name}",
                    status=status,
                    detail=f"value={value}",
                )
            )

    passed_checks = sum(1 for item in results if item.status == "pass")
    total_checks = len(results)
    return {
        "total_checks": total_checks,
        "passed_checks": passed_checks,
        "failed_checks": total_checks - passed_checks,
        "pass_rate": round((passed_checks / total_checks) * 100, 2) if total_checks else 0.0,
        "results": [item.__dict__ for item in results],
    }

