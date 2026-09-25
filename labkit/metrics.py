"""Metric chip row — tiny module to avoid Streamlit hot-reload import glitches."""

from __future__ import annotations

import streamlit as st


def metric_row(items: list[tuple[str, str]]) -> None:
    """Render non-truncating metric chips as (label, value) pairs."""
    cells = []
    for label, value in items:
        cells.append(
            f'<div class="chip"><div class="lbl">{label}</div><div class="val">{value}</div></div>'
        )
    st.markdown(
        f'<div class="metric-row">{"".join(cells)}</div>',
        unsafe_allow_html=True,
    )
