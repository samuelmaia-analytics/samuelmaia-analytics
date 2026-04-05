select
  domain,
  round(avg(governance_score), 2) as governance_score_avg,
  round(avg(quality_score), 2) as quality_score_avg,
  round(avg(execution_score), 2) as execution_score_avg,
  round(avg(observability_score), 2) as observability_score_avg,
  round(avg(project_composite_score), 2) as project_composite_score_avg,
  count(*) as project_count
from {{ ref('int_project_scores') }}
group by domain
