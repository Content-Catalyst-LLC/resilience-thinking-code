# Resilience Indicators and Dashboard Risk

Companion repository folder for the article **“Resilience Indicators and Dashboard Risk.”**

This directory provides reproducible workflows for comparing resilience dashboard designs, scoring indicator systems, detecting dashboard risk, applying threshold and uncertainty penalties, evaluating justice visibility, and simulating how dashboard interpretations change under missing data and uncertainty.

## Correct article directory

```text
articles/resilience-indicators-and-dashboard-risk/
```

## Purpose

This scaffold supports a professional resilience-dashboard analysis workflow:

1. Define indicator coverage, threshold sensitivity, justice visibility, uncertainty transparency, decision-trigger clarity, learning integration, and dashboard-risk exposure.
2. Compare dashboard designs under balanced, threshold-first, justice-first, uncertainty-first, decision-trigger-first, and dashboard-risk-aware priorities.
3. Score systems using naive, threshold-adjusted, and uncertainty-adjusted dashboard scores.
4. Detect red-flag conditions that should not be averaged away.
5. Simulate uncertainty, missingness, threshold risk, and justice visibility using Monte Carlo analysis.
6. Diagnose false precision, hidden inequality, metric fixation, lagging visibility, and dashboard complacency.
7. Support responsible interpretation across infrastructure, ecosystems, public health, climate adaptation, communities, institutions, and social-ecological systems.
8. Provide multi-language examples in Python, R, Julia, SQL, Rust, Go, C, C++, and Fortran.
9. Export reproducible tables, figures, documentation, and notebook placeholders.

## Responsible-use note

The data are synthetic and the models are methodological examples. They are intended for learning, reproducible article companions, dashboard prototyping, and professional modeling design. Real resilience dashboards require empirical data, domain expertise, data-quality review, uncertainty labeling, public participation, community knowledge, and accountable decision triggers.

Do not use these examples to claim exact resilience, rank communities without context, hide uncertainty, replace public judgment with a composite score, or treat a dashboard as proof that a system is safe.

## Quick start

Run the dependency-light Python workflow:

```bash
python3 python/resilience_dashboard_standard.py
```

Optional advanced Python workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/resilience_dashboard_advanced.py
```

Run smoke checks:

```bash
bash smoke-test.sh
```

## Directory structure

```text
articles/resilience-indicators-and-dashboard-risk/
├── python/       # Dashboard scoring, uncertainty, red flags, diagnostics
├── r/            # Scenario-weighted dashboard design comparison
├── julia/        # Indicator score and dashboard-risk examples
├── sql/          # Indicators, systems, scores, thresholds, missingness
├── rust/         # CLI dashboard-value diagnostic scaffold
├── go/           # Dashboard diagnostic utility
├── cpp/          # Fast dashboard-value scoring example
├── fortran/      # Dynamic dashboard score response example
├── c/            # Low-level dashboard-value utility
├── docs/         # Modeling principles, validation, responsible use
├── data/         # Synthetic datasets
├── outputs/      # Generated tables, figures, and models
└── notebooks/    # Notebook placeholders
```
