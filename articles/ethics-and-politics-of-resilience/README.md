# Ethics and Politics of Resilience

Companion repository folder for the article **Ethics and Politics of Resilience**.

This scaffold supports reproducible examples for justice-sensitive resilience analysis. It focuses on protective effectiveness, equity, governance legitimacy, recognition, accountability, burden shifting, implementation burden, participation, responsibility assignment, and uncertainty.

## Directory

```text
articles/ethics-and-politics-of-resilience/
```

## What this scaffold includes

- Synthetic ethical resilience strategy data.
- Synthetic ethical priority scenarios.
- Dependency-light Python workflow for ethical strategy scoring and uncertainty analysis.
- Optional advanced Python workflow using pandas, numpy, and matplotlib.
- R workflow for ethical resilience ranking across normative priorities.
- SQL schema for ethical resilience strategy data and value views.
- Lightweight examples in Julia, C, C++, Go, Rust, and Fortran.
- Responsible-use documentation, validation notes, and WordPress GitHub embed block.

## Responsible-use note

These workflows use synthetic data. They are for methods demonstration, reproducible article companions, planning prototypes, and learning. Real ethical resilience analysis requires affected-community participation, local knowledge, transparent assumptions, governance review, historical context, public accountability, legal and rights analysis where relevant, and disaggregated evidence.

Do not use these examples as automated policy, emergency, relocation, infrastructure, insurance, aid-allocation, or public-service decision systems.

## Quick start

```bash
python3 python/ethical_resilience_standard.py
bash smoke-test.sh
```

Optional advanced workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/ethical_resilience_advanced.py
```
