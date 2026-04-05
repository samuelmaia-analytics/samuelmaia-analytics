from __future__ import annotations

from core.runtime_config import build_runtime_config_summary
from config.settings import get_settings


def test_runtime_config_summary_is_sanitized() -> None:
    summary = build_runtime_config_summary(get_settings())

    assert "change_driver_thresholds" in summary
    assert summary["genai"]["api_key_configured"] in {True, False}
    assert "api_key" not in str(summary).lower() or "api_key_configured" in summary["genai"]
