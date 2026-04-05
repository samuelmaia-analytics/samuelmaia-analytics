from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PortfolioProject:
    project_name: str
    domain: str
    governance_score: float
    quality_score: float
    execution_score: float
    observability_score: float


@dataclass(frozen=True)
class QualityCheckResult:
    rule: str
    status: str
    detail: str

