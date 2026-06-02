# Redundancy and Diversity in System Design

Companion repository folder for the article **“Redundancy and Diversity in System Design.”**

This directory provides reproducible workflows for modeling functional redundancy, diversity, response diversity, common-mode failure exposure, coordination capacity, justice contribution, strategic redundancy placement, and uncertainty-aware resilience design.

## Correct article directory

```text
articles/redundancy-and-diversity-in-system-design/
```

## Purpose

This scaffold supports a professional redundancy-and-diversity resilience workflow:

1. Define critical functions that must continue under disturbance.
2. Score strategies for functional redundancy, diversity, response diversity, coordination capacity, justice contribution, and common-mode failure risk.
3. Compare design strategies under balanced, redundancy-first, diversity-first, response-diversity-first, coordination-first, justice-first, and common-mode-sensitive priorities.
4. Model uncertainty with Monte Carlo simulation.
5. Diagnose common-mode failure and false redundancy.
6. Identify when backup capacity is meaningful, maintained, accessible, and differentiated.
7. Provide multi-language examples in Python, R, Julia, SQL, Rust, Go, C, C++, and Fortran.
8. Export reproducible tables, figures, documentation, and notebook placeholders.

## Responsible-use note

The data are synthetic and the models are methodological examples. They are intended for learning, reproducible article companions, dashboard prototyping, and professional modeling design. Real redundancy and diversity assessment requires empirical system data, local knowledge, engineering review, ecological expertise, governance context, community participation, uncertainty analysis, and public accountability.

Do not use these examples to claim that a system is safe, rank communities, reduce protection for vulnerable groups, or replace stress testing and field validation with model output.

## Quick start

Run the dependency-light Python workflow:

```bash
python3 python/redundancy_diversity_standard.py
```

Optional advanced Python workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/redundancy_diversity_advanced.py
```

Run smoke checks:

```bash
bash smoke-test.sh
```

## Directory structure

```text
articles/redundancy-and-diversity-in-system-design/
├── python/       # Strategy scoring, uncertainty, common-mode diagnostics
├── r/            # Scenario-weighted comparison and plotting
├── julia/        # Response-diversity and common-mode examples
├── sql/          # Strategies, criteria, scenarios, model-run schemas
├── rust/         # CLI resilience-value diagnostic scaffold
├── go/           # Strategy diagnostic utility
├── cpp/          # Fast strategy scoring example
├── fortran/      # Dynamic function-under-disturbance example
├── c/            # Low-level resilience-value utility
├── docs/         # Modeling principles, validation, responsible use
├── data/         # Synthetic datasets
├── outputs/      # Generated tables, figures, and models
└── notebooks/    # Notebook placeholders
```
