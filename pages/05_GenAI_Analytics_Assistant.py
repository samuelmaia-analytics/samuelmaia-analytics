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
artifacts = snapshot["genai_outputs"]
change_drivers = snapshot.get("change_drivers", {})

render_hero_panel(
    "GenAI Analytics Assistant",
    "Provider-agnostic narrative drafts for KPI commentary, glossary support, anomaly triage, and dataset explanation.",
    "AI Support Layer",
    chips=[
        f"Artifacts: {len(artifacts)}",
        f"Provider: {snapshot['genai_insight']['provider_name']}",
        f"Mode: {snapshot['genai_insight']['generation_mode']}",
    ],
)

intro_left, intro_right = st.columns((1.0, 1.0))
with intro_left:
    render_info_card(
        "What This Layer Does",
        "This capability converts governed analytical context into review-ready drafts. It is intentionally optional, provider-agnostic, and safe to evolve toward external LLM providers later.",
    )
with intro_right:
    render_bullet_card(
        "Useful Outcomes",
        [
            "Narrative KPI insight drafts for executive and operating review.",
            "Metric and glossary explanations for self-service understanding.",
            "Anomaly and change-driver framing backed by platform context.",
        ],
    )

selected = st.selectbox(
    "Select an analytics GenAI artifact",
    options=list(artifacts.keys()),
    format_func=lambda value: artifacts[value]["title"],
)
artifact = artifacts[selected]

render_section_header(
    artifact["title"], "Generated draft based on current platform context and configured prompts."
)
st.caption(
    f"Provider: {artifact['provider_name']} | Status: {artifact['provider_status']} | Mode: {artifact['generation_mode']}"
)
artifact_left, artifact_right = st.columns((1.1, 0.9))
with artifact_left:
    render_info_card("Narrative Draft", artifact["narrative"])
with artifact_right:
    render_bullet_card("Key Points", artifact["bullets"])

render_section_header(
    "Change Drivers", "Operational context that helps explain what the drafts should emphasize."
)
st.caption(change_drivers.get("recommended_action", ""))
drivers = change_drivers.get("drivers", [])
if drivers:
    highest = max(
        (driver.get("materiality", "stable") for driver in drivers),
        key=lambda item: {"stable": 0, "watch": 1, "material": 2, "critical": 3}.get(item, 0),
    )
    render_severity_badge("Highest Materiality", highest)
    st.dataframe(drivers, width="stretch", hide_index=True)
else:
    st.write("No material change drivers detected.")

review_left, review_right = st.columns((1.0, 1.0))
with review_left:
    render_bullet_card(
        "Why This Is Useful",
        [
            "Analytical narratives become faster to review and easier to share with non-technical stakeholders.",
            "Context stays tied to platform metrics, drivers, and governed metadata instead of generic text generation.",
            "The provider layer can be swapped later without redesigning the app surface.",
        ],
    )
with review_right:
    render_info_card(
        "Design Constraint",
        "This GenAI layer is intentionally scoped to analytics support. It augments explanation and review, but it does not replace contracts, quality checks, or semantic definitions.",
    )
