# Data Contracts

## Purpose

The root scaffold now validates its generated artifacts against versioned contracts.

## Current Contracts

- `contracts/v1/portfolio_snapshot.schema.json`
- `contracts/v1/semantic_metrics_snapshot.schema.json`

## Validation Surface

Contract validation runs inside `core/pipeline.py` before the pipeline completes successfully.
