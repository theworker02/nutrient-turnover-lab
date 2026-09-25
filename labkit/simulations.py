"""Simulation helpers for population growth, development, and nutrient turnover."""

from __future__ import annotations

import numpy as np
import pandas as pd


def logistic_population(
    days: int,
    r: float,
    k: float,
    n0: float = 10.0,
) -> pd.DataFrame:
    """Discrete logistic growth: N_{t+1} = N_t + r N_t (1 - N_t/K)."""
    n = float(n0)
    rows = []
    for d in range(days + 1):
        rows.append({"day": d, "population": n})
        n = max(0.0, n + r * n * (1.0 - n / k))
    return pd.DataFrame(rows)


def exponential_generations(
    generations: int,
    offspring_per_female: float,
    starting_females: float = 1.0,
    survival: float = 0.5,
) -> pd.DataFrame:
    """Female-lineage boom across discrete generations."""
    f = float(starting_females)
    rows = []
    for g in range(generations + 1):
        rows.append({"generation": g, "females": f, "total_approx": f * 2})
        f = f * offspring_per_female * survival
    return pd.DataFrame(rows)


def drosophila_development_days(temp_c: float) -> dict[str, float]:
    """Approximate D. melanogaster stage durations vs temperature (°C).

    Piecewise fit inspired by published developmental timing trends:
    slow near 16–18°C, ~10 d total near 25°C, faster near 28°C, then heat stress.
    Educational—not a rearing calculator for critical experiments.
    """
    t = float(np.clip(temp_c, 14.0, 32.0))

    # Total egg-to-adult days (empirical-ish curve)
    if t < 18:
        total = 28 - 1.4 * (t - 14)
    elif t < 25:
        total = 19 - (19 - 10) * (t - 18) / 7
    elif t <= 28:
        total = 10 - (10 - 7.5) * (t - 25) / 3
    else:
        total = 7.5 + 1.2 * (t - 28)  # heat stress slows/impedes

    total = float(np.clip(total, 7.0, 30.0))
    # Stage fractions roughly stable with temperature
    egg = total * 0.10
    larva = total * 0.42
    pupa = total * 0.48
    return {
        "temp_c": t,
        "egg_days": egg,
        "larva_days": larva,
        "pupa_days": pupa,
        "total_days": total,
        "adult_preoviposition_days": 1.0 + max(0.0, (25 - t) * 0.08),
    }


def development_temperature_curve(temps: np.ndarray | None = None) -> pd.DataFrame:
    if temps is None:
        temps = np.linspace(15, 31, 33)
    rows = [drosophila_development_days(float(t)) for t in temps]
    return pd.DataFrame(rows)


def stage_structured_flies(
    days: int,
    temp_c: float = 25.0,
    eggs_per_female_per_day: float = 25.0,
    egg_survival: float = 0.7,
    larva_survival: float = 0.6,
    pupa_survival: float = 0.8,
    adult_survival_per_day: float = 0.92,
    starting_females: float = 5.0,
    k_larvae: float = 500.0,
) -> pd.DataFrame:
    """Simple stage-structured Drosophila model (females only for breeding).

    Transitions use mean stage durations from the temperature helper.
    Density dependence acts on larval survival via carrying capacity.
    """
    timing = drosophila_development_days(temp_c)
    # Daily transition probabilities ≈ 1/duration
    p_egg = 1.0 / max(timing["egg_days"], 0.5)
    p_larva = 1.0 / max(timing["larva_days"], 0.5)
    p_pupa = 1.0 / max(timing["pupa_days"], 0.5)

    eggs = 0.0
    larvae = 0.0
    pupae = 0.0
    adults = float(starting_females)

    rows = []
    for d in range(days + 1):
        rows.append(
            {
                "day": d,
                "eggs": eggs,
                "larvae": larvae,
                "pupae": pupae,
                "adult_females": adults,
                "total": eggs + larvae + pupae + adults,
            }
        )
        # Density-dependent larval survival
        dens_surv = larva_survival * (1.0 / (1.0 + larvae / max(k_larvae, 1.0)))

        new_eggs = adults * eggs_per_female_per_day
        egg_to_larva = eggs * p_egg * egg_survival
        larva_to_pupa = larvae * p_larva * dens_surv
        pupa_to_adult = pupae * p_pupa * pupa_survival

        eggs = max(0.0, eggs + new_eggs - eggs * p_egg)
        larvae = max(0.0, larvae + egg_to_larva - larvae * p_larva)
        pupae = max(0.0, pupae + larva_to_pupa - pupae * p_pupa)
        adults = max(0.0, adults * adult_survival_per_day + pupa_to_adult * 0.5)  # ~50% female

    return pd.DataFrame(rows)


