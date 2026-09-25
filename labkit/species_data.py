"""Comparative life-history and metabolic reference data.

Central values are literature-anchored teaching estimates with explicit ranges
and source notes. Prefer ranges over single points when discussing uncertainty.
Not for clinical, veterinary, or protocol-critical use.
"""

from __future__ import annotations

from typing import Any

import pandas as pd

# ---------------------------------------------------------------------------
# Species profiles
# mass-specific BMR: watts per kg (approximate resting / standard rates)
# generation_days: typical minimum generation interval under favorable lab/field
# ---------------------------------------------------------------------------

SPECIES: dict[str, dict[str, Any]] = {
    "fruit_fly": {
        "common_name": "Fruit fly",
        "scientific_name": "Drosophila melanogaster",
        "clade": "Insect",
        "adult_mass_g": 0.0010,
        "adult_mass_range_g": (0.0007, 0.0014),
        "body_temp_c": None,
        "thermotype": "ectotherm",
        "generation_days": 10.0,
        "generation_range_days": (8.0, 14.0),
        "sexual_maturity_days": 1.5,
        "eggs_or_offspring_per_bout": 40,
        "bouts_per_lifetime": 10,
        "lifetime_fecundity": 400,
        "lifetime_fecundity_range": (200, 900),
        "eggs_per_day_peak": 50,
        "lifespan_days": 45,
        "lifespan_range_days": (30, 70),
        "mass_specific_bmr_w_per_kg": 28.0,
        "gut_passage_hours": 0.75,
        "gut_passage_range_h": (0.25, 2.0),
        "digestive_strategy": (
            "Larvae: continuous feeding with extra-oral digestion and a short, high-throughput gut; "
            "adults mainly sip liquids. Yeasts and bacteria on fruit pre-process sugars and supply sterols/vitamins."
        ),
        "nutrient_role": (
            "Vector and amplify yeasts; fragment pulp; convert sugar/amino acids into larval biomass "
            "before an ephemeral patch collapses."
        ),
        "r_or_k": "Strongly r-selected",
        "intrinsic_r_per_day": 0.32,
        "notes": (
            "At 25°C, egg→adult is commonly ~9–11 days (egg ~1 d, larva ~4 d, pupa ~4–5 d). "
            "Development slows sharply below ~18°C and accelerates toward ~28°C before heat stress."
        ),
        "citations": [
            "Ashburner et al., Drosophila: A Laboratory Handbook",
            "Bloomington Drosophila Stock Center husbandry notes",
            "Markow & O'Grady reviews of Drosophila life history",
        ],
    },
    "house_mouse": {
        "common_name": "House mouse",
        "scientific_name": "Mus musculus",
        "clade": "Mammal",
        "adult_mass_g": 22.0,
        "adult_mass_range_g": (18.0, 30.0),
        "body_temp_c": 37.0,
        "thermotype": "endotherm",
        "generation_days": 70.0,
        "generation_range_days": (60.0, 90.0),
        "sexual_maturity_days": 42,
        "eggs_or_offspring_per_bout": 6,
        "bouts_per_lifetime": 8,
        "lifetime_fecundity": 50,
        "lifetime_fecundity_range": (30, 80),
        "eggs_per_day_peak": None,
        "lifespan_days": 730,
        "lifespan_range_days": (500, 1000),
        "mass_specific_bmr_w_per_kg": 8.0,
        "gut_passage_hours": 6.0,
        "gut_passage_range_h": (4.0, 10.0),
        "digestive_strategy": (
            "Omnivore with enzymatic small-intestine digestion plus cecal microbial fermentation of fiber."
        ),
        "nutrient_role": (
            "High mass-specific metabolism for a vertebrate; opportunistic scavenging turns human food waste "
            "into mouse biomass on a weeks-to-months clock."
        ),
        "r_or_k": "r-leaning for a mammal",
        "intrinsic_r_per_day": 0.04,
        "notes": (
            "Gestation ≈ 19–21 days; weaning ≈ 3 weeks; postpartum estrus allows rapid successive litters in labs."
        ),
        "citations": [
            "Mouse reproductive biology handbooks (JAX / laboratory animal science)",
            "Kleiber-style mammalian BMR compilations",
        ],
    },
    "brown_rat": {
        "common_name": "Brown rat",
        "scientific_name": "Rattus norvegicus",
        "clade": "Mammal",
        "adult_mass_g": 320.0,
        "adult_mass_range_g": (250.0, 500.0),
        "body_temp_c": 37.5,
        "thermotype": "endotherm",
        "generation_days": 90.0,
        "generation_range_days": (75.0, 120.0),
        "sexual_maturity_days": 65,
        "eggs_or_offspring_per_bout": 9,
        "bouts_per_lifetime": 7,
        "lifetime_fecundity": 60,
        "lifetime_fecundity_range": (40, 100),
        "eggs_per_day_peak": None,
        "lifespan_days": 900,
        "lifespan_range_days": (700, 1100),
        "mass_specific_bmr_w_per_kg": 5.2,
        "gut_passage_hours": 12.0,
        "gut_passage_range_h": (8.0, 18.0),
        "digestive_strategy": (
            "Omnivore with larger absolute gut capacity than mice; cecal fermentation contributes to fiber use."
        ),
        "nutrient_role": (
            "Colony foraging redistributes refuse nutrients across sites; slower mass-specific rates than mice "
            "but larger per-animal throughput."
        ),
        "r_or_k": "Moderately r-selected mammal",
        "intrinsic_r_per_day": 0.03,
        "notes": "Gestation ≈ 21–23 days; litters often larger than mice; sexual maturity ~8–12 weeks.",
        "citations": [
            "Laboratory rat biology references",
            "Comparative mammalian metabolic rate tables",
        ],
    },
    "nematode": {
        "common_name": "Nematode worm",
        "scientific_name": "Caenorhabditis elegans",
        "clade": "Nematode",
        "adult_mass_g": 4e-6,
        "adult_mass_range_g": (2e-6, 6e-6),
        "body_temp_c": None,
        "thermotype": "ectotherm",
        "generation_days": 3.5,
        "generation_range_days": (2.5, 5.5),
        "sexual_maturity_days": 2.5,
        "eggs_or_offspring_per_bout": 300,
        "bouts_per_lifetime": 1,
        "lifetime_fecundity": 300,
        "lifetime_fecundity_range": (200, 350),
        "eggs_per_day_peak": None,
        "lifespan_days": 18,
        "lifespan_range_days": (12, 25),
        "mass_specific_bmr_w_per_kg": 35.0,
        "gut_passage_hours": 0.05,
        "gut_passage_range_h": (0.02, 0.15),
        "digestive_strategy": (
            "Bacterial feeder: pharyngeal grinding pulverizes microbes; short intestine assimilates quickly."
        ),
        "nutrient_role": "Turns bacterial films into nematode biomass in moist microhabitats within days.",
        "r_or_k": "Extremely r-selected",
        "intrinsic_r_per_day": 0.55,
        "notes": (
            "Hermaphrodites self-fertilize (~300 progeny typical). Generation ≈ 3 days at 20°C; faster at 25°C."
        ),
        "citations": [
            "C. elegans WormBook developmental timing chapters",
            "Classic Brenner / Sulston lab husbandry norms",
        ],
    },
    "baker_yeast": {
        "common_name": "Baker's yeast",
        "scientific_name": "Saccharomyces cerevisiae",
        "clade": "Fungus",
        "adult_mass_g": 4e-11,
        "adult_mass_range_g": (2e-11, 8e-11),
        "body_temp_c": None,
        "thermotype": "ectotherm",
        "generation_days": 0.0625,  # 90 minutes
        "generation_range_days": (0.042, 0.125),
        "sexual_maturity_days": 0.0625,
        "eggs_or_offspring_per_bout": 1,
        "bouts_per_lifetime": 20,
        "lifetime_fecundity": 20,
        "lifetime_fecundity_range": (10, 30),
        "eggs_per_day_peak": None,
        "lifespan_days": 2.0,
        "lifespan_range_days": (1.0, 4.0),
        "mass_specific_bmr_w_per_kg": 180.0,
        "gut_passage_hours": 0.0,
        "gut_passage_range_h": (0.0, 0.0),
        "digestive_strategy": (
            "Extracellular hydrolases (e.g. invertase) plus membrane transporters; fermentation of hexoses "
            "to ethanol + CO₂ when oxygen or respiration capacity is limiting."
        ),
        "nutrient_role": (
            "Primary sugar processor on fruit; produces volatiles that attract Drosophila; "
            "synthesizes sterols and other micronutrients flies require."
        ),
        "r_or_k": "Maximal r-strategy (microbial)",
        "intrinsic_r_per_day": 11.0,  # ln(2)/(90/1440) ≈ 11.1 /day
        "notes": (
            "Doubling ≈ 90 min in rich aerobic medium at ~30°C; slower in ethanol-stressed or anaerobic fruit pulp."
        ),
        "citations": [
            "Yeast genetics / metabolism textbooks (e.g. Sherman primers)",
            "Drosophila–yeast mutualism literature (e.g. Christiaens, Becher, and related reviews)",
        ],
    },
    "rabbit": {
        "common_name": "European rabbit",
        "scientific_name": "Oryctolagus cuniculus",
        "clade": "Mammal",
        "adult_mass_g": 1800.0,
        "adult_mass_range_g": (1400.0, 2500.0),
        "body_temp_c": 39.0,
        "thermotype": "endotherm",
        "generation_days": 120.0,
        "generation_range_days": (100.0, 150.0),
        "sexual_maturity_days": 120,
        "eggs_or_offspring_per_bout": 5,
        "bouts_per_lifetime": 6,
        "lifetime_fecundity": 30,
        "lifetime_fecundity_range": (20, 45),
        "eggs_per_day_peak": None,
        "lifespan_days": 2555,
        "lifespan_range_days": (1800, 3600),
        "mass_specific_bmr_w_per_kg": 3.0,
        "gut_passage_hours": 18.0,
        "gut_passage_range_h": (12.0, 30.0),
        "digestive_strategy": (
            "Hindgut fermenter; cecotrophy recycles microbial protein and vitamins from soft feces."
        ),
        "nutrient_role": "Converts plant fiber into mammal biomass via microbial fermentation loops.",
        "r_or_k": "r-selected for a mid-size herbivore",
        "intrinsic_r_per_day": 0.02,
        "notes": "Gestation ≈ 30–32 days; classic boom–bust herbivore demography in the wild.",
        "citations": [
            "Lagomorph reproductive ecology reviews",
            "Hindgut fermentation / cecotrophy physiology texts",
        ],
    },
    "human": {
        "common_name": "Human",
        "scientific_name": "Homo sapiens",
        "clade": "Mammal",
        "adult_mass_g": 70000.0,
        "adult_mass_range_g": (50000.0, 90000.0),
        "body_temp_c": 37.0,
        "thermotype": "endotherm",
        "generation_days": 10000.0,  # ~27 years demographic generation
        "generation_range_days": (8000.0, 12000.0),
        "sexual_maturity_days": 4750,
        "eggs_or_offspring_per_bout": 1,
        "bouts_per_lifetime": 2,
        "lifetime_fecundity": 2,
        "lifetime_fecundity_range": (0, 8),
        "eggs_per_day_peak": None,
        "lifespan_days": 28000,
        "lifespan_range_days": (25000, 31000),
        "mass_specific_bmr_w_per_kg": 1.15,
        "gut_passage_hours": 40.0,
        "gut_passage_range_h": (24.0, 72.0),
        "digestive_strategy": (
            "Omnivore; long small intestine; modest colonic fermentation. Cooking and fermentation are "
            "external digestive technologies."
        ),
        "nutrient_role": "Culture dominates nutrient breakdown rate more than gut transit speed.",
        "r_or_k": "Strongly K-selected",
        "intrinsic_r_per_day": 0.0002,
        "notes": "Slow-life contrast: decades per generation versus days for flies.",
        "citations": [
            "Human BMR / Mifflin-adjacent order-of-magnitude (~70 W for 70 kg)",
            "Demographic generation length literature",
        ],
    },
    "e_coli": {
        "common_name": "E. coli",
        "scientific_name": "Escherichia coli",
        "clade": "Bacterium",
        "adult_mass_g": 1e-12,
        "adult_mass_range_g": (5e-13, 2e-12),
        "body_temp_c": None,
        "thermotype": "ectotherm",
        "generation_days": 0.014,  # ~20 min doubling in rich medium
        "generation_range_days": (0.010, 0.042),
        "sexual_maturity_days": 0.014,
        "eggs_or_offspring_per_bout": 1,
        "bouts_per_lifetime": 1,
        "lifetime_fecundity": 1,
        "lifetime_fecundity_range": (1, 1),
        "eggs_per_day_peak": None,
        "lifespan_days": 0.042,
        "lifespan_range_days": (0.02, 0.1),
        "mass_specific_bmr_w_per_kg": 900.0,
        "gut_passage_hours": 0.0,
        "gut_passage_range_h": (0.0, 0.0),
        "digestive_strategy": (
            "Membrane transporters + periplasmic enzymes; binary fission converts dissolved organics "
            "into biomass on a minute-scale clock in rich medium."
        ),
        "nutrient_role": (
            "Ultra-fast sugar and amino-acid scavenger in guts and rotting patches; often coexists with "
            "yeasts that dominate high-sugar fruit surfaces."
        ),
        "r_or_k": "Maximal r-strategy (prokaryote)",
        "intrinsic_r_per_day": 50.0,  # ln(2)/(20/1440) ≈ 50 /day
        "notes": (
            "Doubling ≈ 20 min in rich aerobic broth at ~37°C; much slower in cold, oligotrophic, or "
            "acidic fruit pulp. Binary fission ≠ sexual generation—used here as a turnover clock."
        ),
        "citations": [
            "Classic E. coli physiology / Neidhardt-style growth-rate tables",
            "Microbial ecology of fermenting fruit communities",
        ],
    },
    "bluebottle": {
        "common_name": "Bluebottle fly",
        "scientific_name": "Calliphora vicina",
        "clade": "Insect",
        "adult_mass_g": 0.055,
        "adult_mass_range_g": (0.040, 0.080),
        "body_temp_c": None,
        "thermotype": "ectotherm",
        "generation_days": 14.0,
        "generation_range_days": (10.0, 21.0),
        "sexual_maturity_days": 3.0,
        "eggs_or_offspring_per_bout": 180,
        "bouts_per_lifetime": 4,
        "lifetime_fecundity": 700,
        "lifetime_fecundity_range": (400, 1200),
        "eggs_per_day_peak": 100,
        "lifespan_days": 35,
        "lifespan_range_days": (20, 50),
        "mass_specific_bmr_w_per_kg": 22.0,
        "gut_passage_hours": 1.5,
        "gut_passage_range_h": (0.5, 4.0),
        "digestive_strategy": (
            "Carrion/protein specialist: larvae secrete proteases onto soft tissue and re-ingest slurry; "
            "faster absolute biomass gain than fruit-fly larvae on meat patches."
        ),
        "nutrient_role": (
            "Converts protein-rich carcasses into fly biomass within days; forensic indicator of "
            "decomposition stage."
        ),
        "r_or_k": "Strongly r-selected (necrophagous)",
        "intrinsic_r_per_day": 0.28,
        "notes": (
            "Egg→adult often ~10–18 days depending on temperature and tissue. Larger eggs/clutches than "
            "Drosophila; generation slightly slower at matched temps."
        ),
        "citations": [
            "Calliphorid forensic entomology developmental tables",
            "Blowfly reproductive ecology reviews",
        ],
    },
    "honey_bee": {
        "common_name": "Honey bee",
        "scientific_name": "Apis mellifera",
        "clade": "Insect",
        "adult_mass_g": 0.10,
        "adult_mass_range_g": (0.08, 0.12),
        "body_temp_c": None,
        "thermotype": "ectotherm",  # colony thermoregulates; individuals are ectotherms
        "generation_days": 21.0,  # worker brood egg→adult
        "generation_range_days": (19.0, 24.0),
        "sexual_maturity_days": 21,
        "eggs_or_offspring_per_bout": 1,  # per worker; queen lays ~1500/day
        "bouts_per_lifetime": 1,
        "lifetime_fecundity": 1,
        "lifetime_fecundity_range": (0, 1),
        "eggs_per_day_peak": None,
        "lifespan_days": 40,  # summer worker
        "lifespan_range_days": (25, 180),
        "mass_specific_bmr_w_per_kg": 18.0,
        "gut_passage_hours": 8.0,
        "gut_passage_range_h": (4.0, 16.0),
        "digestive_strategy": (
            "Nectar stored and enzymatically inverted to honey; pollen digested with midgut enzymes; "
            "colony-level food processing dominates individual gut speed."
        ),
        "nutrient_role": (
            "Social insect contrast: sterile workers turn floral nectar/pollen into colony stores; "
            "reproduction is queen- and swarm-paced, not solitary boom."
        ),
        "r_or_k": "Colony-level K lean; worker brood still fast",
        "intrinsic_r_per_day": 0.05,  # colony growth proxy, not worker self-reproduction
        "notes": (
            "Worker brood ≈ 21 days (egg 3 / larva 6 / pupa 12). Queen may lay 1,000–2,000 eggs/day in "
            "peak season, but individual workers are sterile—r is colony demography, not solitary fecundity."
        ),
        "citations": [
            "Honey bee developmental timing / Winston The Biology of the Honey Bee",
            "Social insect life-history reviews (colony vs individual selection)",
        ],
    },
    "zebrafish": {
        "common_name": "Zebrafish",
        "scientific_name": "Danio rerio",
        "clade": "Fish",
        "adult_mass_g": 0.5,
        "adult_mass_range_g": (0.3, 0.8),
        "body_temp_c": None,
        "thermotype": "ectotherm",
        "generation_days": 90.0,
        "generation_range_days": (70.0, 120.0),
        "sexual_maturity_days": 90,
        "eggs_or_offspring_per_bout": 200,
        "bouts_per_lifetime": 40,
        "lifetime_fecundity": 8000,
        "lifetime_fecundity_range": (2000, 15000),
        "eggs_per_day_peak": None,
        "lifespan_days": 1260,
        "lifespan_range_days": (900, 1800),
        "mass_specific_bmr_w_per_kg": 6.5,
        "gut_passage_hours": 4.0,
        "gut_passage_range_h": (2.0, 8.0),
        "digestive_strategy": (
            "Omnivorous cyprinid with short gut; continuous or frequent feeding at warm lab temperatures "
            "supports rapid juvenile growth."
        ),
        "nutrient_role": (
            "Fast vertebrate model: external fertilization and large clutch sizes convert plankton/flake "
            "feeds into fish biomass on a months-scale clock."
        ),
        "r_or_k": "r-leaning vertebrate (external eggs)",
        "intrinsic_r_per_day": 0.035,
        "notes": (
            "Sexual maturity ≈ 2.5–4 months at ~28°C. Females can spawn hundreds of eggs every few days. "
            "Generation far slower than flies, but fecundity dwarfs mammals of similar mass."
        ),
        "citations": [
            "Zebrafish husbandry / ZFIN developmental timing notes",
            "Teleost reproductive ecology of Danio",
        ],
    },
    "chicken": {
        "common_name": "Domestic chicken",
        "scientific_name": "Gallus gallus domesticus",
        "clade": "Bird",
        "adult_mass_g": 2000.0,
        "adult_mass_range_g": (1500.0, 3500.0),
        "body_temp_c": 41.0,
        "thermotype": "endotherm",
        "generation_days": 180.0,
        "generation_range_days": (150.0, 220.0),
        "sexual_maturity_days": 150,
        "eggs_or_offspring_per_bout": 1,  # one egg at a time; ~250–300 / year layers
        "bouts_per_lifetime": 250,
        "lifetime_fecundity": 250,
        "lifetime_fecundity_range": (80, 320),
        "eggs_per_day_peak": 1,
        "lifespan_days": 2555,
        "lifespan_range_days": (1800, 4000),
        "mass_specific_bmr_w_per_kg": 4.5,
        "gut_passage_hours": 6.0,
        "gut_passage_range_h": (3.0, 12.0),
        "digestive_strategy": (
            "Crop → proventriculus → gizzard grinding; cecal fermentation of fiber; high body temperature "
            "supports rapid processing of grain/insect diets."
        ),
        "nutrient_role": (
            "Avian r-strategist: external eggs and nearly daily laying convert feed into chick biomass "
            "faster than placental mammals of similar mass."
        ),
        "r_or_k": "r-selected avian (domestic layers)",
        "intrinsic_r_per_day": 0.015,
        "notes": (
            "Incubation ≈ 21 days; layers may produce ~250+ eggs/year. Generation to sexual maturity "
            "~5–7 months. Wild junglefowl are less extreme but still clutch-based."
        ),
        "citations": [
            "Poultry science reproductive / incubation standards",
            "Avian metabolic rate compilations",
        ],
    },
    "domestic_cat": {
        "common_name": "Domestic cat",
        "scientific_name": "Felis catus",
        "clade": "Mammal",
        "adult_mass_g": 4000.0,
        "adult_mass_range_g": (3000.0, 5500.0),
        "body_temp_c": 38.5,
        "thermotype": "endotherm",
        "generation_days": 365.0,
        "generation_range_days": (300.0, 450.0),
        "sexual_maturity_days": 240,
        "eggs_or_offspring_per_bout": 4,
        "bouts_per_lifetime": 8,
        "lifetime_fecundity": 30,
        "lifetime_fecundity_range": (12, 50),
        "eggs_per_day_peak": None,
        "lifespan_days": 4745,
        "lifespan_range_days": (3650, 6500),
        "mass_specific_bmr_w_per_kg": 2.4,
        "gut_passage_hours": 16.0,
        "gut_passage_range_h": (10.0, 24.0),
        "digestive_strategy": (
            "Obligate carnivore: short gut optimized for protein/fat; limited carbohydrate digestion "
            "relative to omnivorous rodents."
        ),
        "nutrient_role": (
            "Mid-size mammal contrast: predation redistributes vertebrate biomass; generation still "
            "year-scale versus insect days."
        ),
        "r_or_k": "Intermediate mammal",
        "intrinsic_r_per_day": 0.008,
        "notes": "Gestation ≈ 63–65 days; litters often 3–5; maturity ~6–12 months depending on breed/nutrition.",
        "citations": [
            "Feline reproductive biology / veterinary theriogenology texts",
            "Mammalian BMR compilations for Felis",
        ],
    },
    "african_elephant": {
        "common_name": "African elephant",
        "scientific_name": "Loxodonta africana",
        "clade": "Mammal",
        "adult_mass_g": 4_000_000.0,
        "adult_mass_range_g": (2_500_000.0, 6_000_000.0),
        "body_temp_c": 36.5,
        "thermotype": "endotherm",
        "generation_days": 6500.0,  # ~18 years demographic
        "generation_range_days": (5500.0, 8000.0),
        "sexual_maturity_days": 4000,
        "eggs_or_offspring_per_bout": 1,
        "bouts_per_lifetime": 6,
        "lifetime_fecundity": 6,
        "lifetime_fecundity_range": (3, 10),
        "eggs_per_day_peak": None,
        "lifespan_days": 23000,
        "lifespan_range_days": (18000, 28000),
        "mass_specific_bmr_w_per_kg": 0.55,
        "gut_passage_hours": 50.0,
        "gut_passage_range_h": (30.0, 72.0),
        "digestive_strategy": (
            "Hindgut fermenter with enormous absolute throughput; microbial cellulose digestion in "
            "enlarged colon/cecum; low digestive efficiency, high intake."
        ),
        "nutrient_role": (
            "Extreme K: landscape-scale herbivory moves tons of plant matter slowly into a few "
            "long-lived calves."
        ),
        "r_or_k": "Extreme K-selected",
        "intrinsic_r_per_day": 0.00015,
        "notes": (
            "Gestation ≈ 22 months; interbirth interval often 4–5 years; sexual maturity ~10–15 years. "
            "Mass-specific metabolism among the lowest of terrestrial mammals."
        ),
        "citations": [
            "Elephant reproductive ecology / Moss and related demography",
            "Megaherbivore digestive physiology reviews",
        ],
    },
}


