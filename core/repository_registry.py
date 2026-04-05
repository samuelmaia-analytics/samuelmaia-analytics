from __future__ import annotations

import json
from pathlib import Path


def load_repository_registry(registry_path: Path) -> list[dict[str, object]]:
    root = registry_path.resolve().parents[1]
    payload = json.loads(registry_path.read_text(encoding="utf-8"))
    projects: list[dict[str, object]] = []
    for item in payload.get("projects", []):
        local_root = root / item["local_path"]
        entrypoint = local_root / item["entrypoint"]
        readme_title = _read_markdown_title(entrypoint) if entrypoint.exists() else None
        projects.append(
            {
                **item,
                "resolved_path": str(local_root),
                "exists_locally": local_root.exists(),
                "entrypoint_exists": entrypoint.exists(),
                "readme_title": readme_title,
                "markdown_files": _count_files(local_root, "*.md"),
                "python_files": _count_files(local_root, "*.py"),
                "tests_present": (local_root / "tests").exists(),
            }
        )
    return projects


def _read_markdown_title(path: Path) -> str | None:
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped.removeprefix("# ").strip()
    return None


def _count_files(root: Path, pattern: str) -> int:
    if not root.exists():
        return 0
    return sum(1 for _ in root.rglob(pattern))
