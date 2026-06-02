# Landscape Resilience and Disturbance Regimes

Companion repository folder for the article **“Landscape Resilience and Disturbance Regimes.”**

This directory provides reproducible workflows for modeling landscape resilience, disturbance spread, patch dynamics, spatial heterogeneity, refugia, ecological memory, connectivity, fragmentation, governance capacity, social vulnerability, and disturbance-regime risk.

## Correct article directory

```text
articles/landscape-resilience-and-disturbance-regimes/
```

## Purpose

This scaffold supports a professional landscape-resilience workflow:

1. Represent landscapes as spatial mosaics of patches with condition, exposure, buffering capacity, ecological memory, refugia, recovery capacity, and connectivity.
2. Compare landscapes across spatial heterogeneity, viable connectivity, refugia capacity, ecological memory, disturbance pressure, fragmentation, governance capacity, and social vulnerability.
3. Simulate disturbance spread across connected patches.
4. Track patch condition, disturbance pressure, resilience margin, and threshold-risk flags over time.
5. Compare disturbance-regime scenarios, including climate-amplified disturbance and compound spatial risk.
6. Support governance, justice, and responsible-use documentation.
7. Provide multi-language examples in Python, R, Julia, SQL, Rust, Go, C, C++, and Fortran.

## Responsible-use note

The data are synthetic and the models are methodological examples. They are intended for learning, reproducible article companions, dashboard prototyping, and professional modeling design. Real landscape-resilience assessment requires calibrated spatial data, land-cover and disturbance histories, remote sensing, field evidence, hydrological and ecological expertise, social vulnerability analysis, local and Indigenous knowledge where appropriate, uncertainty review, and accountable public review.

Do not use these examples to rank communities, landscapes, hazard priorities, or restoration investments without validated evidence and participatory review.

## Quick start

Run the dependency-light Python workflow:

```bash
python3 python/landscape_resilience_standard.py
```

Optional advanced Python workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/landscape_resilience_advanced.py
```

Run smoke checks:

```bash
bash smoke-test.sh
```

## Directory structure

```text
articles/landscape-resilience-and-disturbance-regimes/
├── python/       # Patch dynamics and disturbance-spread simulation
├── r/            # Landscape-resilience profiles and visualization
├── julia/        # Spatial disturbance-threshold example
├── sql/          # Landscapes, patches, disturbance regimes, scenarios, social vulnerability schemas
├── rust/         # CLI diagnostic scaffold
├── go/           # Landscape-resilience diagnostic utility
├── cpp/          # Fast patch disturbance simulation
├── fortran/      # Dynamic landscape resilience-margin example
├── c/            # Low-level patch resilience-margin utility
├── docs/         # Modeling principles, validation, responsible use
├── data/         # Synthetic datasets
├── outputs/      # Generated tables, figures, and models
└── notebooks/    # Notebook placeholders
```