FLY_NUTRIENT_PATHWAYS: list[dict[str, str]] = [
    {
        "stage": "1 · Attraction",
        "title": "Adults lock onto fermentation volatiles",
        "detail": (
            "Yeast metabolism releases esters, alcohols, and acids. Drosophila olfactory circuits are "
            "tuned to these cues, so flies preferentially land on already-active microbial patches."
        ),
    },
    {
        "stage": "2 · Inoculation",
        "title": "Yeasts and bacteria hitchhike onto the fruit",
        "detail": (
            "Cuticle, crop regurgitation, and feces deposit microbes. Fly visitation measurably increases "
            "yeast density compared with undisturbed fruit."
        ),
    },
    {
        "stage": "3 · Fragmentation",
        "title": "Larvae tunnel, mash, and oxygenate pulp",
        "detail": (
            "Mechanical shredding multiplies surface area and remixes oxygen/acid gradients, accelerating "
            "both microbial enzyme access and host digestion."
        ),
    },
    {
        "stage": "4 · Assimilation",
        "title": "Extra-oral enzymes + high gut throughput",
        "detail": (
            "Larvae secrete digestive enzymes onto food and re-ingest slurry. A short gut and near-continuous "
            "feeding convert sugars and amino acids into growth tissue within hours."
        ),
    },
    {
        "stage": "5 · Mutualism",
        "title": "Fly ↔ yeast feedback collapses the patch",
        "detail": (
            "Yeasts unlock sugars and supply essential micronutrients (notably sterols); flies disperse yeasts "
            "to new fruits. Together they outpace either partner alone."
        ),
    },
]


