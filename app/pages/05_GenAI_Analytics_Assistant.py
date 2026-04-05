from __future__ import annotations

import streamlit as st

from app.ui.components import render_severity_badge
from config.settings import get_settings
from core.pipeline import build_portfolio_snapshot


st.title("GenAI Analytics Assistant")
st.caption("Provider-agnostic drafts for KPI narratives, glossary support, anomaly triage, and data asset descriptions.")

snapshot = build_portfolio_snapshot(get_settings())
artifacts = snapshot["genai_outputs"]

selected = st.selectbox(
    "Select an analytics GenAI artifact",
    options=list(artifacts.keys()),
    format_func=lambda value: artifacts[value]["title"],
)
artifact = artifacts[selected]

st.subheader(artifact["title"])
st.caption(
    f"Provider: {artifact['provider_name']} | Status: {artifact['provider_status']} | Mode: {artifact['generation_mode']}"
)
st.markdown(artifact["narrative"])
st.write("Key points")
for bullet in artifact["bullets"]:
    st.write(f"- {bullet}")

change_drivers = snapshot.get("change_drivers", {})
st.subheader("Change Drivers")
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
