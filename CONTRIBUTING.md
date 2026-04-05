# Contributing

## Purpose

This repository is a portfolio platform and analytics scaffold.
Changes should improve business clarity, engineering quality, governance, or reviewability.

## Contribution Standard

Every meaningful change should preserve or improve:

- a canonical runtime path
- governed outputs and documented assumptions
- readability of the operating model
- testability and CI stability

## Local Validation

Run before opening a PR:

```powershell
python -m ruff check .
python -m pytest -q
python scripts/smoke_api.py
python scripts/smoke_streamlit.py
python -m core.cli analytics-checks
```

## Documentation Expectations

Update documentation when behavior changes in:

- `README.md` and `README.pt-BR.md` for user-facing positioning
- `docs/quickstart.md` for runtime or setup changes
- `docs/architecture.md` when operating model or structure changes
- contracts and governance docs when output shapes or policies change

## Pull Request Guidance

- keep scope coherent
- prefer incremental, reviewable changes
- document trade-offs explicitly
- avoid adding stack surface without clear business or architectural value
