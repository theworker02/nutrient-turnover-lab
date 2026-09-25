"""Methods, equations, citations — exhibit builder."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from labkit.species_data import CITATIONS_LONG, SPECIES, species_dataframe
from labkit.ui import callout, hero, inject_style
from labkit.widgets import cite_card, section_header, vivid_layout

inject_style()

hero(
    "Methods & sources",
    "A transparency gallery: design principles, model equations, accuracy by taxon, "
    "and curated reading paths for every clade in the lab.",
    kicker="Source builder",
)

callout(
    "This app is an <strong>interactive teaching synthesis</strong>. Central estimates include explicit ranges. "
    "Replace any number with a primary citation before using it in graded or published work."
)

section_header("Principles", "How numbers were chosen")
p1, p2 = st.columns(2)
with p1:
    st.markdown(
        """
<div class="model-card">
  <h4>1 · Prefer ranges</h4>
  <p style="margin:0;color:#3a4535;">Every species carries low/high bounds for mass, generation, fecundity, and gut time. Charts use central estimates; hover and tables expose uncertainty.</p>
</div>
<div class="model-card">
  <h4>2 · Ecology × physiology</h4>
  <p style="margin:0;color:#3a4535;">Fly “acceleration” is mostly partnership + fragmentation + throughput—not inventing cellulose digestion.</p>
</div>
""",
        unsafe_allow_html=True,
    )
with p2:
    st.markdown(
        """
<div class="model-card">
  <h4>3 · Temperature for ectotherms</h4>
  <p style="margin:0;color:#3a4535;">Development curves are teaching fits inspired by published timing trends—not strain-specific SOPs.</p>
</div>
<div class="model-card">
  <h4>4 · Mammals differ in kind</h4>
  <p style="margin:0;color:#3a4535;">Endothermy and gestation impose time costs insects and microbes do not pay—even when mass-specific BMR looks “fast.”</p>
</div>
""",
        unsafe_allow_html=True,
    )

section_header("Models", "Equations as implemented")
tabs = st.tabs(["Logistic", "Sugar–yeast–larva", "Fly stages", "Kleiber", "Doubling"])
with tabs[0]:
    st.code("N_{t+1} = N_t + r · N_t · (1 - N_t / K)", language="text")
    st.caption("Discrete logistic growth on a shared carrying capacity.")
with tabs[1]:
    st.code(
        "yeast growth ~ Monod(sugar) × fragmentation\n"
        "yeast += growth + adult_seeding\n"
        "sugar  -= yeast_uptake + larva_uptake",
        language="text",
    )
    st.caption("Hourly toy model; yeast index is dimensionless.")
with tabs[2]:
    st.code(
        "transitions ˜ 1 / stage_duration(temp)\n"
        "larval survival declines with density\n"
        "new adults ˜ 50% female",
        language="text",
    )
with tabs[3]:
    st.code("BMR_W ˜ 3.4 · M_kg^0.75", language="text")
    st.caption("Placental-mammal-oriented reference; insects/microbes often deviate.")
with tabs[4]:
    st.code("T_double = ln(2) / r", language="text")

section_header("Coverage", "Where the teaching set sits")
df = species_dataframe()
fig = px.treemap(
    df,
    path=["Clade", "Common name"],
    values="Lifetime fecundity",
    color="Generation time (days)",
    color_continuous_scale=["#b86a1e", "#d4a35c", "#ebe1c8", "#3f5f36"],
    title="Clade → species · size = fecundity · color = generation time",
)
vivid_layout(fig, height=420)
st.plotly_chart(fig, use_container_width=True)

section_header("Accuracy", "Reliable vs uncertain by taxon")
accuracy = pd.DataFrame(
    [
        {"Taxon": "Fruit fly", "Most reliable": "˜10 d gen @ 25°C; high fecundity OM", "Most uncertain": "Exact mass-specific BMR; gut minutes vs hours"},
        {"Taxon": "Mouse / rat", "Most reliable": "Gestation, litter, maturity windows", "Most uncertain": "BMR point (± diet, strain, method)"},
        {"Taxon": "C. elegans", "Most reliable": "˜3 d gen @ 20°C; ~300 brood", "Most uncertain": "Mass and BMR proxies"},
        {"Taxon": "Yeast / E. coli", "Most reliable": "Rich-medium doubling order of magnitude", "Most uncertain": "Mapping to fruit-patch communities"},
        {"Taxon": "Bee / blowfly", "Most reliable": "Brood timing; forensic tables", "Most uncertain": "Colony vs individual r for bees"},
        {"Taxon": "Fish / bird", "Most reliable": "Incubation / clutch norms", "Most uncertain": "Field generation length"},
        {"Taxon": "Cat / elephant / human", "Most reliable": "Gestation & interbirth order of magnitude", "Most uncertain": "Demographic generation culturally variable"},
    ]
)
st.dataframe(accuracy, use_container_width=True, hide_index=True)

section_header("Reading paths", f"{len(CITATIONS_LONG)} curated entry points")
filter_q = st.text_input("Filter citations", placeholder="e.g. yeast, elephant, Kleiber…")
shown = 0
for item in CITATIONS_LONG:
    blob = f"{item['topic']} {item['ref']}".lower()
    if filter_q and filter_q.lower() not in blob:
        continue
    cite_card(item["topic"], item["ref"])
    shown += 1
if filter_q and shown == 0:
    st.info("No citations match that filter.")

section_header("Per-species notes", "Citation snippets on each profile")
sid = st.selectbox(
    "Inspect species source notes",
    list(SPECIES.keys()),
    format_func=lambda k: f"{SPECIES[k]['common_name']} ({SPECIES[k]['scientific_name']})",
)
for c in SPECIES[sid]["citations"]:
    st.markdown(f"- {c}")

section_header("Run locally", "Reproduce this exhibit")
st.code(
    "cd nutrient-turnover-lab\n.\\.venv\\Scripts\\activate\nstreamlit run app.py",
    language="bash",
)
st.caption(f"Teaching set currently includes {len(SPECIES)} species in `labkit/species_data.py`.")
