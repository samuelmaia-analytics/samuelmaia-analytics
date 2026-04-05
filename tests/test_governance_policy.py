from __future__ import annotations

from dataclasses import replace

from config.settings import get_settings
from core.governance_policy import build_governance_policy_report


def test_governance_policy_report_passes_for_default_settings() -> None:
    report = build_governance_policy_report(get_settings())
    assert report["status"] in {"ok", "warn"}
    assert len(report["checks"]) == 3


def test_governance_policy_report_fails_on_threshold_order() -> None:
    settings = replace(
        get_settings(),
        change_watch_threshold=4.0,
        change_material_threshold=3.0,
        change_critical_threshold=2.0,
    )
    report = build_governance_policy_report(settings)
    assert report["status"] == "fail"
    assert report["checks"][0]["status"] == "fail"
