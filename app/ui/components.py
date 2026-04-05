from __future__ import annotations

import streamlit as st


def render_section_header(title: str, description: str) -> None:
    st.subheader(title)
    st.caption(description)


def render_kpi_grid(metrics: dict[str, float]) -> None:
    items = list(metrics.items())
    columns = st.columns(min(4, len(items)))
    for idx, (name, value) in enumerate(items):
        columns[idx % len(columns)].metric(name.replace("_", " ").title(), f"{value:.1f}")


def render_severity_badge(label: str, severity: str) -> None:
    palette = {
        "stable": ("#d1fae5", "#065f46"),
        "watch": ("#fef3c7", "#92400e"),
        "material": ("#fed7aa", "#9a3412"),
        "critical": ("#fecaca", "#991b1b"),
    }
    background, foreground = palette.get(severity, ("#e5e7eb", "#374151"))
    st.markdown(
        (
            f"<div style='display:inline-block;padding:0.35rem 0.65rem;border-radius:999px;"
            f"background:{background};color:{foreground};font-weight:600;font-size:0.85rem;'>"
            f"{label}: {severity.title()}</div>"
        ),
        unsafe_allow_html=True,
    )
