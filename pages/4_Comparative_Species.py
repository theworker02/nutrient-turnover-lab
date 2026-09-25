"""Comparative physiology — gallery with richer visuals and detail."""

from __future__ import annotations

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from labkit.species_data import SPECIES, get_species, species_dataframe, whole_animal_bmr_w
from labkit.simulations import doubling_time_days, kleiber_curve
from labkit.ui import callout, fmt_range, hero, inject_style
from labkit.metrics import metric_row
from labkit.widgets import CLADE_COLORS, section_header, vivid_layout

inject_style()

N_SPECIES = len(SPECIES)

hero(
    "Comparative species gallery",
    f"A {N_SPECIES}-taxon studio: dual species dossiers, vivid radar overlays, parallel coordinates, "
    "and metabolic landscapes from E. coli to elephants.",
    kicker="Comparative physiology",
)

df = species_dataframe()
ids = list(SPECIES.keys())
labels = {k: f"{SPECIES[k]['common_name']} ({SPECIES[k]['scientific_name']})" for k in ids}
clades = sorted({SPECIES[k]["clade"] for k in ids})

filter_clades = st.multiselect("Filter by clade", clades, default=clades)
visible_ids = [k for k in ids if SPECIES[k]["clade"] in filter_clades] or ids
df_v = df[df["id"].isin(visible_ids)]

metric_row(
    [
        ("Visible species", str(len(visible_ids))),
        ("Clades shown", str(len({SPECIES[k]["clade"] for k in visible_ids}))),
        ("Fastest generation", f"{df_v['Generation time (days)'].min():.3g} days"),
        ("Slowest generation", f"{df_v['Generation time (days)'].max():.3g} days"),
    ]
)

section_header("Dossier", "Pick two species to dissect")
sel_a, sel_b = st.columns(2)
with sel_a:
    a_id = st.selectbox("Species A", visible_ids, index=0, format_func=lambda k: labels[k], key="cmp_a")
if "house_mouse" in visible_ids and a_id != "house_mouse":
    b_default = visible_ids.index("house_mouse")
elif len(visible_ids) > 1:
    b_default = 0 if visible_ids[0] != a_id else 1
else:
    b_default = 0
with sel_b:
    b_id = st.selectbox(
        "Species B",
        visible_ids,
        index=min(b_default, len(visible_ids) - 1),
        format_func=lambda k: labels[k],
        key="cmp_b",
    )
a, b = get_species(a_id), get_species(b_id)


