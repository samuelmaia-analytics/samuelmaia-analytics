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


st.title("Change Drivers")
st.caption("Executive surface for the main drivers behind recent portfolio movement.")

snapshot = build_portfolio_snapshot(get_settings())
payload = snapshot["change_drivers"]

st.subheader("Summary")
st.write(payload.get("summary", ""))
st.caption(payload.get("recommended_action", ""))

drivers = payload.get("drivers", [])
if drivers:
    st.subheader("Detected Drivers")
    highest = max(
        (driver.get("materiality", "stable") for driver in drivers),
        key=lambda item: {"stable": 0, "watch": 1, "material": 2, "critical": 3}.get(item, 0),
    )
    render_severity_badge("Highest Materiality", highest)
    st.dataframe(drivers, width="stretch", hide_index=True)
else:
    st.write("No material change drivers detected in the latest comparison.")
