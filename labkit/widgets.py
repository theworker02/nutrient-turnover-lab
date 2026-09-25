"""Small UI widgets (kept separate from the large CSS module for clean Streamlit reloads)."""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

CLADE_COLORS = {
    "Bacterium": "#7a4e6b",
    "Fungus": "#5c6b3d",
    "Nematode": "#2f6b6b",
    "Insect": "#b86a1e",
    "Fish": "#3d7a6b",
    "Bird": "#c47a3a",
    "Mammal": "#6b4a3d",
}


def section_header(label: str, title: str) -> None:
    st.markdown(
        f'<div class="section-block"><div class="section-label">{label}</div>'
        f'<div class="section-title">{title}</div></div>',
        unsafe_allow_html=True,
    )


def quiz_prompt(num: int, question: str, topic: str | None = None) -> None:
    topic_html = f'<div class="quiz-topic">Topic · {topic}</div>' if topic else ""
    st.markdown(
        f"""
        <div class="quiz-wrap">
          {topic_html}
          <div class="quiz-card">
            <span class="quiz-num">{num}</span>
            <span class="quiz-q">{question}</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def score_banner(score: int, total: int) -> None:
    pct = int(round(100 * score / total)) if total else 0
    if pct >= 80:
        grade = "Excellent"
    elif pct >= 60:
        grade = "Solid"
    else:
        grade = "Review the exhibit"
    st.markdown(
        f"""
        <div class="score-banner">
          <div class="big">{score} / {total}</div>
          <div style="color:#3a4535;margin-top:0.35rem;">{pct}% · {grade}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def cite_card(topic: str, ref: str) -> None:
    st.markdown(
        f"""
        <div class="cite-card">
          <div class="cite-topic">{topic}</div>
          <div class="cite-ref">{ref}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def vivid_layout(fig: go.Figure, height: int = 440, **extra) -> go.Figure:
    # Lazy import avoids circular load with labkit.ui
    from labkit.ui import apply_layout

    fig = apply_layout(fig, height=height, **extra)
    fig.update_layout(
        colorway=[
            "#b86a1e",
            "#3f5f36",
            "#2f6b6b",
            "#c45c3a",
            "#7a4e6b",
            "#d4a35c",
            "#4a6b8a",
            "#8a5a2b",
            "#5c8a4a",
            "#9a3d5c",
        ]
    )
    return fig