REPRODUCTION_DRIVERS: list[dict[str, str]] = [
    {
        "driver": "Temperature-compressed development",
        "explanation": (
            "As ectotherms, Drosophila development rate rises with temperature within a viable window. "
            "A kitchen or lab near 25°C packs egg, larva, and pupa into ~10 days."
        ),
    },
    {
        "driver": "High early fecundity",
        "explanation": (
            "Well-fed females can lay dozens of eggs per day early in adult life, accumulating hundreds "
            "of offspring if nutrition and temperature hold."
        ),
    },
    {
        "driver": "Ephemeral-resource life history",
        "explanation": (
            "Rotting fruit is a rich but short-lived lottery. Selection favors converting a sugar pulse into "
            "many offspring before desiccation, competitors, or sanitation remove the patch."
        ),
    },
    {
        "driver": "Overlapping immature stages",
        "explanation": (
            "Eggs, larvae, and pupae coexist on the same fruit. Multiple cohorts—and sometimes multiple "
            "generations—exploit one prolonged infestation."
        ),
    },
    {
        "driver": "Outsourced digestion",
        "explanation": (
            "Yeasts and bacteria pre-digest sugars and synthesize nutrients flies cannot make efficiently, "
            "keeping larval growth rates high without evolving a cellulolytic gut."
        ),
    },
    {
        "driver": "Small absolute energy bill",
        "explanation": (
            "A milligram-scale body needs little absolute power. High mass-specific metabolism still fits "
            "inside a sugar-rich patch, whereas a mouse must fund endothermy and pregnancy continuously."
        ),
    },
    {
        "driver": "No long pregnancy lock-in",
        "explanation": (
            "External eggs and metamorphosis free flies from months of gestation. Chickens and zebrafish "
            "also externalize embryos—but still mature on month-to-year clocks, not ~10 days."
        ),
    },
]


