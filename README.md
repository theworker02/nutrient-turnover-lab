# Nutrient Turnover Lab

**Version:** 0.1.0

Interactive **Streamlit** study of how fruit flies accelerate nutrient breakdown on fermenting fruit, why populations explode, and how that compares across a **14-species** teaching set—from *E. coli* and yeast through flies, bees, zebrafish, and chickens to rodents, cats, humans, and elephants.

## Run

```bash
cd nutrient-turnover-lab
.\.venv\Scripts\activate
streamlit run app.py
```

Open the URL Streamlit prints (usually http://localhost:8501).

## Sections

| Page | Contents |
|------|----------|
| Home | Thesis, metrics with ranges, mass×generation chart |
| Fruit-fly nutrient engine | 5-stage pathway + coupled sugar–yeast–larva simulator |
| Why they multiply | Temp→development curve, generation stacking, stage boom, fecundity ranges |
| Comparative species | Dual profiles, multi-overlay radar, Kleiber context, essays, CSV export |
| Simulators | Nutrient presets / population race / stages / allometry sandboxes |
| Quiz | Five-question knowledge check |
| Methods & sources | Equations, accuracy notes, reading paths |

## Species set

Fruit fly, bluebottle, honey bee, nematode, baker's yeast, *E. coli*, zebrafish, chicken, house mouse, brown rat, rabbit, domestic cat, human, African elephant.

## Accuracy stance

Parameters are **literature-anchored teaching estimates with explicit ranges**, not single-study point fits. See `labkit/species_data.py` and the Methods page before citing numbers.

## Layout

```
app.py
pages/
labkit/species_data.py
labkit/simulations.py
labkit/ui.py
.streamlit/config.toml
```
