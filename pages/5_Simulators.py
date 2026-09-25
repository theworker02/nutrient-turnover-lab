"""Interactive multi-model simulators."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from labkit.species_data import SPECIES, get_species, whole_animal_bmr_w
from labkit.simulations import (
    doubling_time_days,
    half_life_hours,
    kleiber_curve,
    logistic_population,
    nutrient_microbe_fly,
    scenario_presets,
    stage_structured_flies,
)
from labkit.ui import apply_layout, callout, hero, inject_style

inject_style()

hero(
    "Interactive simulators",
    "Four sandboxes: coupled nutrient collapse with presets, multi-species logistic race across the "
    "expanded taxa set, a fly stage engine, and metabolic allometry from microbes to elephants.",
    kicker="Sandbox",
)

mode = st.radio(
    "Simulator",
    ["Nutrient collapse", "Population race", "Fly stages", "Metabolic scaling"],
    horizontal=True,
)

PALETTE = ["#b86a1e", "#3f5f36", "#6b4a3d", "#2f6b6b", "#8a5a2b", "#5c6b3d", "#7a4e6b", "#4a6b8a"]

if mode == "Nutrient collapse":
    callout(
        "Yeast grow on sugar (Monod-like); adult visits seed yeast; larvae consume sugar and raise "
        "fragmentation. Compare microbes-only vs fly-amplified trajectories."
    )
    presets = scenario_presets()
    preset_name = st.selectbox("Scenario preset", list(presets.keys()), index=0)
    if st.button("Apply preset", type="primary"):
        st.session_state["nut_preset"] = preset_name
    p = presets[st.session_state.get("nut_preset", preset_name)]

    c1, c2 = st.columns(2)
    with c1:
        sugar0 = st.slider("Sugar (mg)", 100, 3000, int(p["sugar_mg"]), 50)
        hours = st.slider("Hours", 12, 168, int(p["hours"]), 6)
        larvae = st.slider("Larvae", 0, 300, int(p["larvae"]), 5)
    with c2:
        visits = st.slider("Visits / day", 0.0, 24.0, float(p["visits"]), 0.5)
        y0 = st.slider("Initial yeast index", 0.2, 8.0, float(p["yeast0"]), 0.2)
        frag = st.slider("Fragmentation boost", 1.0, 2.5, 1.6, 0.1)

    with st.expander("Advanced rates"):
        y_growth = st.slider("Yeast growth / h", 0.05, 0.35, 0.15, 0.01)
        larva_use = st.slider("Larva sugar use each", 0.05, 0.6, 0.28, 0.01)
        seed = st.slider("Yeast seed per visit", 0.05, 1.0, 0.35, 0.05)

    base = nutrient_microbe_fly(
        hours,
        sugar0,
        y0,
        0.0,
        0,
        yeast_growth_per_h=y_growth,
        larva_use_each=larva_use,
        fragmentation_boost=1.0,
        fly_seed_per_visit=seed,
    )
    treat = nutrient_microbe_fly(
        hours,
        sugar0,
        y0,
        visits,
        larvae,
        yeast_growth_per_h=y_growth,
        larva_use_each=larva_use,
        fragmentation_boost=frag,
        fly_seed_per_visit=seed,
    )

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=base["hour"],
            y=base["fraction_sugar"],
            name="Microbes only",
            line=dict(color="#8a7a55", dash="dot", width=3),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=treat["hour"],
            y=treat["fraction_sugar"],
            name="With flies",
            line=dict(color="#b86a1e", width=3),
        )
    )
    fig.update_layout(title="Fraction of sugar remaining", xaxis_title="Hour", yaxis_title="Fraction", yaxis=dict(range=[0, 1.05]))
    apply_layout(fig, height=420)
    st.plotly_chart(fig, use_container_width=True)

    fig_y = go.Figure()
    fig_y.add_trace(go.Scatter(x=base["hour"], y=base["yeast_index"], name="Yeast · microbes only", line=dict(color="#8a7a55", dash="dot", width=2.5)))
    fig_y.add_trace(go.Scatter(x=treat["hour"], y=treat["yeast_index"], name="Yeast · with flies", line=dict(color="#3f5f36", width=2.5)))
    fig_y.update_layout(title="Yeast index over time", xaxis_title="Hour", yaxis_title="Yeast index")
    apply_layout(fig_y, height=360)
    st.plotly_chart(fig_y, use_container_width=True)

    h1, h2 = half_life_hours(base), half_life_hours(treat)
    c1, c2, c3 = st.columns(3)
    c1.metric("Half-life microbes", f"{h1:.0f} h" if h1 else "> window")
    c2.metric("Half-life with flies", f"{h2:.0f} h" if h2 else "> window")
    speedup = (h1 / h2) if (h1 and h2 and h2 > 0) else None
    c3.metric("Speedup", f"{speedup:.1f}×" if speedup else "—")
    st.download_button("CSV · with flies", treat.to_csv(index=False), "nutrient_sim.csv", "text/csv")

elif mode == "Population race":
    callout(
        "Default <em>r</em> values come from the species table. Shared <em>K</em> is a teaching "
        "abstraction—real niches differ wildly. Microbes need tiny N0 and often need a log-y axis."
    )
    default_race = ["fruit_fly", "bluebottle", "house_mouse", "zebrafish", "chicken", "domestic_cat"]
    choices = st.multiselect(
        "Competitors",
        list(SPECIES.keys()),
        default=[k for k in default_race if k in SPECIES],
        format_func=lambda k: f"{SPECIES[k]['common_name']} (r˜{SPECIES[k]['intrinsic_r_per_day']:g})",
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        days = st.slider("Days", 10, 730, 180, 5)
    with c2:
        k_shared = st.slider("Shared K", 50, 50000, 5000, 50)
    with c3:
        log_y = st.checkbox("Log Y axis", value=True)
        include_microbes = st.checkbox("Suggest microbe pair", value=False)

    if include_microbes:
        for mid in ("e_coli", "baker_yeast"):
            if mid not in choices:
                choices = list(choices) + [mid]

    if not choices:
        st.warning("Pick at least one competitor.")
    else:
        fig = go.Figure()
        summary = []
        for i, sid in enumerate(choices):
            s = get_species(sid)
            r_default = float(s["intrinsic_r_per_day"])
            # Cap slider range for extreme microbes
            r_hi = min(max(2.0, r_default * 1.5), 80.0) if r_default < 20 else min(80.0, r_default * 1.2)
            r_lo = max(1e-5, r_default / 50)
            step = max(1e-5, r_default / 40) if r_default < 1 else max(0.1, r_default / 50)
            r = st.slider(
                f"r · {s['common_name']}",
                float(r_lo),
                float(r_hi),
                float(r_default),
                float(step),
                key=f"r_{sid}",
                format="%.4f" if r_default < 1 else "%.2f",
            )
            if sid in ("e_coli", "baker_yeast"):
                n0 = 20.0
            elif sid in ("nematode",):
                n0 = 15.0
            elif s["adult_mass_g"] > 1e5:
                n0 = 2.0
            else:
                n0 = 8.0
            series = logistic_population(days, r=r, k=float(k_shared), n0=float(n0))
            fig.add_trace(
                go.Scatter(
                    x=series["day"],
                    y=series["population"],
                    name=s["common_name"],
                    line=dict(color=PALETTE[i % len(PALETTE)], width=3),
                )
            )
            summary.append(
                {
                    "Species": s["common_name"],
                    "Clade": s["clade"],
                    "r /day": r,
                    "Doubling (d)": round(doubling_time_days(r), 4),
                    "N0": n0,
                    "Final N": round(series["population"].iloc[-1], 1),
                    "Days to 50% K": int(series.loc[series["population"] >= 0.5 * k_shared, "day"].iloc[0])
                    if (series["population"] >= 0.5 * k_shared).any()
                    else None,
                }
            )
        fig.update_layout(
            title="Who approaches K first?",
            xaxis_title="Day",
            yaxis_title="N",
            yaxis_type="log" if log_y else "linear",
        )
        apply_layout(fig, height=500)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(summary, use_container_width=True, hide_index=True)
        st.caption(
            "E. coli and yeast can saturate K in hours–days at table r; elephants barely move. "
            "Shared K is pedagogical—do not read absolute N as real census sizes."
        )

elif mode == "Fly stages":
    callout("Temperature sets stage durations; density dependence clips larval survival.")
    c1, c2 = st.columns(2)
    with c1:
        temp = st.slider("Temperature °C", 15, 31, 25, key="st_temp")
        days = st.slider("Days", 15, 120, 50, key="st_days")
        epd = st.slider("Eggs/female/day", 5, 70, 28, key="st_epd")
    with c2:
        n0 = st.slider("Starting adult ♀", 1, 40, 5, key="st_n0")
        k_larv = st.slider("Larval K", 50, 3000, 500, 50, key="st_klarv")
        adult_s = st.slider("Adult daily survival", 0.8, 0.99, 0.92, 0.01, key="st_as")

    stages = stage_structured_flies(
        days,
        temp_c=float(temp),
        eggs_per_female_per_day=float(epd),
        starting_females=float(n0),
        k_larvae=float(k_larv),
        adult_survival_per_day=float(adult_s),
    )
    fig = go.Figure()
    for col, color in [
        ("eggs", "#d4a35c"),
        ("larvae", "#b86a1e"),
        ("pupae", "#6b4a3d"),
        ("adult_females", "#3f5f36"),
    ]:
        fig.add_trace(go.Scatter(x=stages["day"], y=stages[col], name=col, line=dict(color=color, width=2.5)))
    fig.update_layout(title="Stage counts", xaxis_title="Day", yaxis_title="Count")
    apply_layout(fig, height=460)
    st.plotly_chart(fig, use_container_width=True)

    m1, m2, m3 = st.columns(3)
    m1.metric("Peak larvae", f"{stages['larvae'].max():.0f}")
    m2.metric("Peak adult ♀", f"{stages['adult_females'].max():.0f}")
    m3.metric("Final total", f"{stages['total'].iloc[-1]:.0f}")
    st.download_button("CSV", stages.to_csv(index=False), "stages.csv", "text/csv")

else:
    callout(
        "Mammal reference curve BMR ˜ 3.4 M<sup>0.75</sup>. Overlay any teaching species—"
        "microbes and insects often sit off the placental line.",
    )
    show_ids = st.multiselect(
        "Plot species",
        list(SPECIES.keys()),
        default=[
            "e_coli",
            "baker_yeast",
            "fruit_fly",
            "bluebottle",
            "honey_bee",
            "zebrafish",
            "house_mouse",
            "chicken",
            "domestic_cat",
            "rabbit",
            "human",
            "african_elephant",
        ],
        format_func=lambda k: SPECIES[k]["common_name"],
    )
    y_mode = st.radio("Y axis", ["Whole-animal BMR (W)", "Mass-specific (W/kg)"], horizontal=True)

    curve = kleiber_curve(masses_g=np.logspace(-13, 7, 140))
    fig = go.Figure()
    if y_mode.startswith("Whole"):
        fig.add_trace(
            go.Scatter(
                x=curve["mass_g"],
                y=curve["whole_animal_bmr_w"],
                name="BMR ˜ 3.4 M^0.75",
                line=dict(color="#8a7a55", width=3),
            )
        )
        y_title = "Whole-animal BMR (W)"
    else:
        fig.add_trace(
            go.Scatter(
                x=curve["mass_g"],
                y=curve["mass_specific_w_per_kg"],
                name="Mass-specific from Kleiber",
                line=dict(color="#8a7a55", width=3, dash="dot"),
            )
        )
        y_title = "Mass-specific BMR (W/kg)"

    for i, sid in enumerate(show_ids):
        s = get_species(sid)
        if y_mode.startswith("Whole"):
            y = whole_animal_bmr_w(sid)
        else:
            y = s["mass_specific_bmr_w_per_kg"]
        fig.add_trace(
            go.Scatter(
                x=[s["adult_mass_g"]],
                y=[y],
                mode="markers+text",
                text=[s["common_name"]],
                textposition="top center",
                marker=dict(size=13, color=PALETTE[i % len(PALETTE)]),
                name=s["common_name"],
            )
        )
    fig.update_layout(
        xaxis_type="log",
        yaxis_type="log",
        xaxis_title="Mass (g)",
        yaxis_title=y_title,
        title="Allometry explorer",
    )
    apply_layout(fig, height=540)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "Whole-animal energy rises sublinearly with mass. Flies combine high **per-kg** burn with tiny "
        "**absolute** needs—enough to race through a sugar patch before a mouse weans a litter, and "
        "long before an elephant calves."
    )
