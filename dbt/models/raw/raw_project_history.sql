select
  timestamp_utc,
  snapshot_path,
  project_name,
  domain,
  governance_score,
  quality_score,
  execution_score,
  observability_score
from {{ source('portfolio_platform', 'project_history') }}
