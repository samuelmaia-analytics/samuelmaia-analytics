# Business Logic

## Decision Logic

The analytics engineering layer separates source mirroring, semantic cleanup, reusable scoring logic, and business-facing marts.

### Project Composite Score

`int_project_scores` computes a composite score from:

- governance score
- quality score
- execution score
- observability score

This score is designed to answer a business question:
which analytical assets are most decision-ready and operationally trustworthy?

### Repository Readiness

`int_repository_health` classifies local reference repositories into:

- `ready`
- `partial`
- `missing`

This makes maintainability visible as a portfolio capability, not only as repo metadata.

### Marts

- `mart_portfolio_scores`: domain-level rollup for BI and leadership review
- `mart_repository_readiness`: governance-facing view of repository readiness
- `mart_portfolio_overview`: latest one-row executive overview for APIs and dashboards
