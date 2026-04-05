from __future__ import annotations

import csv
from pathlib import Path

from core.models import PortfolioProject


def load_portfolio_projects(csv_path: Path) -> list[PortfolioProject]:
    with csv_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return [
            PortfolioProject(
                project_name=row["project_name"],
                domain=row["domain"],
                governance_score=float(row["governance_score"]),
                quality_score=float(row["quality_score"]),
                execution_score=float(row["execution_score"]),
                observability_score=float(row["observability_score"]),
            )
            for row in reader
        ]

