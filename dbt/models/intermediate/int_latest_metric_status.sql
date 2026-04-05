select
  timestamp_utc,
  decision_readiness_score,
  quality_pass_rate,
  platform_trust_score,
  governance_readiness_score,
  observability_readiness_score
from {{ ref('stg_metric_history') }}
order by timestamp_utc desc
limit 1
