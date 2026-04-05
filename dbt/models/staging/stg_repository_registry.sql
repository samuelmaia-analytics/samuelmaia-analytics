select
  id as repository_id,
  title,
  role,
  resolved_path,
  cast(exists_locally as integer) as exists_locally_flag,
  cast(entrypoint_exists as integer) as entrypoint_exists_flag,
  coalesce(readme_title, title) as effective_readme_title
from {{ ref('raw_repository_registry') }}
