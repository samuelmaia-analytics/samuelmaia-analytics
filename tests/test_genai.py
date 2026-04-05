from __future__ import annotations

from dataclasses import replace

from config.settings import get_settings
from core.ai import build_genai_suite
from core.genai import generate_insight


def test_genai_layer_returns_narrative() -> None:
    settings = get_settings()
    payload = generate_insight(
        {"decision_readiness_score": 90.0, "quality_pass_rate": 100.0, "platform_trust_score": 88.0},
        {"pass_rate": 100.0},
        settings.genai_prompt_path,
        settings.genai_provider,
        settings.genai_model,
    )
    assert "decision readiness score" in payload["narrative"].lower()
    assert payload["prompt_reference"] == "Narrative KPI Insights"
    assert payload["provider_status"] == "local_template"


def test_openai_compatible_provider_falls_back_without_connectivity() -> None:
    settings = replace(
        get_settings(),
        genai_provider="openai-compatible",
        genai_model="gpt-test",
        genai_base_url="http://127.0.0.1:9/v1",
        genai_api_key="fake-key",
        genai_timeout_seconds=1,
    )
    payload = build_genai_suite(
        settings=settings,
        projects=[],
        quality_report={"pass_rate": 100.0},
        semantic_metrics={
            "decision_readiness_score": 90.0,
            "quality_pass_rate": 100.0,
            "platform_trust_score": 88.0,
        },
        metric_catalog={"metrics": [], "dimensions": []},
        repository_registry=[],
        operational_context={
            "freshness": {"sources": {}, "artifacts": {}},
            "recent_events": [],
            "snapshot_history": {"project_change_summary": {"changes": []}},
            "lineage": {},
        },
    )
    assert payload["narrative_kpi_insights"]["provider_status"] == "remote_fallback"


def test_genai_suite_exposes_expected_use_cases() -> None:
    settings = get_settings()
    payload = build_genai_suite(
        settings=settings,
        projects=[{"project_name": "Revenue Intelligence Platform"}],
        quality_report={"pass_rate": 100.0},
        semantic_metrics={
            "decision_readiness_score": 90.0,
            "quality_pass_rate": 100.0,
            "platform_trust_score": 88.0,
        },
        metric_catalog={
            "definitions": [
                {
                    "name": "decision_readiness_score",
                    "owner": "analytics_platform",
                    "formula": "weighted composite",
                    "category": "executive",
                }
            ],
            "dimensions": ["domain"],
        },
        repository_registry=[{"repository": "tmp-revenue-intelligence-platform-suite"}],
        operational_context={
            "freshness": {"sources": {}, "artifacts": {"portfolio_snapshot": {"updated_at_utc": "2026-04-05T22:00:00+00:00"}}},
            "recent_events": [],
            "run_history": {
                "event_count": 2,
                "latest_timestamp_utc": "2026-04-05T22:10:00+00:00",
                "previous_timestamp_utc": "2026-04-05T22:00:00+00:00",
                "trend_summary": "Recent run history is changing: decision_readiness_score improved by 2.50.",
                "metric_deltas": {"decision_readiness_score": 2.5},
                "stability": "changing",
            },
            "snapshot_history": {
                "project_change_summary": {
                    "changes": [
                        {
                            "project_name": "Revenue Intelligence Platform",
                            "change_type": "changed",
                            "detail": "execution_score: 88.0 -> 91.0",
                        }
                    ]
                }
            },
            "lineage": {"portfolio_snapshot": ["raw_portfolio", "semantic_metrics_config"]},
        },
    )
    assert set(payload) == {
        "narrative_kpi_insights",
        "executive_summary",
        "anomaly_explanation_draft",
        "metric_definition_assistant",
        "business_glossary_explanation",
        "pipeline_dataset_description",
    }
    assert payload["metric_definition_assistant"]["provider_status"] == "local_template"
    assert "analytics_platform" in payload["metric_definition_assistant"]["narrative"]
    assert "recent run history" in payload["narrative_kpi_insights"]["narrative"].lower()
    assert "revenue intelligence platform changed" in payload["narrative_kpi_insights"]["narrative"].lower()
    assert "execution_score: 88.0 -> 91.0" in payload["executive_summary"]["narrative"]
