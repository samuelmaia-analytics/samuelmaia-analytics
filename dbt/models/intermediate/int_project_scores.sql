select
  project_id,
  project_name,
  domain,
  governance_score,
  quality_score,
  execution_score,
  observability_score,
  round((governance_score + quality_score + execution_score + observability_score) / 4.0, 2) as project_composite_score,
  case
    when (governance_score + quality_score + execution_score + observability_score) / 4.0 >= 90 then 'leading'
    when (governance_score + quality_score + execution_score + observability_score) / 4.0 >= 80 then 'strong'
    else 'watch'
  end as project_health_band
from {{ ref('stg_portfolio_projects') }}
