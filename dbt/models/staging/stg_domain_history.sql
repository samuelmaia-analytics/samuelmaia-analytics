select
  timestamp_utc,
  snapshot_path,
  domain,
  cast(governance_score as real) as governance_score,
  cast(quality_score as real) as quality_score,
  cast(execution_score as real) as execution_score,
  cast(observability_score as real) as observability_score,
  cast(project_count as real) as project_count
from {{ ref('raw_domain_history') }}
