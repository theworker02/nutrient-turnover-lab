"""Fruit-fly nutrient breakdown pathway + coupled simulator."""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from labkit.species_data import FLY_NUTRIENT_PATHWAYS, get_species
from labkit.simulations import half_life_hours, nutrient_microbe_fly
from labkit.ui import apply_layout, callout, fmt_range, hero, inject_style, stage_card
from labkit.metrics import metric_row

inject_style()

hero(
    "The fruit-fly nutrient engine",
    "Acceleration is a partnership: fermentation volatiles recruit adults, adults inoculate yeasts, "
    "larvae fragment pulp, and short guts assimilate sugars before the patch disappears.",
    kicker="Decomposition partnership",
)

fly = get_species("fruit_fly")
metric_row(
    [
        (
            "Adult mass",
            f"{fly['adult_mass_g']*1000:.1f} mg ({fmt_range(fly['adult_mass_range_g'][0]*1000, fly['adult_mass_range_g'][1]*1000, 'mg')})",
        ),
        (
            "Gut passage",
            f"~{fly['gut_passage_hours']} h ({fmt_range(*fly['gut_passage_range_h'], 'h')})",
        ),
        ("Mass-specific BMR", f"{fly['mass_specific_bmr_w_per_kg']} W/kg"),
        ("Thermotype", fly["thermotype"].title()),
    ]
)

callout(
    "Flies are <strong>not</strong> primary cellulose digesters. Soft, microbe-active fruit is the niche. "
    "Speed comes from patch choice, microbial partners, fragmentation, and larval throughput."
)

st.markdown("### Five-stage pathway")
cols = st.columns(1)
for step in FLY_NUTRIENT_PATHWAYS:
    stage_card(step["stage"], step["title"], step["detail"])

left, right = st.columns(2)
with left:
    st.markdown("#### What gets broken down")
    st.markdown(
        """
| Substrate | Main processors | Products |
|-----------|-----------------|----------|
| Sucrose / hexoses | Yeast invertase + fly gut | Glucose/fructose → ATP, ethanol, CO2, organic acids |
| Soft fruit tissue | Larval enzymes + microbes | Amino acids, peptides, lipids |
| Microbial biomass | Larval digestion | Sterols, vitamins, protein |
"""
    )
with right:
    st.markdown("#### Why mammals differ here")
    st.markdown(
        """
Mice and rats also process food quickly *for vertebrates*, but they:
- Maintain ~37°C continuously (energetic overhead)
- Invest weeks in gestation + lactation per bout
- Rarely specialize on a single fermenting fruit patch the way *Drosophila* larvae do

Their nutrient "acceleration" is metabolic intensity + scavenger behavior, not 10-day generations.
"""
    )

st.markdown("### Coupled sugar–yeast–larva simulator")
st.caption(
    "Yeast grow on remaining sugar (Monod-like). Adult visits seed yeast. Larvae consume sugar and "
    "boost effective yeast access via fragmentation. Compare microbes-only vs fly-active patches."
)

c1, c2, c3 = st.columns(3)
with c1:
    sugar0 = st.slider("Starting sugar (mg)", 100, 3000, 1000, 50)
    hours = st.slider("Hours", 12, 120, 72, 6)
with c2:
    larvae = st.slider("Larvae", 0, 250, 50, 5)
    visits = st.slider("Adult visits / day", 0.0, 20.0, 6.0, 0.5)
with c3:
    y0 = st.slider("Initial yeast index", 0.2, 10.0, 1.0, 0.2)
    frag = st.slider("Fragmentation boost", 1.0, 2.5, 1.5, 0.05)

alone = nutrient_microbe_fly(
    hours, sugar0, initial_yeast=y0, fly_visits_per_day=0.0, n_larvae=0, fragmentation_boost=1.0
)
with_flies = nutrient_microbe_fly(
    hours,
    sugar0,
    initial_yeast=y0,
    fly_visits_per_day=visits,
    n_larvae=larvae,
    fragmentation_boost=frag,
)

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=alone["hour"],
        y=alone["sugar_mg"],
        name="Sugar — microbes only",
        line=dict(color="#8a7a55", width=3, dash="dot"),
    )
)
fig.add_trace(
    go.Scatter(
        x=with_flies["hour"],
        y=with_flies["sugar_mg"],
        name="Sugar — with flies",
        line=dict(color="#b86a1e", width=3),
        fill="tozeroy",
        fillcolor="rgba(184,106,30,0.12)",
    )
)
fig.add_trace(
    go.Scatter(
        x=with_flies["hour"],
        y=with_flies["yeast_index"],
        name="Yeast index — with flies",
        yaxis="y2",
        line=dict(color="#3f5f36", width=2.5),
    )
)
fig.update_layout(
    title="Sugar collapse and yeast amplification",
    xaxis_title="Hours",
    yaxis_title="Sugar (mg)",
    yaxis2=dict(title="Yeast index", overlaying="y", side="right", showgrid=False),
    legend=dict(orientation="h", y=1.12),
)
apply_layout(fig, height=480)
st.plotly_chart(fig, use_container_width=True)

h1 = half_life_hours(alone)
h2 = half_life_hours(with_flies)
k1, k2, k3 = st.columns(3)
k1.metric("Sugar half-life (microbes)", f"{h1:.0f} h" if h1 is not None else "> window")
k2.metric("Sugar half-life (with flies)", f"{h2:.0f} h" if h2 is not None else "> window")
if h1 and h2 and h2 > 0:
    k3.metric("Speed-up", f"{h1/h2:.1f}× faster half-life")
else:
    k3.metric("Speed-up", "n/a")

st.download_button(
    "Download simulation CSV",
    with_flies.to_csv(index=False),
    file_name="nutrient_yeast_fly_sim.csv",
    mime="text/csv",
)

with st.expander("Model assumptions"):
    st.markdown(
        """
- Yeast index is a dimensionless biomass proxy, not CFU/ml.
- Fragmentation multiplies yeast growth access, standing in for surface-area / oxygen effects.
- Parameters are tuned for teaching intuition (direction & relative magnitude), not fitted to a single experiment.
- Real fruit chemistry, humidity, and community composition add substantial variance.
"""
    )