QUIZ: list[dict[str, Any]] = [
    {
        "q": "What primarily attracts Drosophila adults to fruit?",
        "choices": [
            "Pure sucrose vapor from intact ripe fruit",
            "Fermentation volatiles from yeast/bacterial metabolism",
            "Infrared heat of warm pulp",
            "Magnetic cues from soil minerals",
        ],
        "answer": 1,
        "why": "Flies are drawn to esters, alcohols, and acids produced as microbes ferment sugars.",
        "topic": "Attraction",
    },
    {
        "q": "Why do fruit flies accelerate nutrient breakdown beyond microbes alone?",
        "choices": [
            "They invent novel cellulose enzymes unique to insects",
            "They seed microbes, fragment pulp, and assimilate sugars rapidly as larvae",
            "Adults chew wood fibers into dust",
            "They raise fruit temperature above pasteurization",
        ],
        "answer": 1,
        "why": "Acceleration is ecological + physiological: inoculation, fragmentation, and high larval throughput.",
        "topic": "Nutrient engine",
    },
    {
        "q": "Rough egg→adult time for D. melanogaster at 25°C?",
        "choices": ["~2 days", "~10 days", "~70 days", "~1 year"],
        "answer": 1,
        "why": "About 9–11 days is typical at 25°C under standard lab conditions.",
        "topic": "Development",
    },
    {
        "q": "Compared with house mice, fruit flies mainly win on…",
        "choices": [
            "Absolute body size",
            "Generation rate and eggs per unit time",
            "Maintaining 37°C body temperature",
            "Digesting cellulose like a cow",
        ],
        "answer": 1,
        "why": "Mice are larger endotherms with month-scale generations; flies compound on a ~10-day clock.",
        "topic": "Comparison",
    },
    {
        "q": "Which partner is often the first chemical processor of fruit sugars?",
        "choices": ["Rabbits", "Humans", "Saccharomyces yeasts", "Adult mouse gut only"],
        "answer": 2,
        "why": "Yeasts hydrolyze and ferment sugars; flies amplify and disperse them.",
        "topic": "Mutualism",
    },
    {
        "q": "Cooling a Drosophila culture from 25°C toward 18°C typically…",
        "choices": [
            "Shortens egg→adult time",
            "Lengthens development (ectotherm clock slows)",
            "Converts flies into endotherms",
            "Stops yeast fermentation permanently",
        ],
        "answer": 1,
        "why": "Ectotherm development rate rises with temperature inside a viable window; cool rooms stretch the life cycle.",
        "topic": "Temperature",
    },
    {
        "q": "On a log–log mass vs generation plot, elephants sit far from fruit flies mainly because…",
        "choices": [
            "Elephants have higher mass-specific BMR than flies",
            "Large K-selected mammals have long generation times",
            "Elephants lack guts",
            "Flies maintain 37°C body temperature",
        ],
        "answer": 1,
        "why": "Body size and slow life history (long gestation, delayed maturity) push elephants to the slow pole.",
        "topic": "Allometry",
    },
    {
        "q": "E. coli in rich broth can double in ~20 minutes. Why isn’t that the whole fruit-patch story?",
        "choices": [
            "Bacteria never grow on fruit",
            "Acid, sugar stress, and yeast communities often dominate the volatiles flies track",
            "Flies eat only cellulose",
            "E. coli has a 10-day generation on every substrate",
        ],
        "answer": 1,
        "why": "Lab rich-medium speed is an upper bound; real fruit chemistry and yeast–fly mutualisms reshape who processes sugars.",
        "topic": "Microbes",
    },
]


