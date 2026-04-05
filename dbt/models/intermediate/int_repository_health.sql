select
  repository_id,
  title,
  role,
  effective_readme_title,
  exists_locally_flag,
  entrypoint_exists_flag,
  (exists_locally_flag * 50) + (entrypoint_exists_flag * 50) as readiness_score,
  case
    when exists_locally_flag = 1 and entrypoint_exists_flag = 1 then 'ready'
    when exists_locally_flag = 1 then 'partial'
    else 'missing'
  end as readiness_status
from {{ ref('stg_repository_registry') }}
