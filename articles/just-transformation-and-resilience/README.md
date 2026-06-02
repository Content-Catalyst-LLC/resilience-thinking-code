# Just Transformation and Resilience

Companion repository folder for the article **Just Transformation and Resilience**.

This scaffold supports reproducible examples for evaluating transformation pathways through resilience, equity, ecological repair, governance legitimacy, livelihood protection, exposure reduction, burden shifting, lock-in risk, implementation burden, justice gaps, and justice-adjusted resilience.

## Directory

```text
articles/just-transformation-and-resilience/
```

## What this scaffold includes

- Synthetic just transformation pathway data.
- Synthetic dynamic transformation pathway data.
- Dependency-light Python workflow for pathway scoring, justice-gap diagnostics, Monte Carlo uncertainty analysis, and dynamic transformation simulation.
- Optional advanced Python workflow using pandas, numpy, and matplotlib.
- R workflow for comparing transformation pathways across justice and resilience priorities.
- SQL schema for pathway data, dynamic pathway data, and value views.
- Lightweight examples in Julia, C, C++, Go, Rust, and Fortran.
- Responsible-use documentation, validation notes, and WordPress GitHub embed block.

## Responsible-use note

These workflows use synthetic data. They are for methods demonstration, reproducible article companions, planning prototypes, and learning. Real just transformation analysis requires affected-community participation, worker and livelihood analysis, social protection design, ecological evidence, public finance review, rights review where relevant, institutional capacity assessment, and accountable governance.

Do not use these examples as automated policy, emergency, relocation, infrastructure, insurance, investment, aid-allocation, employment, or public-service decision systems.

## Quick start

```bash
python3 python/just_transformation_resilience_standard.py
bash smoke-test.sh
```

Optional advanced workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/just_transformation_resilience_advanced.py
```
