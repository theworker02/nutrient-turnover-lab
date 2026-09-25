"""Reproduction speed — colorful multi-chart exhibit."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from labkit.species_data import REPRODUCTION_DRIVERS, SPECIES, get_species, species_dataframe
from labkit.simulations import (
    development_temperature_curve,
    doubling_time_days,
    drosophila_development_days,
    exponential_generations,
    generations_in_window,
    logistic_population,
    stage_structured_flies,
)
from labkit.ui import callout, hero, inject_style, stage_card
from labkit.metrics import metric_row
from labkit.widgets import CLADE_COLORS, section_header, vivid_layout

inject_style()

hero(
    "Why they multiply so fast",
    "Colorful charts of temperature clocks, stage overlap, generation stacking, and fecundity—"
    "showing why one mated female becomes a cloud while mammals are still gestating.",
    kicker="Life-history speed",
)

fly = get_species("fruit_fly")
mouse = get_species("house_mouse")
bee = get_species("honey_bee")
coli = get_species("e_coli")

metric_row(
    [
        ("Fly generation", f"{fly['generation_days']:.0f} days"),
        ("Lifetime eggs", f"~{fly['lifetime_fecundity']}"),
        ("vs house mouse", f"{mouse['generation_days']/fly['generation_days']:.0f}× slower"),
        ("vs honey bee brood", f"{bee['generation_days']/fly['generation_days']:.1f}×"),
        ("E. coli doubling", f"~{coli['generation_days']*24*60:.0f} min"),
    ]
)

callout(
    "Flies win on <strong>rate</strong>—many generations and many eggs on a short clock. "
    "Microbes are faster still; vertebrates trade speed for size, care, and endothermy."
)

section_header("Drivers", "Five reasons the boom happens")
for d in REPRODUCTION_DRIVERS:
    stage_card("Driver", d["driver"], d["explanation"])

section_header("Generation stacking", "How many generations fit in a season?")
window = st.slider("Calendar window (days)", 30, 365, 90, 15, key="mul_window")
compare_ids = st.multiselect(
    "Species",
    list(SPECIES.keys()),
    default=[
        "e_coli",
        "baker_yeast",
        "fruit_fly",
        "bluebottle",
        "nematode",
        "honey_bee",
        "zebrafish",
        "house_mouse",
        "chicken",
        "domestic_cat",
        "human",
        "african_elephant",
    ],
    format_func=lambda k: SPECIES[k]["common_name"],
)
gen_rows = []
for sid in compare_ids:
    s = SPECIES[sid]
    n_gen = generations_in_window(window, s["generation_days"])
    gen_rows.append(
        {
            "Common name": s["common_name"],
            "Clade": s["clade"],
            "Generation (d)": s["generation_days"],
            f"Gens in {window} d": round(n_gen, 2),
            "Doubling from r (d)": round(doubling_time_days(s["intrinsic_r_per_day"]), 3),
            "r": s["intrinsic_r_per_day"],
        }
    )
gen_df = pd.DataFrame(gen_rows).sort_values(f"Gens in {window} d", ascending=True)

gcol1, gcol2 = st.columns([1.35, 1])
with gcol1:
    fig_g = px.bar(
        gen_df,
        x=f"Gens in {window} d",
        y="Common name",
        orientation="h",
        color="Clade",
        color_discrete_map=CLADE_COLORS,
        title=f"Generations in {window} days",
        log_x=True,
    )
    vivid_layout(fig_g, height=max(400, 30 * len(gen_df) + 100))
    st.plotly_chart(fig_g, use_container_width=True)
with gcol2:
    fig_pie = px.pie(
        gen_df.tail(min(8, len(gen_df))),
        names="Common name",
        values=f"Gens in {window} d",
        color="Common name",
        color_discrete_sequence=px.colors.qualitative.Bold,
        title="Share of stacked gens (top slice)",
        hole=0.45,
    )
    vivid_layout(fig_pie, height=400)
    st.plotly_chart(fig_pie, use_container_width=True)

st.dataframe(gen_df.sort_values(f"Gens in {window} d", ascending=False), use_container_width=True, hide_index=True)

section_header("Temperature clock", "Ectotherm development in color")
temp = st.slider("Ambient temperature (°C)", 15, 31, 25, key="mul_temp")
timing = drosophila_development_days(temp)
metric_row(
    [
        ("Egg stage", f"{timing['egg_days']:.1f} days"),
        ("Larva stage", f"{timing['larva_days']:.1f} days"),
        ("Pupa stage", f"{timing['pupa_days']:.1f} days"),
        ("Egg → adult", f"{timing['total_days']:.1f} days"),
        ("Pre-oviposition", f"{timing['adult_preoviposition_days']:.1f} days"),
    ]
)

curve = development_temperature_curve()
fig_t = make_subplots(specs=[[{"secondary_y": False}]])
fig_t.add_trace(
    go.Scatter(
        x=curve["temp_c"],
        y=curve["total_days"],
        name="Egg→adult",
        line=dict(color="#b86a1e", width=4),
        fill="tozeroy",
        fillcolor="rgba(184,106,30,0.18)",
    )
)
fig_t.add_trace(
    go.Scatter(
        x=curve["temp_c"],
        y=curve["larva_days"],
        name="Larva",
        line=dict(color="#3f5f36", width=2.5, dash="dot"),
    )
)
fig_t.add_trace(
    go.Scatter(
        x=curve["temp_c"],
        y=curve["pupa_days"],
        name="Pupa",
        line=dict(color="#2f6b6b", width=2.5, dash="dash"),
    )
)
fig_t.add_trace(
    go.Scatter(
        x=curve["temp_c"],
        y=curve["egg_days"],
        name="Egg",
        line=dict(color="#d4a35c", width=2),
    )
)
fig_t.add_vline(x=temp, line_dash="dash", line_color="#7a4e6b", line_width=2)
fig_t.add_annotation(
    x=temp,
    y=timing["total_days"],
    text=f"{timing['total_days']:.1f} d @ {temp}°C",
    showarrow=True,
    arrowhead=2,
    bgcolor="rgba(255,252,245,0.9)",
)
fig_t.update_layout(title="Stage durations vs temperature", xaxis_title="°C", yaxis_title="Days")
vivid_layout(fig_t, height=440)
st.plotly_chart(fig_t, use_container_width=True)

# Stage pie at selected temp
pie_df = pd.DataFrame(
    {
        "Stage": ["Egg", "Larva", "Pupa"],
        "Days": [timing["egg_days"], timing["larva_days"], timing["pupa_days"]],
    }
)
p_a, p_b = st.columns(2)
with p_a:
    fig_sp = px.pie(
        pie_df,
        names="Stage",
        values="Days",
        color="Stage",
        color_discrete_map={"Egg": "#d4a35c", "Larva": "#b86a1e", "Pupa": "#6b4a3d"},
        title=f"Time budget inside {timing['total_days']:.1f} d cycle",
        hole=0.4,
    )
    vivid_layout(fig_sp, height=360)
    st.plotly_chart(fig_sp, use_container_width=True)
with p_b:
    # Heatmap: generations vs temp for fly-like organism
    temps = np.arange(16, 31)
    windows = [30, 60, 90, 120, 180]
    heat = []
    for w in windows:
        row = []
        for t in temps:
            tot = drosophila_development_days(float(t))["total_days"]
            row.append(w / tot)
        heat.append(row)
    fig_h = go.Figure(
        data=go.Heatmap(
            z=heat,
            x=temps,
            y=[f"{w} d" for w in windows],
            colorscale=[[0, "#ebe1c8"], [0.35, "#d4a35c"], [0.7, "#b86a1e"], [1, "#3f5f36"]],
            colorbar=dict(title="Gens"),
        )
    )
    fig_h.update_layout(title="Fly-like gens vs temp — season", xaxis_title="°C")
    vivid_layout(fig_h, height=360)
    st.plotly_chart(fig_h, use_container_width=True)

section_header("Stage-structured boom", "Eggs → larvae → pupae → adults")
s1, s2, s3 = st.columns(3)
with s1:
    days = st.slider("Days", 20, 120, 60, 5, key="mul_days")
    n0 = st.slider("Starting ♀ adults", 1, 50, 5, key="mul_n0")
with s2:
    epd = st.slider("Eggs / ♀ / day", 5, 80, 30, 5, key="mul_epd")
    k_larv = st.slider("Larval K", 50, 2000, 600, 50, key="mul_k")
with s3:
    egg_s = st.slider("Egg survival", 0.2, 1.0, 0.7, 0.05, key="mul_es")
    adult_s = st.slider("Adult daily survival", 0.8, 0.99, 0.93, 0.01, key="mul_as")

stages = stage_structured_flies(
    days,
    temp_c=float(temp),
    eggs_per_female_per_day=float(epd),
    egg_survival=float(egg_s),
    adult_survival_per_day=float(adult_s),
    starting_females=float(n0),
    k_larvae=float(k_larv),
)

fig_s = go.Figure()
fills = {
    "eggs": ("Eggs", "rgba(212,163,92,0.85)"),
    "larvae": ("Larvae", "rgba(184,106,30,0.85)"),
    "pupae": ("Pupae", "rgba(196,92,58,0.8)"),
    "adult_females": ("Adult females", "rgba(63,95,54,0.85)"),
}
for col, (name, fill) in fills.items():
    fig_s.add_trace(
        go.Scatter(
            x=stages["day"],
            y=stages[col],
            name=name,
            stackgroup="one",
            mode="lines",
            line=dict(width=0.5, color=fill),
            fillcolor=fill,
        )
    )
fig_s.update_layout(title="Stacked stage structure", xaxis_title="Day", yaxis_title="Count")
vivid_layout(fig_s, height=460)
st.plotly_chart(fig_s, use_container_width=True)

# Line overlay (non-stacked) for clarity
fig_lines = go.Figure()
colors_line = {
    "eggs": "#d4a35c",
    "larvae": "#b86a1e",
    "pupae": "#c45c3a",
    "adult_females": "#3f5f36",
    "total": "#7a4e6b",
}
for col, color in colors_line.items():
    fig_lines.add_trace(
        go.Scatter(
            x=stages["day"],
            y=stages[col],
            name=col.replace("_", " ").title(),
            line=dict(color=color, width=3 if col != "total" else 2.5),
        )
    )
fig_lines.update_layout(title="Stage trajectories (unstacked)", xaxis_title="Day", yaxis_title="Count")
vivid_layout(fig_lines, height=400)
st.plotly_chart(fig_lines, use_container_width=True)

metric_row(
    [
        ("Peak larvae", f"{stages['larvae'].max():.0f}"),
        ("Peak adult females", f"{stages['adult_females'].max():.0f}"),
        ("Final total", f"{stages['total'].iloc[-1]:.0f}"),
    ]
)
st.download_button("Download stage CSV", stages.to_csv(index=False), "fly_stages.csv", "text/csv")

section_header("Compounding vs ceiling", "Boom math meets carrying capacity")
g1, g2 = st.columns(2)
with g1:
    gens = st.slider("Generations", 1, 12, 8, key="mul_gens")
    daus = st.slider("Surviving daughters / ♀", 1.0, 20.0, 5.0, 0.5, key="mul_daus")
    boom = exponential_generations(gens, daus, survival=0.7)
    fig_b = go.Figure()
    fig_b.add_trace(
        go.Scatter(
            x=boom["generation"],
            y=boom["females"],
            mode="lines+markers",
            line=dict(color="#b86a1e", width=4),
            marker=dict(size=10, color="#d4a35c", line=dict(width=2, color="#b86a1e")),
            fill="tozeroy",
            fillcolor="rgba(184,106,30,0.2)",
            name="Females",
        )
    )
    fig_b.update_layout(title="Female-lineage boom", xaxis_title="Generation", yaxis_title="Females", yaxis_type="log")
    vivid_layout(fig_b, height=380)
    st.plotly_chart(fig_b, use_container_width=True)
    st.caption(f"After {gens} gens → {boom['females'].iloc[-1]:,.0f} females (toy lineage, log y).")
with g2:
    r = st.slider("Logistic r (1/day)", 0.05, 0.8, float(fly["intrinsic_r_per_day"]), 0.01, key="mul_r")
    k = st.slider("Carrying capacity", 50, 5000, 800, 50, key="mul_cap")
    pop = logistic_population(60, r=r, k=float(k), n0=10.0)
    fig_l = go.Figure()
    fig_l.add_trace(
        go.Scatter(
            x=pop["day"],
            y=pop["population"],
            line=dict(color="#3f5f36", width=4),
            fill="tozeroy",
            fillcolor="rgba(63,95,54,0.22)",
            name="N(t)",
        )
    )
    fig_l.add_hline(y=k, line_dash="dash", line_color="#c45c3a", line_width=2, annotation_text="K")
    fig_l.update_layout(title="Logistic ceiling on one patch", xaxis_title="Day", yaxis_title="Flies")
    vivid_layout(fig_l, height=380)
    st.plotly_chart(fig_l, use_container_width=True)

section_header("Across the set", "Speed, output, and mass")
df = species_dataframe()
fig_sc = px.scatter(
    df,
    x="Generation time (days)",
    y="Lifetime fecundity",
    size="Adult mass (g)",
    color="Clade",
    hover_name="Common name",
    hover_data=["Scientific name", "r (1/day)", "Strategy"],
    log_x=True,
    log_y=True,
    color_discrete_map=CLADE_COLORS,
    title="Generation vs fecundity — bubble = mass",
)
fly_row = df[df["id"] == "fruit_fly"].iloc[0]
fig_sc.add_annotation(
    x=fly_row["Generation time (days)"],
    y=max(fly_row["Lifetime fecundity"], 1),
    text="Fruit fly",
    showarrow=True,
    arrowhead=2,
    ax=50,
    ay=-40,
    bgcolor="rgba(255,252,245,0.9)",
    font=dict(color="#b86a1e", size=13),
)
vivid_layout(fig_sc, height=480)
st.plotly_chart(fig_sc, use_container_width=True)

# Intrinsic r bar
df_r = df.sort_values("r (1/day)")
fig_rbar = px.bar(
    df_r,
    x="r (1/day)",
    y="Common name",
    orientation="h",
    color="Clade",
    color_discrete_map=CLADE_COLORS,
    title="Intrinsic growth rate r (1/day) — log x",
    log_x=True,
)
vivid_layout(fig_rbar, height=max(420, 28 * len(df_r) + 100))
st.plotly_chart(fig_rbar, use_container_width=True)

df_f = df.sort_values("Lifetime fecundity")
fig_f = px.bar(
    df_f,
    x="Lifetime fecundity",
    y="Common name",
    orientation="h",
    error_x=df_f["Fecundity high"] - df_f["Lifetime fecundity"],
    error_x_minus=df_f["Lifetime fecundity"] - df_f["Fecundity low"],
    color="Clade",
    color_discrete_map=CLADE_COLORS,
    title="Lifetime offspring (♀ range) — log x",
    log_x=True,
)
vivid_layout(fig_f, height=max(420, 28 * len(df_f) + 100))
st.plotly_chart(fig_f, use_container_width=True)
st.caption(
    'Honey-bee workers are sterile here (fecundity ≈ 1); E. coli "fecundity" is fission (1→2)—speed lives in generation time.'
)
