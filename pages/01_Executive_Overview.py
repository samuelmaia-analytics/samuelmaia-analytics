from __future__ import annotations

import streamlit as st

from app.ui.components import (
    render_bullet_card,
    render_hero_panel,
    render_info_card,
    render_kpi_grid,
    render_section_header,
    render_severity_badge,
)
from config.settings import get_settings
from core.pipeline import build_portfolio_snapshot


snapshot = build_portfolio_snapshot(get_settings())
semantic_metrics = snapshot["semantic_metrics"]
project_change_summary = snapshot["operational_context"]["snapshot_history"].get(
    "project_change_summary", {}
)
driver_payload = snapshot.get("change_drivers", {})
driver_levels = [
    driver.get("materiality", "stable") for driver in driver_payload.get("drivers", [])
]

render_hero_panel(
    "Executive Overview",
    "Decision readiness, portfolio trust, and the latest movement across analytical assets in one surface.",
    "Portfolio Signal",
    chips=[
        f"Decision Readiness: {semantic_metrics['decision_readiness_score']:.1f}",
        f"Quality Pass Rate: {semantic_metrics['quality_pass_rate']:.1f}%",
        f"Projects Tracked: {len(snapshot['repository_registry'])}",
    ],
)

render_section_header(
    "Top-Level KPI Signal",
    "This page compresses portfolio health into a review surface suitable for leadership, recruiting review, and technical due diligence.",
)
render_kpi_grid(
    {
        "decision_readiness_score": semantic_metrics["decision_readiness_score"],
        "quality_pass_rate": semantic_metrics["quality_pass_rate"],
        "platform_trust_score": semantic_metrics["platform_trust_score"],
    }
)

intro_left, intro_right = st.columns((1.05, 0.95))
with intro_left:
    render_info_card(
        "What This Surface Shows",
        "The platform translates quality, governance, and execution signals into a concise executive view so reviewers can understand portfolio health before inspecting implementation detail.",
    )
with intro_right:
    render_bullet_card(
        "Review Questions",
        [
            "Is the platform ready for decision support and stakeholder consumption?",
            "Did trust or quality improve across the most recent historical comparison?",
            "Which asset is driving movement in the portfolio signal?",
        ],
    )

history = snapshot["operational_context"]["snapshot_history"].get("metric_history_series", [])
if history:
    render_section_header(
        "Metric Trend", "Historical movement of the portfolio-level KPI set across recorded runs."
    )
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

render_section_header(
    "Project Change Summary", "Asset-level contribution behind the current portfolio movement."
)
st.caption(project_change_summary.get("summary", ""))
project_changes = project_change_summary.get("changes", [])
if driver_levels:
    highest = max(
        driver_levels,
        key=lambda item: {"stable": 0, "watch": 1, "material": 2, "critical": 3}.get(item, 0),
    )
    render_severity_badge("Portfolio Change Severity", highest)
if project_changes:
    st.dataframe(project_changes, width="stretch", hide_index=True)
else:
    st.write("No project-level changes detected across the latest historical comparison.")

signal_col, action_col = st.columns((1.0, 1.0))
with signal_col:
    render_bullet_card(
        "Why This Matters",
        [
            "Portfolio movement is traceable to project-level drivers instead of hidden in a single aggregate score.",
            "Historical comparisons make governance and execution trends reviewable over time.",
            "Severity highlights where a reviewer should focus attention first.",
        ],
    )
with action_col:
    render_info_card(
        "Recommended Action",
        snapshot.get("change_drivers", {}).get(
            "recommended_action", "No action currently recommended."
        ),
    )
