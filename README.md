<p align="center">
  <img src="docs/logo.svg" alt="nutrient-turnover-lab official logo" width="128" height="128">
</p>

<p align="center">
  <a href="https://theworker02.github.io/nutrient-turnover-lab/"><img src="https://img.shields.io/badge/docs-live-0B1F33?style=for-the-badge&labelColor=C9A227" alt="Docs"></a>
  <a href="https://github.com/theworker02/nutrient-turnover-lab/releases/tag/v1.0.0"><img src="https://img.shields.io/badge/release-v1.0.0-success?style=for-the-badge" alt="Release"></a>
  <a href="https://github.com/theworker02/nutrient-turnover-lab/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-see%20LICENSE-blue?style=for-the-badge" alt="License"></a>
  <a href="https://github.com/theworker02/nutrient-turnover-lab"><img src="https://img.shields.io/badge/status-maintained-informational?style=for-the-badge" alt="Status"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-0B1F33.svg" alt="version">
  <img src="https://img.shields.io/badge/category-product-C9A227.svg" alt="category">
  <img src="https://img.shields.io/badge/pages-enabled-222.svg" alt="pages">
  <img src="https://img.shields.io/badge/docs-thickened-brightgreen.svg" alt="docs">
  <img src="https://img.shields.io/badge/notes-detailed-lightgrey.svg" alt="notes">
</p>


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

## Badges & release notes

| Badge | Meaning |
| --- | --- |
| docs live | Public documentation / Pages surface for `nutrient-turnover-lab` |
| release v1.0.0 | Stable tagged release with narrative notes |
| license | See repository `LICENSE` for terms |
| status maintained | Actively kept in the @theworker02 portfolio |
| version 1.0.0 | Documentation and brand completeness milestone |
| pages enabled | Site intended at `https://theworker02.github.io/nutrient-turnover-lab/` |

Detailed narrative for the stable line lives in [CHANGELOG.md](./CHANGELOG.md) and the [v1.0.0 GitHub Release](https://github.com/theworker02/nutrient-turnover-lab/releases/tag/v1.0.0).

## Acquisition

See [ACQUISITION.md](./ACQUISITION.md) for the diligence-oriented product brief, asset map, and commercial posture notes.
