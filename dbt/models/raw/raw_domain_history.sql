select
  timestamp_utc,
  snapshot_path,
  domain,
  governance_score,
  quality_score,
  execution_score,
  observability_score,
  project_count
from {{ source('portfolio_platform', 'domain_history') }}
