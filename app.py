"""Nutrient Turnover Lab — home."""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from labkit.metrics import metric_row
from labkit.species_data import SPECIES, species_dataframe
from labkit.ui import apply_layout, callout, hero, inject_style

st.set_page_config(
    page_title="Nutrient Turnover Lab",
    page_icon="🪰",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_style()

n_species = len(SPECIES)

hero(
    "Nutrient Turnover Lab",
    "How fruit flies and their yeast partners collapse a fruit's sugars into biomass—and why fly "
    "populations compound so fast—mapped against microbes, insects, fish, birds, and mammals "
    f"across a {n_species}-species teaching set.",
)

metric_row(
    [
        ("Focal species", "D. melanogaster"),
        ("Egg → adult @ 25°C", "~10 days"),
        ("Lifetime eggs", "~200–900"),
        ("Comparison set", f"{n_species} species"),
    ]
)

callout(
    "<strong>Core idea:</strong> flies do not out-enzyme the microbial world alone. They "
    "<em>amplify</em> it—seeding yeasts, shredding pulp, and converting sugars on a larval clock "
    "matched to ephemeral fruit—while mammals pay endotherm and pregnancy time costs. "
    "E. coli is faster still; elephants anchor the extreme K end."
)

st.markdown("### Navigate the exhibit")
a, b = st.columns(2)
with a:
    st.info("**Fruit-fly nutrient engine** — attraction → inoculation → fragmentation → assimilation → mutualism")
    st.info("**Why they multiply** — temperature curves, generation stacking, stage-structured boom")
with b:
    st.info("**Comparative species** — dual profiles, multi-overlay radar, Kleiber context, essays")
    st.info("**Simulators & quiz** — nutrient presets, population race, allometry explorer")

df = species_dataframe()
fig = px.scatter(
    df,
    x="Adult mass (g)",
    y="Generation time (days)",
    size="Lifetime fecundity",
    color="Clade",
    hover_name="Common name",
    hover_data=["Scientific name", "Gen. low (days)", "Gen. high (days)", "Mass-specific BMR (W/kg)"],
    log_x=True,
    log_y=True,
    title="Body size vs generation time (log–log) — bubble = lifetime fecundity",
)
apply_layout(fig, height=480)
st.plotly_chart(fig, use_container_width=True)

st.caption(
    "Hover a point to see generation-time ranges. E. coli and yeast sit at extreme speed; "
    "elephants and humans anchor the slow end. Values are literature-anchored teaching "
    "estimates—see Methods."
)

with st.expander("Run this lab"):
    st.code(
        "cd nutrient-turnover-lab\n"
        ".\\.venv\\Scripts\\activate\n"
        "streamlit run app.py",
        language="bash",
    )
