# Maladaptive Resilience

Companion repository folder for the article **Maladaptive Resilience**.

This scaffold supports reproducible examples for distinguishing adaptive resilience from harmful persistence. It focuses on persistence capacity, harm reduction, lock-in reduction, equity, transformation capacity, ecological integrity, burden shifting, implementation burden, maladaptive risk, and adaptive resilience.

## Directory

```text
articles/maladaptive-resilience/
```

## What this scaffold includes

- Synthetic maladaptive resilience strategy data.
- Synthetic harmful-persistence pathway data.
- Dependency-light Python workflow for strategy scoring, maladaptive-risk diagnostics, Monte Carlo uncertainty analysis, and lock-in pathway simulation.
- Optional advanced Python workflow using pandas, numpy, and matplotlib.
- R workflow for comparing adaptive and maladaptive resilience strategies across alternative priorities.
- SQL schema for strategy data, pathway data, and value views.
- Lightweight examples in Julia, C, C++, Go, Rust, and Fortran.
- Responsible-use documentation, validation notes, and WordPress GitHub embed block.

## Responsible-use note

These workflows use synthetic data. They are for methods demonstration, reproducible article companions, planning prototypes, and learning. Real maladaptive-resilience analysis requires affected-community participation, local knowledge, ecological evidence, infrastructure data, institutional review, historical context, social vulnerability analysis, public accountability, and domain expertise.

Do not use these examples as automated policy, emergency, relocation, infrastructure, insurance, investment, aid-allocation, or public-service decision systems.

## Quick start

```bash
python3 python/maladaptive_resilience_standard.py
bash smoke-test.sh
```

Optional advanced workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/maladaptive_resilience_advanced.py
```
