from __future__ import annotations

import streamlit as st

from app.ui.components import (
    render_bullet_card,
    render_hero_panel,
    render_info_card,
    render_section_header,
)
from config.settings import get_settings
from core.pipeline import build_portfolio_snapshot


snapshot = build_portfolio_snapshot(get_settings())
registry = snapshot["repository_registry"]
ready_count = sum(1 for item in registry if item["exists_locally"] and item["entrypoint_exists"])
change_summary = snapshot["operational_context"]["snapshot_history"].get(
    "repository_change_summary", {}
)

render_hero_panel(
    "Repository Intelligence",
    "Readiness, integration posture, and historical movement across the reference assets that support the portfolio platform.",
    "Asset Control Layer",
    chips=[
        f"Repositories Tracked: {len(registry)}",
        f"Ready Locally: {ready_count}/{len(registry)}",
        f"Historical Changes: {len(change_summary.get('changes', []))}",
    ],
)

intro_left, intro_right = st.columns((1.0, 1.0))
with intro_left:
    render_info_card(
        "Why This Layer Exists",
        "The platform stays maintainable by integrating supporting repositories through metadata, checks, and readiness signals instead of forcing every asset into one runtime surface.",
    )
with intro_right:
    render_bullet_card(
        "Review Focus",
        [
            "Which assets are locally available and operationally ready?",
            "What changed between the latest historical comparisons?",
            "How does each repository contribute to the portfolio signal over time?",
        ],
    )

render_section_header(
    "Registry Status", "Current integration posture of the local reference repositories."
)
st.dataframe(registry, width="stretch", hide_index=True)
st.metric("Ready Local Repositories", f"{ready_count}/{len(registry)}")

render_section_header(
    "Repository Change Summary", "Historical comparison of registry state between recent snapshots."
)
st.caption(change_summary.get("summary", ""))
changes = change_summary.get("changes", [])
if changes:
    st.dataframe(changes, width="stretch", hide_index=True)
else:
    st.write("No repository changes detected across the latest historical comparison.")

project_history = snapshot["operational_context"]["snapshot_history"].get(
    "project_history_series", []
)
if project_history:
    render_section_header(
        "Project Metric History",
        "Governance, quality, execution, and observability movement for each tracked asset.",
    )
    project_choice = st.selectbox(
        "Select a project", options=sorted({row["project_name"] for row in project_history})
    )
    filtered = [row for row in project_history if row["project_name"] == project_choice]
    st.line_chart(
        filtered,
        x="timestamp_utc",
        y=["governance_score", "quality_score", "execution_score", "observability_score"],
    )

detail_left, detail_right = st.columns((1.0, 1.0))
with detail_left:
    render_bullet_card(
        "Why This Improves Portfolio Quality",
        [
            "The flagship platform can stay clean while supporting repositories remain visible and comparable.",
            "Readiness checks make repository references auditable instead of narrative-only.",
            "Historical signals show whether an asset is becoming more governed or more fragile.",
        ],
    )
with detail_right:
    render_info_card(
        "Operating Principle",
        "Reference assets should be discoverable, assessable, and selectively integrated. This prevents portfolio sprawl while preserving technical depth.",
    )
