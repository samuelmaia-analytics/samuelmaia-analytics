select
  lower(replace(project_name, ' ', '_')) as project_id,
  project_name,
  domain,
  cast(governance_score as real) as governance_score,
  cast(quality_score as real) as quality_score,
  cast(execution_score as real) as execution_score,
  cast(observability_score as real) as observability_score
from {{ ref('raw_portfolio_projects') }}
