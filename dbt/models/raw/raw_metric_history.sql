select
  timestamp_utc,
  snapshot_path,
  decision_readiness_score,
  quality_pass_rate,
  platform_trust_score,
  governance_readiness_score,
  observability_readiness_score
from {{ source('portfolio_platform', 'metric_history') }}
