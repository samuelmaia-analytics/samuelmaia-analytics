from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from config.settings import Settings, get_settings


@dataclass(frozen=True)
class ModelSpec:
    name: str
    layer: str
    path: Path


LAYER_ORDER = ("raw", "staging", "intermediate", "marts")


def run_analytics_engineering_checks(settings: Settings) -> dict[str, Any]:
    model_specs = _discover_models(settings)
    test_files = sorted((settings.data_dir.parents[0] / "dbt" / "tests").glob("*.sql"))
    results: list[dict[str, Any]] = []

    with sqlite3.connect(settings.warehouse_path) as conn:
        _materialize_models(conn, model_specs)
        for test_file in test_files:
            sql = _compile_sql(test_file.read_text(encoding="utf-8"))
            rows = conn.execute(sql).fetchall()
            results.append(
                {
                    "test": test_file.stem,
                    "status": "pass" if not rows else "fail",
                    "failure_count": len(rows),
                }
            )

    failed = [item for item in results if item["status"] == "fail"]
    return {
        "status": "ok" if not failed else "fail",
        "models_built": len(model_specs),
        "tests_run": len(results),
        "failed_tests": len(failed),
        "results": results,
    }


def _discover_models(settings: Settings) -> list[ModelSpec]:
    dbt_models_root = settings.data_dir.parents[0] / "dbt" / "models"
    specs: list[ModelSpec] = []
    for layer in LAYER_ORDER:
        layer_dir = dbt_models_root / layer
        for path in sorted(layer_dir.glob("*.sql")):
            specs.append(ModelSpec(name=path.stem, layer=layer, path=path))
    return specs


def _materialize_models(conn: sqlite3.Connection, specs: list[ModelSpec]) -> None:
    for spec in specs:
        sql = _compile_sql(spec.path.read_text(encoding="utf-8"))
        conn.execute(f"drop view if exists {spec.name}")
        conn.execute(f"create temp view {spec.name} as {sql}")


def _compile_sql(sql: str) -> str:
    compiled = re.sub(
        r"\{\{\s*source\('([^']+)',\s*'([^']+)'\)\s*\}\}",
        lambda match: match.group(2),
        sql,
    )
    compiled = re.sub(
        r"\{\{\s*ref\('([^']+)'\)\s*\}\}",
        lambda match: match.group(1),
        compiled,
    )
    return compiled.strip()


def main() -> None:
    report = run_analytics_engineering_checks(get_settings())
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
