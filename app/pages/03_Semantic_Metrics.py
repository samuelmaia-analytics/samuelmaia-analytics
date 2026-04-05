from __future__ import annotations

import streamlit as st

from config.settings import get_settings
from core.pipeline import build_portfolio_snapshot


st.title("Semantic Metrics")
st.caption("Metric definitions, rollups, and domain-level analytical trust surfaces.")

snapshot = build_portfolio_snapshot(get_settings())
catalog = snapshot["metric_catalog"]

st.subheader("Headline Metrics")
st.json(catalog["headline_metrics"])

st.subheader("Metric Definitions")
st.dataframe(catalog["definitions"], width="stretch", hide_index=True)

st.subheader("Domain Rollup")
rollup_rows = [
    {"domain": domain, **metrics}
    for domain, metrics in catalog["domain_rollup"].items()
]
st.dataframe(rollup_rows, width="stretch", hide_index=True)

domain_history = snapshot["operational_context"]["snapshot_history"].get("domain_history_series", [])
if domain_history:
    st.subheader("Domain Trend History")
    domain_choice = st.selectbox("Select a domain", options=sorted({row["domain"] for row in domain_history}))
    filtered = [row for row in domain_history if row["domain"] == domain_choice]
    st.line_chart(
        filtered,
        x="timestamp_utc",
        y=["governance_score", "quality_score", "execution_score", "observability_score"],
    )
