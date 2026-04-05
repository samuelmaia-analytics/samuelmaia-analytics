from __future__ import annotations

from pathlib import Path

from core.contracts import validate_contract


def test_snapshot_contract_accepts_minimal_valid_payload() -> None:
    schema_root = Path(__file__).resolve().parents[1] / "contracts" / "v1"
    payload = {
        "projects": [],
        "repository_registry": [],
        "quality_report": {},
        "semantic_metrics": {},
        "metric_catalog": {},
        "operational_context": {},
        "genai_outputs": {},
        "genai_insight": {},
        "change_drivers": {},
        "observability_event": {},
    }
    errors = validate_contract(payload, schema_root / "portfolio_snapshot.schema.json")
    assert errors == []


def test_semantic_metrics_contract_accepts_export_shape() -> None:
    schema_root = Path(__file__).resolve().parents[1] / "contracts" / "v1"
    payload = {
        "definitions": [],
        "dimensions": [],
        "headline_metrics": {},
        "domain_rollup": {},
    }
    errors = validate_contract(payload, schema_root / "semantic_metrics_snapshot.schema.json")
    assert errors == []
