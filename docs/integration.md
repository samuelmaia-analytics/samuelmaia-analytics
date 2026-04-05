# Local Repository Integration

## Purpose

The root enterprise scaffold does not absorb the `tmp-*` repositories directly into the runtime core.
Instead, it integrates them selectively through a repository registry.

## How It Works

- `config/project_registry.json` declares which local repositories matter to the platform scaffold
- `core/repository_registry.py` resolves local paths and verifies that entrypoints exist
- the pipeline exposes this registry through artifacts, the API, and the Streamlit app

## Why This Matters

This keeps the root scaffold maintainable while still acknowledging the technical depth that already exists in the local reference repositories.
