# Analytics Engineering Layer

This repository now includes a stronger dbt-inspired analytics engineering structure.
It is designed to work in two modes:

- `dbt-ready`: the folder layout, source definitions, model layers, tests, and docs follow a dbt-style operating model
- `dbt-like local runner`: the project can compile and validate the SQL graph against the local SQLite warehouse without requiring dbt-core in the environment

## Structure

```text
dbt/
  docs/                 business logic and lineage-oriented documentation
  models/
    raw/                source-facing pass-through models
    staging/            naming cleanup and semantic normalization
    intermediate/       reusable analytical transformations
    marts/              business-facing data products
  profiles/             example dbt profile
  tests/                SQL data tests
```

## Layer Intent

- `raw`: mirror the warehouse sources with minimal transformation
- `staging`: standardize names, booleans, score handling, and semantic consistency
- `intermediate`: reusable business logic that should not live directly in marts
- `marts`: decision-ready analytical outputs for executive and product consumption

## Local Validation

Run the canonical pipeline first:

```powershell
python -m core.pipeline
```

Then run the dbt-like validator:

```powershell
python -m core.analytics_engineering
```

This compiles the model graph, materializes temporary views in SQLite, and executes SQL data tests.

## If You Want Real dbt Later

The folder layout is already aligned for a future `dbt-core` setup.
To operationalize real dbt later, the next step is to add:

1. `dbt-core` and a SQLite-compatible adapter or warehouse adapter
2. CI commands for `dbt deps`, `dbt build`, and docs generation
3. production target profiles and environment-specific credentials
