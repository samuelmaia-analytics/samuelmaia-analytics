from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_cli_health_and_export(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]

    health = subprocess.run(
        [sys.executable, "-m", "core.cli", "health"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    health_payload = json.loads(health.stdout)
    assert health_payload["status"] in {"ok", "degraded"}

    output_path = tmp_path / "snapshot.json"
    exported = subprocess.run(
        [sys.executable, "-m", "core.cli", "export", "--output", str(output_path)],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    export_payload = json.loads(exported.stdout)
    assert export_payload["status"] == "ok"
    assert output_path.exists()
