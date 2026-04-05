from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


def validate_contract(payload: dict[str, object], schema_path: Path) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    return [error.message for error in validator.iter_errors(payload)]

