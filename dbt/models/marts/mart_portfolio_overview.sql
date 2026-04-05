select
  metrics.timestamp_utc,
  metrics.decision_readiness_score,
  metrics.quality_pass_rate,
  metrics.platform_trust_score,
  metrics.governance_readiness_score,
  metrics.observability_readiness_score,
  (select count(*) from {{ ref('int_project_scores') }}) as project_count,
  (select count(*) from {{ ref('int_repository_health') }} where readiness_status = 'ready') as ready_repository_count
from {{ ref('int_latest_metric_status') }} as metrics
