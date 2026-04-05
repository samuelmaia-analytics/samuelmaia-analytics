select
  id,
  title,
  role,
  resolved_path,
  exists_locally,
  entrypoint_exists,
  readme_title
from {{ source('portfolio_platform', 'repository_registry') }}
