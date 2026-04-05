from __future__ import annotations

import streamlit as st

from config.settings import get_settings
from core.pipeline import build_portfolio_snapshot


st.title("Repository Intelligence")
st.caption("Selective integration of local reference repositories into the enterprise scaffold.")

snapshot = build_portfolio_snapshot(get_settings())
registry = snapshot["repository_registry"]

st.subheader("Registry Status")
st.dataframe(registry, width="stretch", hide_index=True)

ready_count = sum(1 for item in registry if item["exists_locally"] and item["entrypoint_exists"])
st.metric("Ready Local Repositories", f"{ready_count}/{len(registry)}")

change_summary = snapshot["operational_context"]["snapshot_history"].get("repository_change_summary", {})
st.subheader("Repository Change Summary")
st.caption(change_summary.get("summary", ""))
changes = change_summary.get("changes", [])
if changes:
    st.dataframe(changes, width="stretch", hide_index=True)
else:
    st.write("No repository changes detected across the latest historical comparison.")

st.subheader("Why This Layer Exists")
st.markdown(
    """
    The root scaffold stays maintainable by integrating local repositories through metadata and readiness checks,
    instead of collapsing every technical asset into one runtime surface too early.
    """
)

project_history = snapshot["operational_context"]["snapshot_history"].get("project_history_series", [])
if project_history:
    st.subheader("Project Metric History")
    project_choice = st.selectbox("Select a project", options=sorted({row["project_name"] for row in project_history}))
    filtered = [row for row in project_history if row["project_name"] == project_choice]
    st.line_chart(
        filtered,
        x="timestamp_utc",
        y=["governance_score", "quality_score", "execution_score", "observability_score"],
    )
