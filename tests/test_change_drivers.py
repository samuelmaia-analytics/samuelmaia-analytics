from __future__ import annotations

from dataclasses import replace

from config.settings import get_settings
from core.change_drivers import build_change_drivers


def test_change_drivers_extracts_metric_and_project_signals() -> None:
    settings = replace(
        get_settings(),
        change_watch_threshold=1.0,
        change_material_threshold=3.0,
        change_critical_threshold=5.0,
    )
    payload = build_change_drivers(
        {
            "operational_context": {
                "run_history": {"stability": "changing", "metric_deltas": {"decision_readiness_score": 2.5}},
                "snapshot_history": {
                    "project_change_summary": {
                        "changes": [
                            {
                                "project_name": "Revenue Intelligence Platform",
                                "change_type": "changed",
                                "detail": "execution_score: 88.0 -> 91.0",
                            }
                        ]
                    },
                    "repository_change_summary": {"changes": []},
                },
            }
        },
        settings,
    )

    assert payload["drivers"][0]["driver_type"] == "metric"
    assert payload["drivers"][0]["materiality"] == "watch"
    assert payload["drivers"][1]["driver_type"] == "project"
    assert "Revenue Intelligence Platform" in payload["recommended_action"]
