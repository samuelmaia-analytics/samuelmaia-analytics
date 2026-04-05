select *
from {{ ref('stg_repository_registry') }}
where role not in ('flagship', 'core')
