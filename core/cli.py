from __future__ import annotations

import argparse
import json
from pathlib import Path

from config.settings import get_settings
from core.governance_policy import build_governance_policy_report
from core.health import build_health_report
from core.pipeline import build_portfolio_snapshot


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Portfolio platform operational CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("snapshot", help="Build the canonical portfolio snapshot.")
    subparsers.add_parser("health", help="Print the current operational health report.")
    subparsers.add_parser("analytics-checks", help="Run dbt-like analytics engineering checks against the warehouse.")
    subparsers.add_parser("policy-checks", help="Print governance policy checks for runtime configuration.")
    subparsers.add_parser("validate", help="Run snapshot build as a contract and quality validation.")
    subparsers.add_parser("sync-registry", help="Sync enriched repository registry metadata.")

    export_cmd = subparsers.add_parser("export", help="Export a copy of the snapshot to a target path.")
    export_cmd.add_argument("--output", required=True, help="Target file path for the exported snapshot JSON.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    settings = get_settings()

    if args.command == "snapshot":
        snapshot = build_portfolio_snapshot(settings)
        print(json.dumps(snapshot["semantic_metrics"], indent=2))
        return

    if args.command == "health":
        print(json.dumps(build_health_report(settings), indent=2))
        return

    if args.command == "analytics-checks":
        from core.analytics_engineering import run_analytics_engineering_checks

        print(json.dumps(run_analytics_engineering_checks(settings), indent=2))
        return

    if args.command == "policy-checks":
        print(json.dumps(build_governance_policy_report(settings), indent=2))
        return

    if args.command == "validate":
        snapshot = build_portfolio_snapshot(settings)
        print(
            json.dumps(
                {
                    "status": "ok",
                    "quality_pass_rate": snapshot["quality_report"]["pass_rate"],
                    "projects": len(snapshot["projects"]),
                },
                indent=2,
            )
        )
        return

    if args.command == "sync-registry":
        from core.metadata_sync import sync_repository_metadata

        registry = sync_repository_metadata(settings)
        print(json.dumps({"status": "ok", "projects": len(registry)}, indent=2))
        return

    if args.command == "export":
        snapshot = build_portfolio_snapshot(settings)
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
        print(json.dumps({"status": "ok", "output": str(output)}, indent=2))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
