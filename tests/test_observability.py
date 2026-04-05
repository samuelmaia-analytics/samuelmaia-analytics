from __future__ import annotations

from pathlib import Path

from core.observability import emit_observability_event


def test_observability_event_is_written(tmp_path: Path) -> None:
    event = emit_observability_event("test_event", {"status": "ok"}, tmp_path)
    assert event["event_name"] == "test_event"
    assert (tmp_path / "events.jsonl").exists()