def dossier(s: dict, accent: str) -> None:
    mass_r = fmt_range(*s["adult_mass_range_g"], "g")
    gen_r = fmt_range(*s["generation_range_days"], "d")
    fec_r = fmt_range(*s["lifetime_fecundity_range"])
    life_r = fmt_range(*s["lifespan_range_days"], "d")
    gut_r = fmt_range(*s["gut_passage_range_h"], "h")
    dbl = doubling_time_days(s["intrinsic_r_per_day"])
    st.markdown(
        f"""
        <div class="species-panel" style="border-top: 4px solid {accent};">
          <div class="section-label">{s['clade']} · {s['thermotype']}</div>
          <h3>{s['common_name']}</h3>
          <div class="species-meta"><em>{s['scientific_name']}</em> · {s['r_or_k']}</div>
          <div class="stat-grid">
            <div class="stat-cell"><div class="lbl">Mass</div><div class="val">{s['adult_mass_g']:g} g</div><span class="range-pill">{mass_r}</span></div>
            <div class="stat-cell"><div class="lbl">Generation</div><div class="val">{s['generation_days']:g} d</div><span class="range-pill">{gen_r}</span></div>
            <div class="stat-cell"><div class="lbl">Lifetime fecundity</div><div class="val">{s['lifetime_fecundity']}</div><span class="range-pill">{fec_r}</span></div>
            <div class="stat-cell"><div class="lbl">Lifespan</div><div class="val">{s['lifespan_days']} d</div><span class="range-pill">{life_r}</span></div>
            <div class="stat-cell"><div class="lbl">BMR / kg</div><div class="val">{s['mass_specific_bmr_w_per_kg']} W</div></div>
            <div class="stat-cell"><div class="lbl">Gut passage</div><div class="val">{s['gut_passage_hours']} h</div><span class="range-pill">{gut_r}</span></div>
            <div class="stat-cell"><div class="lbl">Intrinsic r</div><div class="val">{s['intrinsic_r_per_day']}/d</div></div>
            <div class="stat-cell"><div class="lbl">Doubling</div><div class="val">{dbl:.3g} d</div></div>
          </div>
          <p style="margin:0.55rem 0 0;color:#3a4535;line-height:1.45;"><strong>Digestion.</strong> {s['digestive_strategy']}</p>
          <p style="margin:0.45rem 0 0;color:#3a4535;line-height:1.45;"><strong>Nutrient role.</strong> {s['nutrient_role']}</p>
          <p style="margin:0.45rem 0 0;color:#5a6454;font-size:0.92rem;line-height:1.45;">{s['notes']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander(f"Sources — {s['common_name']}"):
        for c in s["citations"]:
            st.markdown(f"- {c}")


col_a, col_b = st.columns(2)
with col_a:
    dossier(a, CLADE_COLORS.get(a["clade"], "#b86a1e"))
with col_b:
    dossier(b, CLADE_COLORS.get(b["clade"], "#3f5f36"))

section_header("Ratios", "A ÷ B at a glance")
ratios = [
    ("Mass", f"{a['adult_mass_g']/b['adult_mass_g']:.2e}"),
    ("Generation", f"{a['generation_days']/b['generation_days']:.2f}×"),
    ("Fecundity", f"{a['lifetime_fecundity']/max(b['lifetime_fecundity'],1):.2f}×"),
    ("Gut", f"{(a['gut_passage_hours'] or 1e-3)/max(b['gut_passage_hours'] or 1e-3,1e-6):.2f}×"),
    ("r", f"{a['intrinsic_r_per_day']/max(b['intrinsic_r_per_day'],1e-12):.2e}"),
    ("BMR/kg", f"{a['mass_specific_bmr_w_per_kg']/b['mass_specific_bmr_w_per_kg']:.2f}×"),
]
chips = "".join(
    f'<div class="ratio-chip"><div class="lbl">{lab}</div><div class="val">{val}</div></div>'
    for lab, val in ratios
)
st.markdown(f'<div class="ratio-strip">{chips}</div>', unsafe_allow_html=True)

# Detail comparison bars
section_header("Detail bars", "Log-scaled trait duel")
traits = {
    "Adult mass (g)": (a["adult_mass_g"], b["adult_mass_g"]),
    "Generation (d)": (a["generation_days"], b["generation_days"]),
    "Fecundity": (max(a["lifetime_fecundity"], 0.1), max(b["lifetime_fecundity"], 0.1)),
    "BMR W/kg": (a["mass_specific_bmr_w_per_kg"], b["mass_specific_bmr_w_per_kg"]),
    "Gut (h)": (max(a["gut_passage_hours"], 0.01), max(b["gut_passage_hours"], 0.01)),
}
fig_duel = go.Figure()
fig_duel.add_trace(
    go.Bar(
        name=a["common_name"],
        x=list(traits.keys()),
        y=[v[0] for v in traits.values()],
        marker_color="#b86a1e",
    )
)
fig_duel.add_trace(
    go.Bar(
        name=b["common_name"],
        x=list(traits.keys()),
        y=[v[1] for v in traits.values()],
        marker_color="#3f5f36",
    )
)
fig_duel.update_layout(barmode="group", yaxis_type="log", title="Trait duel (log y)")
vivid_layout(fig_duel, height=400)
st.plotly_chart(fig_duel, use_container_width=True)

section_header("Radar", "Normalized life-history signatures")
radar_extra = st.multiselect(
    "Overlay more species",
    [k for k in visible_ids if k not in (a_id, b_id)],
    default=[],
    format_func=lambda k: SPECIES[k]["common_name"],
    max_selections=5,
)
callout(
    f"Axes are log-scaled then min–max normalized across all {N_SPECIES} species. "
    "High = relatively extreme within this teaching set."
)


def radar_values(species_id: str) -> dict[str, float]:
    s = SPECIES[species_id]
    return {
        "Mass": np.log10(max(s["adult_mass_g"], 1e-15)),
        "Gen. speed": -np.log10(max(s["generation_days"], 1e-6)),
        "Fecundity": np.log10(max(s["lifetime_fecundity"], 1)),
        "BMR/kg": np.log10(max(s["mass_specific_bmr_w_per_kg"], 1e-3)),
        "Gut speed": -np.log10(max(s["gut_passage_hours"], 0.01)),
        "r speed": np.log10(max(s["intrinsic_r_per_day"], 1e-6)),
    }


keys_radar = list(radar_values("fruit_fly").keys())
matrix = {k: [] for k in keys_radar}
for sid in ids:
    rv = radar_values(sid)
    for k in keys_radar:
        matrix[k].append(rv[k])
mins = {k: min(v) for k, v in matrix.items()}
maxs = {k: max(v) for k, v in matrix.items()}


def norm_radar(species_id: str) -> list[float]:
    rv = radar_values(species_id)
    return [(rv[k] - mins[k]) / (maxs[k] - mins[k] or 1.0) for k in keys_radar]


palette = ["#b86a1e", "#3f5f36", "#2f6b6b", "#c45c3a", "#7a4e6b", "#d4a35c", "#4a6b8a"]
fig_r = go.Figure()
for i, sid in enumerate([a_id, b_id] + radar_extra):
    vals = norm_radar(sid)
    fig_r.add_trace(
        go.Scatterpolar(
            r=vals + [vals[0]],
            theta=keys_radar + [keys_radar[0]],
            fill="toself",
            name=SPECIES[sid]["common_name"],
            line=dict(color=palette[i % len(palette)], width=2),
            opacity=0.7,
        )
    )
fig_r.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1], gridcolor="rgba(36,61,40,0.12)")))
vivid_layout(fig_r, height=540, title="Life-history radar")
st.plotly_chart(fig_r, use_container_width=True)

section_header("Gallery maps", "Where everyone sits")
m1, m2 = st.columns(2)
with m1:
    fig_land = px.scatter(
        df_v,
        x="Generation time (days)",
        y="Mass-specific BMR (W/kg)",
        size="Lifetime fecundity",
        color="Clade",
        hover_name="Common name",
        hover_data=["Scientific name", "Strategy", "r (1/day)"],
        log_x=True,
        log_y=True,
        color_discrete_map=CLADE_COLORS,
        title="Metabolism × generation",
    )
    vivid_layout(fig_land, height=440)
    st.plotly_chart(fig_land, use_container_width=True)
with m2:
    fig_sun = px.sunburst(
        df_v,
        path=["Clade", "Thermotype", "Common name"],
        values="Adult mass (g)",
        color="Generation time (days)",
        color_continuous_scale=["#b86a1e", "#ebe1c8", "#3f5f36"],
        title="Clade → thermotype → species",
    )
    vivid_layout(fig_sun, height=440)
    st.plotly_chart(fig_sun, use_container_width=True)

section_header("Parallel coordinates", "Multi-trait fingerprints")
pc = df_v.copy()
pc["log_mass"] = np.log10(pc["Adult mass (g)"].clip(lower=1e-15))
pc["log_gen"] = np.log10(pc["Generation time (days)"].clip(lower=1e-6))
pc["log_fec"] = np.log10(pc["Lifetime fecundity"].clip(lower=0.1))
pc["log_bmr"] = np.log10(pc["Mass-specific BMR (W/kg)"].clip(lower=1e-3))
fig_pc = go.Figure(
    data=go.Parcoords(
        line=dict(
            color=pc["Generation time (days)"],
            colorscale=[[0, "#b86a1e"], [0.5, "#d4a35c"], [1, "#3f5f36"]],
            showscale=True,
            colorbar=dict(title="Gen (d)"),
        ),
        dimensions=[
            dict(label="log mass", values=pc["log_mass"]),
            dict(label="log gen", values=pc["log_gen"]),
            dict(label="log fecundity", values=pc["log_fec"]),
            dict(label="log BMR/kg", values=pc["log_bmr"]),
            dict(label="r /day", values=pc["r (1/day)"]),
        ],
    )
)
vivid_layout(fig_pc, height=420, title="Brush the axes to isolate life-history clusters")
st.plotly_chart(fig_pc, use_container_width=True)

section_header("Table", "Full comparison with ranges")
show = df_v.drop(columns=["id"])
st.dataframe(show, use_container_width=True, hide_index=True)
st.download_button("Download CSV", show.to_csv(index=False), "species_comparison.csv", "text/csv")

section_header("Allometry", "Whole-animal energy vs size")
curve = kleiber_curve(masses_g=np.logspace(-13, 7, 120))
fig = px.line(curve, x="mass_g", y="whole_animal_bmr_w", log_x=True, log_y=True)
fig.update_traces(name="Mammal ~ M^0.75", line_color="#8a7a55", showlegend=True)
xs, ys, texts, colors = [], [], [], []
for sid in visible_ids:
    s = SPECIES[sid]
    xs.append(s["adult_mass_g"])
    ys.append(whole_animal_bmr_w(sid))
    texts.append(s["common_name"])
    colors.append(CLADE_COLORS.get(s["clade"], "#b86a1e"))
fig.add_scatter(
    x=xs,
    y=ys,
    mode="markers+text",
    text=texts,
    textposition="top center",
    marker=dict(size=13, color=colors, line=dict(width=1, color="white")),
    name="Species",
)
fig.update_layout(xaxis_title="Mass (g)", yaxis_title="Whole-animal BMR (W)", title="Kleiber context")
vivid_layout(fig, height=520)
st.plotly_chart(fig, use_container_width=True)

section_header("Essays", "One paragraph per species")
essays = {
    "fruit_fly": "Yeast-rich fruit specialists. Acceleration = vectoring + fragmentation + short-gut throughput.",
    "house_mouse": "Small endotherm with rapid litters—still locked to ~2–3 month generations.",
    "brown_rat": "Larger refuse throughput than mice; mammalian pregnancy timescales remain.",
    "nematode": "~3-day generations on bacteria; bridges microbes and insects on the speed axis.",
    "baker_yeast": "First sugar processor on fruit; ~90 min doubling in rich medium; fly mutualist.",
    "rabbit": "Hindgut fermentation + cecotrophy; boom–bust herbivore demography.",
    "human": "Slow-life pole. Cooking/fermentation are external digestion; culture beats gut speed.",
    "e_coli": "Prokaryote extreme (~20 min rich broth). Fruit patches are harsher; yeasts often dominate volatiles.",
    "bluebottle": "Necrophagous fly guild—protein patches, huge clutches, forensic timing tables.",
    "honey_bee": "Social contrast: ~21 d brood, but colony/caste demography ≠ solitary r.",
    "zebrafish": "Fast vertebrate model: external eggs, huge clutches, month-scale generation.",
    "chicken": "Avian r-strategist: near-daily eggs, 21-day incubation—still far slower than flies.",
    "domestic_cat": "Mid carnivore mammal: year-scale generation between rats and elephants.",
    "african_elephant": "Extreme K: 22-month gestation, landscape hindgut fermentation.",
}
essay_ids = [k for k in ids if k in essays]
tabs = st.tabs([SPECIES[k]["common_name"] for k in essay_ids])
for tab, key in zip(tabs, essay_ids):
    with tab:
        s = SPECIES[key]
        accent = CLADE_COLORS.get(s["clade"], "#b86a1e")
        st.markdown(
            f"<div class='callout' style='border-left-color:{accent}'>{essays[key]}</div>",
            unsafe_allow_html=True,
        )
        st.caption(
            f"{s['scientific_name']} · {s['r_or_k']} · r ≈ {s['intrinsic_r_per_day']}/day · "
            f"gen {fmt_range(*s['generation_range_days'], 'd')}"
        )
        d1, d2 = st.columns(2)
        d3, d4 = st.columns(2)
        d1.metric("Mass", f"{s['adult_mass_g']:g} g")
        d2.metric("Generation", f"{s['generation_days']:g} d")
        d3.metric("Fecundity", f"{s['lifetime_fecundity']}")
        d4.metric("BMR/kg", f"{s['mass_specific_bmr_w_per_kg']}")
