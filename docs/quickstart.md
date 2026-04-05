# Quickstart

## Install

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

## Run the Canonical Pipeline

```powershell
python -m core.pipeline
```

Generated outputs:

- `data/processed/portfolio_snapshot.json`
- `data/processed/semantic_metrics_snapshot.json`
- `data/warehouse/portfolio_platform.db`

## Run the API

```powershell
python -m uvicorn services.api.main:app --reload
```

Protected endpoints require:

`X-API-Key: portfolio-demo-key`

## Run the Streamlit App

```powershell
streamlit run streamlit_app.py
```

## Run Tests

```powershell
python -m pytest -q
```

## Run Smoke Checks

```powershell
python scripts/smoke_api.py
python scripts/smoke_streamlit.py
```

## Run the Operational CLI

```powershell
python -m core.cli health
python -m core.cli analytics-checks
python -m core.cli policy-checks
python -m core.cli validate
python -m core.cli snapshot
python -m core.cli sync-registry
python -m core.cli export --output tmp\snapshot.json
```

## Optional JWT Mode

If you want bearer-token auth instead of API key auth for protected endpoints:

```powershell
$env:PORTFOLIO_JWT_ENABLED="true"
$env:PORTFOLIO_JWT_SECRET="replace-with-a-32-char-minimum-secret"
```

The JWT secret must be at least 32 characters.

## Optional GenAI Provider Mode

The default provider is deterministic and local. To connect an external LLM later:

```powershell
$env:PORTFOLIO_GENAI_PROVIDER="openai-compatible"
$env:PORTFOLIO_GENAI_MODEL="gpt-4.1-mini"
$env:PORTFOLIO_GENAI_BASE_URL="https://api.openai.com/v1"
$env:PORTFOLIO_GENAI_API_KEY="your-api-key"
```

See `docs/genai_analytics.md` for the provider contract and operating model.

## Change Driver Thresholds

Change-driver materiality is configurable through environment variables:

```powershell
$env:PORTFOLIO_CHANGE_WATCH_THRESHOLD="1.0"
$env:PORTFOLIO_CHANGE_MATERIAL_THRESHOLD="3.0"
$env:PORTFOLIO_CHANGE_CRITICAL_THRESHOLD="5.0"
```

These thresholds classify portfolio movement as `watch`, `material`, or `critical` across metric, project, and repository drivers.

The current sanitized runtime configuration can be reviewed in:

- Streamlit: `Governance and Quality`
- API: `GET /governance/runtime-config`

Data governance and LGPD baseline are documented in:

- `config/data_governance.json`
- `docs/governance_lgpd.md`

Governance policy validation is also available in:

- CLI: `python -m core.cli policy-checks`
- API: `GET /governance/policy-checks`

Analytics-engineering validation is also available in:

- CLI: `python -m core.cli analytics-checks`
- API: `GET /governance/analytics-engineering`
- Streamlit: `Governance and Quality`

Additional operating references:

- `docs/api.md`
- `docs/business-case.md`
- `docs/metric-layer.md`
- `docs/data-governance.md`
- `docs/data-quality.md`
- `docs/roadmap.md`

## Analytics Engineering Layer

The repository includes a dbt-inspired structure under `dbt/` with:

- `raw`, `staging`, `intermediate`, and `marts`
- source definitions
- schema and data tests
- a metric layer
- business logic and lineage docs

You can validate the local SQLite warehouse without installing dbt by running:

```powershell
python -m core.cli analytics-checks
```
