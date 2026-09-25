"""Shared Streamlit styling, chrome, and Plotly defaults."""

from __future__ import annotations

import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

:root {
  --ink: #182016;
  --moss: #243d28;
  --leaf: #3f5f36;
  --amber: #b86a1e;
  --amber-soft: #d4a35c;
  --pulp: #e8c47a;
  --paper: #f4ecda;
  --card: rgba(255, 252, 245, 0.88);
  --line: rgba(36, 61, 40, 0.14);
}

html, body, [class*="css"] {
  font-family: "IBM Plex Sans", "Segoe UI", sans-serif;
  color: var(--ink);
}

.stApp {
  background:
    radial-gradient(ellipse 90% 55% at 8% -10%, rgba(184, 106, 30, 0.20), transparent 55%),
    radial-gradient(ellipse 70% 50% at 95% 5%, rgba(63, 95, 54, 0.22), transparent 52%),
    radial-gradient(circle at 50% 120%, rgba(232, 196, 122, 0.25), transparent 45%),
    linear-gradient(168deg, #f8f1e2 0%, #ebe1c8 42%, #dfe6d4 100%);
}

.stApp::before {
  content: "";
  pointer-events: none;
  position: fixed;
  inset: 0;
  opacity: 0.035;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='120' height='120' filter='url(%23n)' opacity='0.55'/%3E%3C/svg%3E");
  z-index: 0;
}

h1, h2, h3, .brand-title {
  font-family: "Fraunces", Georgia, serif !important;
  letter-spacing: -0.025em;
  color: var(--moss) !important;
}

[data-testid="stSidebar"] {
  background:
    linear-gradient(185deg, #1d3022 0%, #152019 55%, #101811 100%);
  border-right: 1px solid rgba(232, 196, 122, 0.12);
}
[data-testid="stSidebar"] * { color: #f3ead8 !important; }
[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {
  border-radius: 10px !important;
  margin: 0.15rem 0.35rem !important;
  padding: 0.45rem 0.7rem !important;
}
[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {
  background: rgba(212, 163, 92, 0.16) !important;
}
[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] {
  background: rgba(184, 106, 30, 0.28) !important;
  box-shadow: inset 3px 0 0 var(--amber-soft);
}

.hero-panel {
  position: relative;
  overflow: hidden;
  background:
    linear-gradient(125deg, rgba(255,252,245,0.95), rgba(244,236,218,0.82)),
    radial-gradient(circle at 90% 20%, rgba(184,106,30,0.12), transparent 40%);
  border: 1px solid var(--line);
  border-radius: 22px;
  padding: 1.75rem 1.9rem 1.55rem;
  margin-bottom: 1.15rem;
  box-shadow: 0 18px 50px rgba(24, 32, 22, 0.08);
  backdrop-filter: blur(8px);
}
.hero-panel::after {
  content: "";
  position: absolute;
  right: -40px;
  top: -40px;
  width: 180px;
  height: 180px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(184,106,30,0.18), transparent 70%);
}

.brand-kicker {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--amber);
  font-weight: 700;
  margin-bottom: 0.4rem;
}
.brand-title {
  font-size: clamp(1.85rem, 3.5vw, 2.55rem);
  line-height: 1.08;
  margin: 0 0 0.55rem 0;
}
.brand-lede {
  font-size: 1.05rem;
  max-width: 48rem;
  color: #3a4535;
  margin: 0;
  line-height: 1.55;
}

.stage-card {
  background: rgba(255, 252, 245, 0.92);
  border-radius: 16px;
  padding: 1.05rem 1.2rem;
  border: 1px solid rgba(184, 106, 30, 0.22);
  margin-bottom: 0.7rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.stage-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 28px rgba(24, 32, 22, 0.07);
}
.stage-card .stage {
  color: var(--amber);
  font-weight: 700;
  font-size: 0.78rem;
  letter-spacing: 0.07em;
  text-transform: uppercase;
}

.callout {
  background: linear-gradient(100deg, rgba(63,95,54,0.1), rgba(184,106,30,0.08));
  border-left: 4px solid var(--leaf);
  border-radius: 0 14px 14px 0;
  padding: 0.95rem 1.15rem;
  margin: 0.85rem 0 1.1rem;
  color: #2c3628;
}

.range-pill {
  display: inline-block;
  background: rgba(184, 106, 30, 0.12);
  color: #7a4a14;
  border-radius: 999px;
  padding: 0.15rem 0.65rem;
  font-size: 0.8rem;
  font-weight: 600;
  margin-left: 0.35rem;
}

div[data-testid="stMetric"] {
  background: rgba(255, 252, 245, 0.9);
  border-radius: 14px;
  padding: 0.65rem 0.75rem;
  border: 1px solid var(--line);
  box-shadow: 0 6px 18px rgba(24, 32, 22, 0.04);
  height: 100%;
  overflow: visible;
}
div[data-testid="stMetric"] label {
  color: #5a6454 !important;
  white-space: normal !important;
  overflow: visible !important;
  text-overflow: unset !important;
  line-height: 1.25 !important;
  font-size: 0.78rem !important;
}
div[data-testid="stMetricValue"] {
  font-size: clamp(0.95rem, 1.6vw, 1.35rem) !important;
  white-space: normal !important;
  overflow: visible !important;
  text-overflow: unset !important;
  line-height: 1.2 !important;
  word-break: break-word;
}
div[data-testid="stMetricDelta"] {
  white-space: normal !important;
}

/* Prevent Streamlit from ellipsizing metric text */
div[data-testid="stMetricLabel"] > div {
  white-space: normal !important;
  overflow: visible !important;
}

div[data-testid="stExpander"] {
  background: rgba(255,252,245,0.7);
  border-radius: 14px;
  border: 1px solid var(--line);
}

.stTabs [data-baseweb="tab-list"] {
  gap: 0.35rem;
  flex-wrap: wrap;
}
.stTabs [data-baseweb="tab"] {
  background: rgba(255,252,245,0.65);
  border-radius: 10px 10px 0 0;
  padding: 0.45rem 0.9rem;
}

.section-label {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--amber);
  font-weight: 700;
  margin: 0.35rem 0 0.2rem;
}
.section-title {
  font-family: "Fraunces", Georgia, serif;
  font-size: 1.4rem;
  color: var(--moss);
  margin: 0 0 0.55rem;
  line-height: 1.2;
}
.section-block {
  margin: 1.1rem 0 0.35rem;
}

.quiz-wrap {
  background: linear-gradient(145deg, rgba(255,252,245,0.96), rgba(244,236,218,0.88));
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 0.85rem 1.1rem 0.35rem;
  margin-bottom: 0.85rem;
  box-shadow: 0 8px 22px rgba(24,32,22,0.05);
}
.quiz-wrap .quiz-topic {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #7a4a14;
  font-weight: 600;
  margin-bottom: 0.35rem;
}
.quiz-card {
  background: transparent;
  border: none;
  border-radius: 0;
  padding: 0 0 0.35rem 0;
  margin-bottom: 0;
  box-shadow: none;
}
.quiz-num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.85rem;
  height: 1.85rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #b86a1e, #d4a35c);
  color: #fffaf0;
  font-weight: 700;
  font-size: 0.85rem;
  margin-right: 0.55rem;
  flex-shrink: 0;
  vertical-align: middle;
}
.quiz-q {
  font-family: "Fraunces", Georgia, serif;
  font-size: 1.05rem;
  color: var(--moss);
  display: inline;
  line-height: 1.35;
  vertical-align: middle;
}
.score-banner {
  background: linear-gradient(120deg, rgba(63,95,54,0.14), rgba(184,106,30,0.16));
  border: 1px solid rgba(63,95,54,0.22);
  border-radius: 20px;
  padding: 1.25rem 1.5rem;
  text-align: center;
  margin: 0.8rem 0 1.2rem;
}
.score-banner .big {
  font-family: "Fraunces", Georgia, serif;
  font-size: 2.6rem;
  color: var(--moss);
  line-height: 1;
}
.feedback-ok, .feedback-bad {
  border-radius: 14px;
  padding: 0.85rem 1.05rem;
  margin-bottom: 0.55rem;
}
.feedback-ok { background: rgba(63,95,54,0.12); border-left: 4px solid #3f5f36; }
.feedback-bad { background: rgba(184,106,30,0.12); border-left: 4px solid #b86a1e; }

.cite-card {
  background: rgba(255,252,245,0.92);
  border-radius: 16px;
  border: 1px solid var(--line);
  padding: 1rem 1.15rem;
  margin-bottom: 0.65rem;
  box-shadow: 0 8px 22px rgba(24,32,22,0.04);
}
.cite-topic {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--amber);
  font-weight: 700;
}
.cite-ref { color: #3a4535; margin-top: 0.3rem; line-height: 1.45; }

.species-panel {
  background:
    linear-gradient(160deg, rgba(255,252,245,0.96), rgba(236,228,208,0.85)),
    radial-gradient(circle at 100% 0%, rgba(184,106,30,0.12), transparent 45%);
  border: 1px solid var(--line);
  border-radius: 20px;
  padding: 1.2rem 1.3rem;
  margin-bottom: 0.5rem;
  box-shadow: 0 14px 36px rgba(24,32,22,0.07);
  min-height: 100%;
}
.species-panel h3 {
  font-family: "Fraunces", Georgia, serif;
  margin: 0.15rem 0 0.2rem;
  color: var(--moss);
  font-size: 1.45rem;
}
.species-meta { color: #5a6454; font-size: 0.92rem; margin-bottom: 0.75rem; }
.stat-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.55rem;
  margin: 0.75rem 0;
}
.stat-cell {
  background: rgba(255,255,255,0.55);
  border-radius: 12px;
  padding: 0.55rem 0.7rem;
  border: 1px solid rgba(36,61,40,0.08);
}
.stat-cell .lbl { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.06em; color: #6a7464; }
.stat-cell .val { font-family: "Fraunces", Georgia, serif; color: var(--moss); font-size: 1.05rem; word-break: break-word; }
.stat-cell .range-pill { margin-left: 0; margin-top: 0.25rem; display: inline-block; }

.ratio-strip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
  gap: 0.55rem;
  margin: 0.5rem 0 1rem;
}
.ratio-chip {
  background: linear-gradient(160deg, #fffaf0, #f0e4c8);
  border-radius: 14px;
  padding: 0.7rem 0.85rem;
  border: 1px solid rgba(184,106,30,0.2);
  text-align: center;
  min-width: 0;
}
.ratio-chip .lbl { font-size: 0.7rem; color: #6a7464; text-transform: uppercase; letter-spacing: 0.05em; }
.ratio-chip .val {
  font-family: "Fraunces", Georgia, serif;
  font-size: clamp(0.95rem, 1.5vw, 1.2rem);
  color: #b86a1e;
  word-break: break-word;
}

.metric-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 0.65rem;
  margin: 0.35rem 0 0.95rem;
}
.metric-row .chip {
  background: rgba(255, 252, 245, 0.92);
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 0.7rem 0.85rem;
  box-shadow: 0 6px 18px rgba(24, 32, 22, 0.04);
  min-width: 0;
}
.metric-row .chip .lbl {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #5a6454;
  margin-bottom: 0.2rem;
  line-height: 1.25;
}
.metric-row .chip .val {
  font-family: "Fraunces", Georgia, serif;
  font-size: 1.2rem;
  color: var(--moss);
  line-height: 1.25;
  word-break: break-word;
}

.model-card {
  background: rgba(255,252,245,0.9);
  border-radius: 16px;
  border: 1px solid var(--line);
  padding: 1rem 1.15rem;
  margin-bottom: 0.7rem;
}
.model-card h4 {
  font-family: "Fraunces", Georgia, serif;
  color: var(--moss);
  margin: 0 0 0.4rem;
}

/* Layout polish */
.block-container {
  padding-top: 1.4rem !important;
  padding-bottom: 2.5rem !important;
  max-width: 1200px;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
  background: rgba(255,252,245,0.55);
  border-color: var(--line) !important;
}
[data-testid="stSidebarNav"] li:first-child span {
  font-size: 0 !important;
}
[data-testid="stSidebarNav"] li:first-child a span {
  font-size: 0 !important;
}
[data-testid="stSidebarNav"] li:first-child a::after {
  content: "Overview";
  font-size: 0.95rem !important;
  color: #f3ead8 !important;
  visibility: visible !important;
}
.stAppDeployButton,
[data-testid="stAppDeployButton"],
button[kind="header"],
[data-testid="stToolbar"] {
  display: none !important;
  visibility: hidden !important;
}
iframe[title="streamlit_plotly"] {
  border-radius: 12px;
}

footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
</style>
"""

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,252,245,0.72)",
    font=dict(family="IBM Plex Sans", color="#182016", size=13),
    title=dict(font=dict(family="Fraunces", size=18, color="#243d28")),
    margin=dict(l=40, r=20, t=55, b=40),
    legend=dict(bgcolor="rgba(255,252,245,0.85)", bordercolor="rgba(36,61,40,0.1)", borderwidth=1),
    colorway=["#b86a1e", "#3f5f36", "#6b4a3d", "#2f6b6b", "#8a5a2b", "#5c6b3d", "#7a4e6b", "#4a6b8a", "#9a6b3d"],
)


def inject_style() -> None:
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    pio.templates.default = "plotly_white"


def apply_layout(fig: go.Figure, height: int = 440, **extra) -> go.Figure:
    layout = {**PLOTLY_LAYOUT, "height": height, **extra}
    fig.update_layout(**layout)
    fig.update_xaxes(gridcolor="rgba(36,61,40,0.08)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(36,61,40,0.08)", zeroline=False)
    return fig


def hero(title: str, lede: str, kicker: str = "Nutrient Turnover Lab") -> None:
    st.markdown(
        f"""
        <div class="hero-panel">
          <div class="brand-kicker">{kicker}</div>
          <h1 class="brand-title">{title}</h1>
          <p class="brand-lede">{lede}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def stage_card(stage: str, title: str, detail: str) -> None:
    st.markdown(
        f"""
        <div class="stage-card">
          <div class="stage">{stage}</div>
          <h3 style="margin:0.25rem 0 0.4rem 0;font-family:Fraunces,Georgia,serif;color:#243d28;">{title}</h3>
          <p style="margin:0;color:#3a4535;line-height:1.5;">{detail}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def callout(text: str) -> None:
    st.markdown(f'<div class="callout">{text}</div>', unsafe_allow_html=True)


def fmt_range(low, high, unit: str = "") -> str:
    u = f" {unit}" if unit else ""
    return f"{low:g}–{high:g}{u}"


# Re-export widgets so older imports keep working after Streamlit reloads
from labkit.widgets import (  # noqa: E402
    CLADE_COLORS,
    cite_card,
    quiz_prompt,
    score_banner,
    section_header,
    vivid_layout,
)
