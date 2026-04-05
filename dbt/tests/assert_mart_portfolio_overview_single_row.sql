select *
from {{ ref('mart_portfolio_overview') }}
limit -1 offset 1
