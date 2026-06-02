# Future Directions in Resilience Thinking

Companion repository folder for the article **Future Directions in Resilience Thinking**.

This scaffold supports reproducible examples for comparing future resilience strategy portfolios under uncertainty. It focuses on adaptive capacity, buffering capacity, transformability, governance quality, equity performance, digital resilience, climate readiness, systemic exposure, implementation burden, and robustness across alternative strategic priorities.

## Directory

```text
articles/future-directions-in-resilience-thinking/
```

## What this scaffold includes

- Synthetic future resilience strategy data.
- Synthetic strategic priority scenarios.
- Dependency-light Python workflow for portfolio scoring and uncertainty analysis.
- Optional advanced Python workflow using pandas, numpy, and matplotlib.
- R workflow for scenario-weighted strategy comparison.
- SQL schema for strategy data and value views.
- Lightweight examples in Julia, C, C++, Go, Rust, and Fortran.
- Responsible-use documentation, validation notes, and WordPress GitHub embed block.

## Responsible-use note

These workflows use synthetic data. They are for methods demonstration, reproducible article companions, planning prototypes, and learning. Real resilience strategy requires domain evidence, affected-community participation, engineering judgment where infrastructure is involved, ecological assessment, social vulnerability analysis, public accountability, and transparent governance.

Do not use these examples as automated policy, emergency, investment, relocation, infrastructure, insurance, or public-service decision systems.

## Quick start

```bash
python3 python/future_resilience_standard.py
bash smoke-test.sh
```

Optional advanced workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/future_resilience_advanced.py
```
