select
  repository_id,
  title,
  role,
  readiness_score,
  readiness_status
from {{ ref('int_repository_health') }}
