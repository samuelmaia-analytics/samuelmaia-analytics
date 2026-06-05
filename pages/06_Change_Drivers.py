from __future__ import annotations

import streamlit as st

from app.ui.components import (
    render_bullet_card,
    render_hero_panel,
    render_info_card,
    render_section_header,
    render_severity_badge,
)
from config.settings import get_settings
from core.pipeline import build_portfolio_snapshot


snapshot = build_portfolio_snapshot(get_settings())
payload = snapshot["change_drivers"]
drivers = payload.get("drivers", [])

render_hero_panel(
    "Change Drivers",
    "Executive view of the portfolio movements that matter most, with severity and suggested action.",
    "Decision Triage",
    chips=[
        f"Drivers Detected: {len(drivers)}",
        f"Action Ready: {'YES' if payload.get('recommended_action') else 'NO'}",
        f"Summary Available: {'YES' if payload.get('summary') else 'NO'}",
    ],
)

intro_left, intro_right = st.columns((1.0, 1.0))
with intro_left:
    render_info_card(
        "What This Surface Does",
        "This page turns historical metric movement into a prioritized review layer, highlighting what changed, how material the movement is, and what action should follow.",
    )
with intro_right:
    render_bullet_card(
        "Review Questions",
        [
            "What is moving the portfolio signal right now?",
            "Is the movement stable, watch-worthy, material, or critical?",
            "Which action should happen before the next stakeholder review?",
        ],
    )

render_section_header(
    "Summary", "Short explanation of the current portfolio movement and the suggested response."
)
summary_left, summary_right = st.columns((1.1, 0.9))
with summary_left:
    render_info_card("Change Narrative", payload.get("summary", "No summary available."))
with summary_right:
    render_info_card(
        "Recommended Action", payload.get("recommended_action", "No action currently recommended.")
    )

if drivers:
    render_section_header(
        "Detected Drivers",
        "Structured list of the strongest contributors behind the most recent historical comparison.",
    )
    highest = max(
        (driver.get("materiality", "stable") for driver in drivers),
        key=lambda item: {"stable": 0, "watch": 1, "material": 2, "critical": 3}.get(item, 0),
    )
    render_severity_badge("Highest Materiality", highest)
    st.dataframe(drivers, width="stretch", hide_index=True)
else:
    st.write("No material change drivers detected in the latest comparison.")

detail_left, detail_right = st.columns((1.0, 1.0))
with detail_left:
    render_bullet_card(
        "Why This Matters",
        [
            "Reviewers can focus on what changed instead of re-reading every metric or asset table.",
            "Materiality thresholds create a consistent standard for escalation and monitoring.",
            "The same change logic can support executive summaries, anomaly drafts, and operational triage.",
        ],
    )
with detail_right:
    render_info_card(
        "Operating Principle",
        "Movement should be explainable, severity should be visible, and the recommended action should be explicit. This page packages those three elements together.",
    )