CITATIONS_LONG: list[dict[str, str]] = [
    {
        "topic": "Drosophila husbandry & timing",
        "ref": "Ashburner, M., Golic, K. & Hawley, R.S. Drosophila: A Laboratory Handbook. Cold Spring Harbor Laboratory Press.",
    },
    {
        "topic": "Life history / ecology",
        "ref": "Markow, T.A. & O'Grady, P. reviews on Drosophila reproductive ecology and natural history.",
    },
    {
        "topic": "Yeast–fly mutualism & volatiles",
        "ref": "Becher et al. and related work on yeast volatiles attracting Drosophila; Christiaens et al. on yeast–fly interactions.",
    },
    {
        "topic": "C. elegans timing",
        "ref": "WormBook chapters on developmental timing and brood size under standard temperatures.",
    },
    {
        "topic": "Metabolic allometry",
        "ref": "Kleiber, M. The Fire of Life; modern compilations of mammalian basal metabolic rates.",
    },
    {
        "topic": "Rodent reproduction",
        "ref": "Laboratory animal science references for Mus musculus and Rattus norvegicus gestation, litter size, and maturity.",
    },
    {
        "topic": "Bacterial growth rates",
        "ref": "E. coli physiology tables (Neidhardt-style): ~20 min doubling in rich medium at 37°C.",
    },
    {
        "topic": "Blowfly / calliphorid timing",
        "ref": "Forensic entomology developmental tables for Calliphora and related genera.",
    },
    {
        "topic": "Honey bee brood & colony demography",
        "ref": "Winston, The Biology of the Honey Bee; social-insect life-history reviews.",
    },
    {
        "topic": "Zebrafish & poultry models",
        "ref": "ZFIN / zebrafish husbandry notes; poultry incubation and layer fecundity standards.",
    },
    {
        "topic": "Cat & elephant demography",
        "ref": "Feline theriogenology texts; African elephant demography (e.g. Moss and related reviews).",
    },
]


