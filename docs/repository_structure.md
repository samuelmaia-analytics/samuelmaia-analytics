# Repository Structure

## What Changed

The repository previously operated mainly as a portfolio hub plus local copies of supporting repositories.
It now also contains a dedicated enterprise scaffold at the root for maintainable analytical product development.

## Root Enterprise Scaffold

- `app/`: Streamlit app, pages, and UI primitives
- `assets/`: shared front-end styling
- `config/`: centralized configuration, metric definitions, quality rules, prompts
- `core/`: core logic and canonical pipeline
- `data/`: sample source data, processed artifacts, observability output
- `dbt/`: dbt-inspired analytics engineering layer with sources, models, tests, metrics, and lineage docs
- `services/`: FastAPI base
- `tests/`: core validation suite
- `.github/workflows/`: CI foundation

## Existing Portfolio Repositories

The `tmp-*` directories remain available as technical references and source material.
They are not the new primary application structure for the root repository.
