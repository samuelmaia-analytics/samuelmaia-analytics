# Enterprise Scaffold Architecture

## Intent

This repository now includes an enterprise-style platform scaffold at the root.
The goal is to provide a maintainable base for analytics products while keeping the existing portfolio repositories available as reference implementations.

## Top-Level Structure

```text
app/        Streamlit presentation layer
assets/     styling and visual assets
config/     centralized settings, rules, prompts, and semantic metric definitions
core/       domain logic, pipeline orchestration, quality, metrics, GenAI, observability
data/       raw sample inputs, processed outputs, and observability logs
docs/       architecture and operating documentation
services/   FastAPI service layer
tests/      automated validation for the core platform scaffold
```

## Design Principles

- keep business and pipeline logic in `core/`
- keep app and service layers thin
- centralize settings and runtime file paths under `config/`
- make data quality, semantic metrics, GenAI insights, and observability first-class platform capabilities
- keep the scaffold inspectable and easy to extend into a fuller product

## Delivery Surfaces

- `streamlit_app.py`: canonical Streamlit entrypoint
- `pages/`: canonical Streamlit multipage views
- `app/streamlit_app.py`: compatibility wrapper for the legacy app path
- `services/api/main.py`: FastAPI base with health, snapshot, metrics, and insights endpoints
- `core/pipeline.py`: orchestrates the canonical snapshot build
- `scripts/smoke_api.py`: executable API smoke validation
- `scripts/smoke_streamlit.py`: executable Streamlit smoke validation

## Platform Capabilities

- `core/data_quality.py`: governed quality checks
- `core/semantic_metrics.py` and `core/metric_catalog.py`: semantic metric computation and export
- `core/ai/`: analytics-oriented GenAI capability layer with prompt pack, provider abstraction, and typed artifacts
- `core/observability.py`: structured event emission
- `core/change_drivers.py`: configurable materiality classification for executive change monitoring
- `core/runtime_config.py`: sanitized runtime configuration summary for governance review
- `core/governance_policy.py`: runtime policy checks for thresholds, auth, and GenAI readiness
- `core/analytics_engineering.py`: dbt-like local compiler and SQL test runner over the SQLite warehouse
- `core/repository_registry.py`: selective integration of local `tmp-*` repositories as reference assets
- `contracts/v1/`: versioned JSON schema contracts for generated artifacts
- `core/writeback.py`: SQLite warehouse export for SQL and dbt-ready consumption

## Recommended Next Extensions

1. expand the GenAI layer with richer context sources and approval workflows
2. add richer semantic metrics catalogs and dbt-compatible metric exports
3. add warehouse adapters and stronger artifact contracts
4. expand CI with smoke tests for Streamlit and API
