from __future__ import annotations

from pathlib import Path

from config.settings import get_settings
from core.ai import build_genai_suite


def generate_insight(
    semantic_metrics: dict[str, float],
    quality_report: dict[str, object],
    prompt_path: Path,
    provider: str,
    model: str,
    base_url: str = "",
    api_key: str = "",
    timeout_seconds: int = 10,
    max_retries: int = 2,
) -> dict[str, str]:
    _ = (prompt_path, provider, model, base_url, api_key, timeout_seconds, max_retries)
    settings = get_settings()
    suite = build_genai_suite(
        settings=settings,
        projects=[],
        quality_report=dict(quality_report),
        semantic_metrics=semantic_metrics,
        metric_catalog={"metrics": [], "dimensions": []},
        repository_registry=[],
        operational_context={"freshness": {"sources": {}, "artifacts": {}}, "recent_events": [], "lineage": {}},
    )
    narrative = suite["narrative_kpi_insights"]
    return {
        "prompt_reference": str(narrative["prompt_reference"]),
        "narrative": str(narrative["narrative"]),
        "risk_note": str(narrative["bullets"][2]),
        "provider_status": str(narrative["provider_status"]),
    }
