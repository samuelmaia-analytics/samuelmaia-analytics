from __future__ import annotations

from config.settings import get_settings
from core.data_quality import run_quality_checks
from core.sample_data import load_portfolio_projects


def test_quality_report_has_expected_shape() -> None:
    settings = get_settings()
    projects = load_portfolio_projects(settings.raw_portfolio_path)
    report = run_quality_checks(projects, settings.quality_rules_path)
    assert report["total_checks"] > 0
    assert report["failed_checks"] == 0
    assert report["pass_rate"] == 100.0

