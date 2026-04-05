from __future__ import annotations

from dataclasses import replace

from config.settings import get_settings
from core.metadata_sync import sync_repository_metadata


def test_metadata_sync_writes_registry_snapshot(tmp_path) -> None:
    settings = get_settings()
    test_settings = replace(settings, artifacts_dir=tmp_path / "processed")
    registry = sync_repository_metadata(test_settings)
    assert len(registry) >= 1
    assert (test_settings.artifacts_dir / "repository_registry_snapshot.json").exists()
