from __future__ import annotations

from config.settings import get_settings
from core.repository_registry import load_repository_registry


def test_repository_registry_detects_local_paths() -> None:
    settings = get_settings()
    registry = load_repository_registry(settings.project_registry_path)
    assert len(registry) >= 3
    assert any(item["exists_locally"] for item in registry)

