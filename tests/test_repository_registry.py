from __future__ import annotations

import json
from pathlib import Path

from core.repository_registry import load_repository_registry


def test_repository_registry_detects_local_paths(tmp_path: Path) -> None:
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    project_dir = tmp_path / "sample-project"
    project_dir.mkdir()
    (project_dir / "README.md").write_text("# Sample Project\n", encoding="utf-8")
    (project_dir / "app.py").write_text("print('ok')\n", encoding="utf-8")
    (project_dir / "tests").mkdir()

    registry_path = config_dir / "project_registry.json"
    registry_path.write_text(
        json.dumps(
            {
                "projects": [
                    {
                        "id": "sample-project",
                        "title": "Sample Project",
                        "role": "core",
                        "local_path": "sample-project",
                        "entrypoint": "README.md",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    registry = load_repository_registry(registry_path)
    assert registry == [
        {
            "id": "sample-project",
            "title": "Sample Project",
            "role": "core",
            "local_path": "sample-project",
            "entrypoint": "README.md",
            "resolved_path": str(project_dir),
            "exists_locally": True,
            "entrypoint_exists": True,
            "readme_title": "Sample Project",
            "markdown_files": 1,
            "python_files": 1,
            "tests_present": True,
        }
    ]