def nutrient_microbe_fly(
    hours: int,
    fruit_sugar_mg: float,
    initial_yeast: float = 1.0,
    fly_visits_per_day: float = 4.0,
    n_larvae: int = 40,
    yeast_growth_per_h: float = 0.15,
    yeast_sugar_halfsat: float = 80.0,
    yeast_use_per_biomass: float = 0.45,
    larva_use_each: float = 0.28,
    fragmentation_boost: float = 1.4,
    fly_seed_per_visit: float = 0.35,
) -> pd.DataFrame:
    """Coupled sugar–yeast–larva toy model.

    - Yeast grow logistically-ish on sugar (Monod-like).
    - Adult visits inoculate yeast.
    - Larvae consume sugar and boost effective yeast access via fragmentation.
    """
    sugar = float(fruit_sugar_mg)
    yeast = float(initial_yeast)
    rows = []
    visits_per_hour = fly_visits_per_day / 24.0

    for h in range(hours + 1):
        rows.append(
            {
                "hour": h,
                "sugar_mg": max(sugar, 0.0),
                "yeast_index": max(yeast, 0.0),
                "fraction_sugar": max(sugar, 0.0) / fruit_sugar_mg if fruit_sugar_mg else 0.0,
            }
        )
        if sugar <= 0:
            sugar = 0.0
            yeast *= 0.98
            continue

        monod = sugar / (yeast_sugar_halfsat + sugar)
        growth = yeast_growth_per_h * monod * fragmentation_boost
        yeast = yeast + yeast * growth + visits_per_hour * fly_seed_per_visit
        yeast = min(yeast, 500.0)

        yeast_consume = yeast * yeast_use_per_biomass * monod
        larva_consume = n_larvae * larva_use_each * (0.6 + 0.4 * monod)
        sugar = max(0.0, sugar - yeast_consume - larva_consume)

    return pd.DataFrame(rows)


def nutrient_depletion(
    hours: int,
    fruit_sugar_mg: float,
    fly_larvae: int,
    yeast_boost: float,
    base_microbial_rate: float = 0.8,
) -> pd.DataFrame:
    """Legacy simple depletion (kept for compatibility)."""
    sugar = float(fruit_sugar_mg)
    rows = []
    for h in range(hours + 1):
        rows.append(
            {
                "hour": h,
                "sugar_remaining_mg": max(sugar, 0.0),
                "fraction_remaining": max(sugar, 0.0) / fruit_sugar_mg if fruit_sugar_mg else 0.0,
            }
        )
        microbial = base_microbial_rate * yeast_boost
        larval = fly_larvae * 0.35
        sugar = max(0.0, sugar - microbial - larval)
    return pd.DataFrame(rows)


def kleiber_curve(
    masses_g: np.ndarray | None = None,
    a: float = 3.4,
    b: float = 0.75,
) -> pd.DataFrame:
    """Mammal-oriented allometry BMR (W) ≈ a * M_kg^b.

    Coefficient ~3.4 W·kg^-0.75 is in the ballpark of classic Kleiber calibrations
    for placental mammals; insects will deviate—overlay species points separately.
    """
    if masses_g is None:
        masses_g = np.logspace(-4, 5, 100)
    m_kg = masses_g / 1000.0
    bmr_w = a * np.power(m_kg, b)
    mass_specific = bmr_w / m_kg
    return pd.DataFrame(
        {
            "mass_g": masses_g,
            "whole_animal_bmr_w": bmr_w,
            "mass_specific_w_per_kg": mass_specific,
        }
    )


def doubling_time_days(r: float) -> float:
    if r <= 0:
        return float("inf")
    return float(np.log(2) / r)


def half_life_hours(df: pd.DataFrame, value_col: str = "fraction_sugar") -> float | None:
    hit = df.loc[df[value_col] <= 0.5]
    if hit.empty:
        return None
    return float(hit.iloc[0]["hour"])


def generations_in_window(window_days: float, generation_days: float) -> float:
    """How many generation intervals fit in a calendar window."""
    if generation_days <= 0:
        return float("inf")
    return float(window_days) / float(generation_days)


def compare_logistic_race(
    species_params: list[dict],
    days: int,
    k: float,
) -> pd.DataFrame:
    """Multi-species logistic trajectories for plotting.

    Each item: {"id", "name", "r", "n0"}.
    """
    frames = []
    for sp in species_params:
        series = logistic_population(days, r=float(sp["r"]), k=float(k), n0=float(sp["n0"]))
        series = series.assign(species=sp["name"], species_id=sp["id"])
        frames.append(series)
    if not frames:
        return pd.DataFrame(columns=["day", "population", "species", "species_id"])
    return pd.concat(frames, ignore_index=True)


def scenario_presets() -> dict[str, dict]:
    """Named simulator starting points for teaching demos."""
    return {
        "Kitchen fruit bowl": {
            "sugar_mg": 1200,
            "hours": 72,
            "larvae": 60,
            "visits": 8.0,
            "yeast0": 1.2,
        },
        "Heavy infestation": {
            "sugar_mg": 1800,
            "hours": 96,
            "larvae": 180,
            "visits": 16.0,
            "yeast0": 3.0,
        },
        "Microbes alone": {
            "sugar_mg": 1200,
            "hours": 72,
            "larvae": 0,
            "visits": 0.0,
            "yeast0": 1.2,
        },
        "Sparse pioneer visits": {
            "sugar_mg": 800,
            "hours": 48,
            "larvae": 15,
            "visits": 2.0,
            "yeast0": 0.4,
        },
    }
