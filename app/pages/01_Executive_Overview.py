from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.ui.components import render_severity_badge
from config.settings import get_settings
from core.pipeline import build_portfolio_snapshot


st.title("Executive Overview")
st.caption("Quick access to the latest portfolio-level analytical signal.")

snapshot = build_portfolio_snapshot(get_settings())
st.metric("Decision Readiness Score", f"{snapshot['semantic_metrics']['decision_readiness_score']:.1f}")
st.metric("Quality Pass Rate", f"{snapshot['semantic_metrics']['quality_pass_rate']:.1f}%")
st.metric("Platform Trust Score", f"{snapshot['semantic_metrics']['platform_trust_score']:.1f}")

history = snapshot["operational_context"]["snapshot_history"].get("metric_history_series", [])
if history:
    st.subheader("Metric Trend")
    st.caption(snapshot["operational_context"]["snapshot_history"].get("comparison_summary", ""))
    chart_rows = [
        {
            "timestamp_utc": item["timestamp_utc"],
            "decision_readiness_score": item["decision_readiness_score"],
            "quality_pass_rate": item["quality_pass_rate"],
            "platform_trust_score": item["platform_trust_score"],
        }
        for item in history
    ]
    st.line_chart(chart_rows, x="timestamp_utc")

project_change_summary = snapshot["operational_context"]["snapshot_history"].get("project_change_summary", {})
st.subheader("Project Change Summary")
st.caption(project_change_summary.get("summary", ""))
project_changes = project_change_summary.get("changes", [])
driver_payload = snapshot.get("change_drivers", {})
driver_levels = [driver.get("materiality", "stable") for driver in driver_payload.get("drivers", [])]
if driver_levels:
    highest = max(driver_levels, key=lambda item: {"stable": 0, "watch": 1, "material": 2, "critical": 3}.get(item, 0))
    render_severity_badge("Portfolio Change Severity", highest)
if project_changes:
    st.dataframe(project_changes, width="stretch", hide_index=True)
else:
    st.write("No project-level changes detected across the latest historical comparison.")
