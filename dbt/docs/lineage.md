# Lineage

## Model Flow

```text
sources
  portfolio_projects
  repository_registry
  metric_history
  domain_history
  project_history

raw
  raw_portfolio_projects
  raw_repository_registry
  raw_metric_history
  raw_domain_history
  raw_project_history

staging
  stg_portfolio_projects
  stg_repository_registry
  stg_metric_history
  stg_domain_history
  stg_project_history

intermediate
  int_project_scores
  int_domain_scores
  int_repository_health
  int_latest_metric_status

marts
  mart_portfolio_scores
  mart_repository_readiness
  mart_portfolio_overview
```

## Consumption Intent

- dashboards and Streamlit pages should prefer marts
- cross-cutting business logic should live in intermediate models
- sources and raw models should remain close to the warehouse shape
- staging is responsible for semantic consistency and naming discipline
