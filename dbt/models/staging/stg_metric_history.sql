select
  timestamp_utc,
  snapshot_path,
  cast(decision_readiness_score as real) as decision_readiness_score,
  cast(quality_pass_rate as real) as quality_pass_rate,
  cast(platform_trust_score as real) as platform_trust_score,
  cast(governance_readiness_score as real) as governance_readiness_score,
  cast(observability_readiness_score as real) as observability_readiness_score
from {{ ref('raw_metric_history') }}
