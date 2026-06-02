# Urban Resilience and Adaptation

Companion repository folder for the article **“Urban Resilience and Adaptation.”**

This directory provides reproducible workflows for urban resilience strategy comparison, exposure and vulnerability scoring, service-continuity diagnostics, adaptive-capacity review, ecological-buffering assessment, equity-adjusted resilience value, maladaptation-risk review, urban stress simulation, and uncertainty-aware city adaptation planning.

## Correct article directory

```text
articles/urban-resilience-and-adaptation/
```

## Purpose

This scaffold supports a professional urban resilience modeling workflow:

1. Define strategies across exposure reduction, vulnerability reduction, service continuity, adaptive capacity, ecological buffering, equity protection, and maladaptation risk.
2. Compare strategies under balanced, exposure-first, vulnerability-first, service-continuity-first, adaptation-first, ecology-first, equity-first, and maladaptation-sensitive priorities.
3. Simulate neighborhood or urban-system performance under heat, flood, power outage, housing stress, service disruption, and compound events.
4. Estimate equity-adjusted resilience value and unequal service/access risk.
5. Diagnose maladaptation review triggers, service-continuity constraints, ecological-buffering gaps, and equity-protection gaps.
6. Model uncertainty using Monte Carlo simulation.
7. Support responsible interpretation across housing, transport, water, power, public health, green-blue infrastructure, digital systems, community networks, and governance.
8. Provide multi-language examples in Python, R, Julia, SQL, Rust, Go, C, C++, and Fortran.
9. Export reproducible tables, figures, documentation, and notebook placeholders.

## Responsible-use note

The data are synthetic and the models are methodological examples. They are intended for learning, reproducible article companions, dashboard prototyping, and professional modeling design. Real urban resilience analysis requires local hazard data, block-level exposure data, housing records, infrastructure condition data, public-health evidence, climate scenarios, community participation, engineering review, ecological monitoring, anti-displacement review, and accountable governance.

Do not use these examples to rank neighborhoods, justify displacement, certify public safety, replace engineering or public-health judgment, automate resource allocation, or hide unequal exposure and recovery behind a single resilience score.

## Quick start

Run the dependency-light Python workflow:

```bash
python3 python/urban_resilience_standard.py
```

Optional advanced Python workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/urban_resilience_advanced.py
```

Run smoke checks:

```bash
bash smoke-test.sh
```

## Directory structure

```text
articles/urban-resilience-and-adaptation/
├── python/       # Urban scoring, stress simulation, uncertainty
├── r/            # Scenario-weighted strategy comparison
├── julia/        # Resilience pathway examples
├── sql/          # Neighborhoods, systems, hazards, strategies, scenarios
├── rust/         # CLI resilience-value diagnostic scaffold
├── go/           # Strategy diagnostic utility
├── cpp/          # Fast urban resilience scoring example
├── fortran/      # Urban function under stress dynamics
├── c/            # Low-level resilience value utility
├── docs/         # Modeling principles, validation, responsible use
├── data/         # Synthetic datasets
├── outputs/      # Generated tables, figures, and models
└── notebooks/    # Notebook placeholders
```
