select
  domain,
  governance_score_avg,
  quality_score_avg,
  execution_score_avg,
  observability_score_avg,
  project_composite_score_avg,
  project_count
from {{ ref('int_domain_scores') }}
