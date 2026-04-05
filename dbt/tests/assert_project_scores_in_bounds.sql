select *
from {{ ref('stg_portfolio_projects') }}
where governance_score < 0
   or governance_score > 100
   or quality_score < 0
   or quality_score > 100
   or execution_score < 0
   or execution_score > 100
   or observability_score < 0
   or observability_score > 100
