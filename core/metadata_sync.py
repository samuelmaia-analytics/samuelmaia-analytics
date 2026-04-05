from __future__ import annotations

import json

from config.settings import Settings
from core.repository_registry import load_repository_registry


def sync_repository_metadata(settings: Settings) -> list[dict[str, object]]:
    registry = load_repository_registry(settings.project_registry_path)
    output = settings.artifacts_dir / "repository_registry_snapshot.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    return registry
