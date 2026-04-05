from __future__ import annotations

import sqlite3
from pathlib import Path

from core.trend_series import build_domain_history_series, build_metric_history_series, build_project_history_series


def write_sqlite_exports(snapshot: dict[str, object], warehouse_path: Path) -> None:
    warehouse_path.parent.mkdir(parents=True, exist_ok=True)
    projects = snapshot["projects"]
    registry = snapshot["repository_registry"]
    artifacts_dir = Path(snapshot["operational_context"]["freshness"]["artifacts"]["portfolio_snapshot"]["path"]).parent
    metric_history = build_metric_history_series(artifacts_dir)
    domain_history = build_domain_history_series(artifacts_dir)
    project_history = build_project_history_series(artifacts_dir)

    with sqlite3.connect(warehouse_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS portfolio_projects (
                project_name TEXT NOT NULL,
                domain TEXT NOT NULL,
                governance_score REAL NOT NULL,
                quality_score REAL NOT NULL,
                execution_score REAL NOT NULL,
                observability_score REAL NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS repository_registry (
                id TEXT NOT NULL,
                title TEXT NOT NULL,
                role TEXT NOT NULL,
                resolved_path TEXT NOT NULL,
                exists_locally INTEGER NOT NULL,
                entrypoint_exists INTEGER NOT NULL,
                readme_title TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS metric_history (
                timestamp_utc TEXT NOT NULL,
                snapshot_path TEXT NOT NULL,
                decision_readiness_score REAL,
                quality_pass_rate REAL,
                platform_trust_score REAL,
                governance_readiness_score REAL,
                observability_readiness_score REAL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS domain_history (
                timestamp_utc TEXT NOT NULL,
                snapshot_path TEXT NOT NULL,
                domain TEXT NOT NULL,
                governance_score REAL,
                quality_score REAL,
                execution_score REAL,
                observability_score REAL,
                project_count REAL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS project_history (
                timestamp_utc TEXT NOT NULL,
                snapshot_path TEXT NOT NULL,
                project_name TEXT NOT NULL,
                domain TEXT NOT NULL,
                governance_score REAL,
                quality_score REAL,
                execution_score REAL,
                observability_score REAL
            )
            """
        )
        conn.execute("DELETE FROM portfolio_projects")
        conn.execute("DELETE FROM repository_registry")
        conn.execute("DELETE FROM metric_history")
        conn.execute("DELETE FROM domain_history")
        conn.execute("DELETE FROM project_history")
        conn.executemany(
            """
            INSERT INTO portfolio_projects (
                project_name, domain, governance_score, quality_score, execution_score, observability_score
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    item["project_name"],
                    item["domain"],
                    item["governance_score"],
                    item["quality_score"],
                    item["execution_score"],
                    item["observability_score"],
                )
                for item in projects
            ],
        )
        conn.executemany(
            """
            INSERT INTO repository_registry (
                id, title, role, resolved_path, exists_locally, entrypoint_exists, readme_title
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    item["id"],
                    item["title"],
                    item["role"],
                    item["resolved_path"],
                    1 if item["exists_locally"] else 0,
                    1 if item["entrypoint_exists"] else 0,
                    item.get("readme_title"),
                )
                for item in registry
            ],
        )
        conn.executemany(
            """
            INSERT INTO metric_history (
                timestamp_utc,
                snapshot_path,
                decision_readiness_score,
                quality_pass_rate,
                platform_trust_score,
                governance_readiness_score,
                observability_readiness_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    item["timestamp_utc"],
                    item["snapshot_path"],
                    item["decision_readiness_score"],
                    item["quality_pass_rate"],
                    item["platform_trust_score"],
                    item["governance_readiness_score"],
                    item["observability_readiness_score"],
                )
                for item in metric_history
                if item["timestamp_utc"]
            ],
        )
        conn.executemany(
            """
            INSERT INTO domain_history (
                timestamp_utc,
                snapshot_path,
                domain,
                governance_score,
                quality_score,
                execution_score,
                observability_score,
                project_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    item["timestamp_utc"],
                    item["snapshot_path"],
                    item["domain"],
                    item["governance_score"],
                    item["quality_score"],
                    item["execution_score"],
                    item["observability_score"],
                    item["project_count"],
                )
                for item in domain_history
                if item["timestamp_utc"]
            ],
        )
        conn.executemany(
            """
            INSERT INTO project_history (
                timestamp_utc,
                snapshot_path,
                project_name,
                domain,
                governance_score,
                quality_score,
                execution_score,
                observability_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    item["timestamp_utc"],
                    item["snapshot_path"],
                    item["project_name"],
                    item["domain"],
                    item["governance_score"],
                    item["quality_score"],
                    item["execution_score"],
                    item["observability_score"],
                )
                for item in project_history
                if item["timestamp_utc"] and item["project_name"] and item["domain"]
            ],
        )
        conn.execute(
            """
            CREATE VIEW IF NOT EXISTS v_portfolio_scores AS
            SELECT
                domain,
                AVG(governance_score) AS governance_score_avg,
                AVG(quality_score) AS quality_score_avg,
                AVG(execution_score) AS execution_score_avg,
                AVG(observability_score) AS observability_score_avg
            FROM portfolio_projects
            GROUP BY domain
            """
        )
        conn.execute(
            """
            CREATE VIEW IF NOT EXISTS v_metric_history_latest AS
            SELECT
                timestamp_utc,
                decision_readiness_score,
                quality_pass_rate,
                platform_trust_score,
                governance_readiness_score,
                observability_readiness_score
            FROM metric_history
            ORDER BY timestamp_utc DESC
            """
        )
        conn.execute(
            """
            CREATE VIEW IF NOT EXISTS v_domain_history_latest AS
            SELECT
                timestamp_utc,
                domain,
                governance_score,
                quality_score,
                execution_score,
                observability_score,
                project_count
            FROM domain_history
            ORDER BY timestamp_utc DESC, domain ASC
            """
        )
        conn.execute(
            """
            CREATE VIEW IF NOT EXISTS v_project_history_latest AS
            SELECT
                timestamp_utc,
                project_name,
                domain,
                governance_score,
                quality_score,
                execution_score,
                observability_score
            FROM project_history
            ORDER BY timestamp_utc DESC, project_name ASC
            """
        )
