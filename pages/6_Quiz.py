"""Knowledge check quiz — polished exhibit."""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from labkit.species_data import QUIZ
from labkit.ui import callout, hero, inject_style
from labkit.metrics import metric_row
from labkit.widgets import score_banner, section_header, vivid_layout

inject_style()

hero(
    "Knowledge check",
    "Eight short questions spanning attraction chemistry, mutualism, temperature, and the "
    "fast-slow life-history spectrum. Score yourself, then revisit the exhibit.",
    kicker="Quiz gallery",
)

answered = sum(1 for i in range(len(QUIZ)) if st.session_state.get(f"quiz_{i}") is not None)
prog = answered / len(QUIZ)
topics = len({q.get("topic", "General") for q in QUIZ})
metric_row(
    [
        ("Progress", f"{answered} / {len(QUIZ)} answered"),
        ("Questions", str(len(QUIZ))),
        ("Topics", str(topics)),
    ]
)
st.progress(prog)

section_header("Walkthrough", "Answer each card")

for i, item in enumerate(QUIZ):
    topic = item.get("topic", "General")
    with st.container(border=True):
        st.markdown(
            f'<div class="quiz-topic">Topic · {topic}</div>'
            f'<span class="quiz-num">{i + 1}</span>'
            f'<span class="quiz-q">{item["q"]}</span>',
            unsafe_allow_html=True,
        )
        st.radio(
            f"q{i}",
            list(range(len(item["choices"]))),
            format_func=lambda j, ch=item["choices"]: ch[j],
            index=None,
            key=f"quiz_{i}",
            label_visibility="collapsed",
        )

c_score, c_reset = st.columns(2)
with c_score:
    score_clicked = st.button("Score quiz", type="primary", use_container_width=True)
with c_reset:
    if st.button("Clear answers", use_container_width=True):
        for i in range(len(QUIZ)):
            st.session_state.pop(f"quiz_{i}", None)
        st.session_state.pop("quiz_feedback", None)
        st.rerun()

if score_clicked:
    answers = [st.session_state.get(f"quiz_{i}") for i in range(len(QUIZ))]
    if any(a is None for a in answers):
        st.warning("Answer every question first.")
        st.session_state.quiz_feedback = None
    else:
        score = sum(1 for a, item in zip(answers, QUIZ) if a == item["answer"])
        st.session_state.quiz_feedback = {"score": score, "answers": answers}

fb = st.session_state.get("quiz_feedback")
if fb:
    section_header("Results", "How you did")
    score_banner(fb["score"], len(QUIZ))

    topic_rows: dict[str, dict[str, int]] = {}
    for i, item in enumerate(QUIZ):
        t = item.get("topic", "General")
        topic_rows.setdefault(t, {"ok": 0, "n": 0})
        topic_rows[t]["n"] += 1
        if fb["answers"][i] == item["answer"]:
            topic_rows[t]["ok"] += 1

    fig = go.Figure()
    topics_sorted = sorted(topic_rows.keys())
    fig.add_trace(
        go.Bar(
            x=topics_sorted,
            y=[topic_rows[t]["ok"] for t in topics_sorted],
            name="Correct",
            marker_color="#3f5f36",
        )
    )
    fig.add_trace(
        go.Bar(
            x=topics_sorted,
            y=[topic_rows[t]["n"] - topic_rows[t]["ok"] for t in topics_sorted],
            name="Missed",
            marker_color="#d4a35c",
        )
    )
    fig.update_layout(barmode="stack", title="Score by topic", yaxis_title="Questions")
    vivid_layout(fig, height=340)
    st.plotly_chart(fig, use_container_width=True)

    for i, item in enumerate(QUIZ):
        ok = fb["answers"][i] == item["answer"]
        cls = "feedback-ok" if ok else "feedback-bad"
        mark = "Correct" if ok else "Review"
        st.markdown(
            f'<div class="{cls}"><strong>Q{i+1} · {mark}.</strong> {item["why"]}</div>',
            unsafe_allow_html=True,
        )

callout(
    "Want the primary literature and model equations? Open <strong>Methods & sources</strong> next."
)
