from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path


def emit_observability_event(event_name: str, payload: dict[str, object], output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    event = {
        "event_name": event_name,
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "payload": payload,
    }
    with (output_dir / "events.jsonl").open("a", encoding="utf-8") as file:
        file.write(json.dumps(event) + "\n")
    return event

