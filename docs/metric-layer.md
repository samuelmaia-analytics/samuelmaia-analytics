# Metric Layer

## Intent

The root scaffold uses a semantic metric layer so the same KPI logic can be reused in API, app, warehouse, contracts, and documentation.

## Current Headline Metrics

- `decision_readiness_score`
- `quality_pass_rate`
- `platform_trust_score`
- `governance_readiness_score`
- `observability_readiness_score`

## Sources of Truth

- definitions: `config/semantic_metrics.json`
- computation: `core/semantic_metrics.py`
- catalog export: `core/metric_catalog.py`
- warehouse validation: `dbt/` and `core/analytics_engineering.py`
