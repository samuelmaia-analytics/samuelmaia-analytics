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
catalog = snapshot["metric_catalog"]
headline_metrics = catalog["headline_metrics"]
domain_rollup = catalog["domain_rollup"]
domain_history = snapshot["operational_context"]["snapshot_history"].get(
    "domain_history_series", []
)

render_hero_panel(
    "Semantic Metrics",
    "Shared KPI definitions, domain rollups, and semantic consistency signals used across the platform surface.",
    "Metric Layer",
    chips=[
        f"Headline Metrics: {len(headline_metrics)}",
        f"Definitions: {len(catalog['definitions'])}",
        f"Domains: {len(domain_rollup)}",
    ],
)

intro_left, intro_right = st.columns((1.0, 1.0))
with intro_left:
    render_info_card(
        "Why This Layer Matters",
        "Semantic consistency is what makes metrics reusable across the app, API, warehouse, and documentation. This page shows the definitions and rollups that keep analytical interpretation aligned.",
    )
with intro_right:
    render_bullet_card(
        "Review Focus",
        [
            "Are KPI definitions explicit and reusable across surfaces?",
            "Can domain-level performance be reviewed without rebuilding logic in each tool?",
            "Does the metric layer make business interpretation safer and more consistent?",
        ],
    )

render_section_header(
    "Headline Metrics",
    "Top-level metrics surfaced as the shared analytical language of the platform.",
)
st.json(catalog["headline_metrics"])

render_section_header(
    "Metric Definitions",
    "Business-facing and technically reusable definitions for the current KPI set.",
)
st.dataframe(catalog["definitions"], width="stretch", hide_index=True)

render_section_header(
    "Domain Rollup",
    "Aggregated scorecards showing analytical maturity across major capability domains.",
)
rollup_rows = [{"domain": domain, **metrics} for domain, metrics in domain_rollup.items()]
st.dataframe(rollup_rows, width="stretch", hide_index=True)

if domain_history:
    render_section_header(
        "Domain Trend History",
        "Historical movement of governance, quality, execution, and observability by domain.",
    )
    domain_choice = st.selectbox(
        "Select a domain", options=sorted({row["domain"] for row in domain_history})
    )
    filtered = [row for row in domain_history if row["domain"] == domain_choice]
    st.line_chart(
        filtered,
        x="timestamp_utc",
        y=["governance_score", "quality_score", "execution_score", "observability_score"],
    )

bottom_left, bottom_right = st.columns((1.0, 1.0))
with bottom_left:
    render_bullet_card(
        "Business Value",
        [
            "A clear metric layer reduces disagreement in dashboards, APIs, and executive reporting.",
            "Domain rollups make it easier to explain where analytical maturity is strong or still uneven.",
            "Reusable definitions strengthen handoff between analysts, engineers, and stakeholders.",
        ],
    )
with bottom_right:
    render_info_card(
        "Operating Principle",
        "Metrics should be defined once, reused broadly, and reviewed in context. This page is the visible proof of that discipline.",
    )
