SELECT
    domain,
    AVG(governance_score) AS governance_score_avg,
    AVG(quality_score) AS quality_score_avg,
    AVG(execution_score) AS execution_score_avg,
    AVG(observability_score) AS observability_score_avg
FROM portfolio_projects
GROUP BY domain
ORDER BY governance_score_avg DESC;