def species_dataframe() -> pd.DataFrame:
    rows = []
    for key, s in SPECIES.items():
        rows.append(
            {
                "id": key,
                "Common name": s["common_name"],
                "Scientific name": s["scientific_name"],
                "Clade": s["clade"],
                "Thermotype": s["thermotype"],
                "Adult mass (g)": s["adult_mass_g"],
                "Mass low (g)": s["adult_mass_range_g"][0],
                "Mass high (g)": s["adult_mass_range_g"][1],
                "Generation time (days)": s["generation_days"],
                "Gen. low (days)": s["generation_range_days"][0],
                "Gen. high (days)": s["generation_range_days"][1],
                "Sexual maturity (days)": s["sexual_maturity_days"],
                "Offspring / bout": s["eggs_or_offspring_per_bout"],
                "Lifetime fecundity": s["lifetime_fecundity"],
                "Fecundity low": s["lifetime_fecundity_range"][0],
                "Fecundity high": s["lifetime_fecundity_range"][1],
                "Lifespan (days)": s["lifespan_days"],
                "Mass-specific BMR (W/kg)": s["mass_specific_bmr_w_per_kg"],
                "Gut passage (h)": s["gut_passage_hours"],
                "r (1/day)": s["intrinsic_r_per_day"],
                "Strategy": s["r_or_k"],
            }
        )
    return pd.DataFrame(rows)


def get_species(species_id: str) -> dict[str, Any]:
    return SPECIES[species_id]


def whole_animal_bmr_w(species_id: str) -> float:
    s = SPECIES[species_id]
    return s["mass_specific_bmr_w_per_kg"] * (s["adult_mass_g"] / 1000.0)
