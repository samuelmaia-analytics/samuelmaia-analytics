CREATE TABLE IF NOT EXISTS portfolio_projects (
    project_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    governance_score REAL NOT NULL,
    quality_score REAL NOT NULL,
    execution_score REAL NOT NULL,
    observability_score REAL NOT NULL
);

