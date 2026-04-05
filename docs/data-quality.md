# Data Quality

## Purpose

The platform exposes quality as a first-class operating signal rather than a hidden implementation detail.

## Current Quality Surface

- required columns and score bounds in `config/quality_rules.json`
- governed checks in `core/data_quality.py`
- quality report embedded in the canonical snapshot
- visibility in Streamlit, API, and contracts

## Why It Matters

Quality affects whether an analytical output should be trusted for business review.
That is why quality is part of runtime summaries, decision readiness, and governance surfaces.
