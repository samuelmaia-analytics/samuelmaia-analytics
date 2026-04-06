from __future__ import annotations

import streamlit as st

__all__ = [
    "render_section_header",
    "render_kpi_grid",
    "render_hero_panel",
    "render_info_card",
    "render_bullet_card",
    "render_severity_badge",
]


def render_section_header(title: str, description: str) -> None:
    st.subheader(title)
    st.caption(description)


def render_kpi_grid(metrics: dict[str, float]) -> None:
    items = list(metrics.items())
    columns = st.columns(min(4, len(items)))
    for idx, (name, value) in enumerate(items):
        columns[idx % len(columns)].metric(name.replace("_", " ").title(), f"{value:.1f}")


def render_hero_panel(title: str, subtitle: str, eyebrow: str, chips: list[str] | None = None) -> None:
    chip_markup = ""
    if chips:
        chip_markup = "<div class='sm-chip-row'>" + "".join(
            f"<span class='sm-chip'>{chip}</span>" for chip in chips
        ) + "</div>"
    st.markdown(
        (
            "<section class='sm-hero'>"
            f"<div class='eyebrow'>{eyebrow}</div>"
            f"<h1>{title}</h1>"
            f"<p class='subtitle'>{subtitle}</p>"
            f"{chip_markup}"
            "</section>"
        ),
        unsafe_allow_html=True,
    )


def render_info_card(title: str, body: str) -> None:
    st.markdown(
        f"<section class='sm-card'><h4>{title}</h4><p>{body}</p></section>",
        unsafe_allow_html=True,
    )


def render_bullet_card(title: str, bullets: list[str]) -> None:
    items = "".join(f"<li>{bullet}</li>" for bullet in bullets)
    st.markdown(
        f"<section class='sm-card'><h4>{title}</h4><ul class='sm-list'>{items}</ul></section>",
        unsafe_allow_html=True,
    )


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
