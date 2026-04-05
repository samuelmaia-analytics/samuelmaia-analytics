# SQL Assets

## Purpose

The scaffold exports portfolio metadata into SQLite so that downstream SQL, BI, and dbt-style consumption can start from a governed local warehouse.

## Structure

- `ddl/`: warehouse object definitions
- `analytics/`: downstream analytical queries

## Warehouse

Default path:

`data/warehouse/portfolio_platform.db`

