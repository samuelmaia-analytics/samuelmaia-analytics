from __future__ import annotations

import json
from typing import Any

from config.settings import Settings


def load_business_glossary(settings: Settings) -> dict[str, Any]:
    path = settings.config_dir / "business_glossary.json"
    return json.loads(path.read_text(encoding="utf-8"))


def load_dataset_catalog(settings: Settings) -> dict[str, Any]:
    path = settings.config_dir / "dataset_catalog.json"
    return json.loads(path.read_text(encoding="utf-8"))
