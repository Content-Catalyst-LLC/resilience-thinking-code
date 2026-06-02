# Resilience Metrics and Measurement

Companion repository folder for the article **“Resilience Metrics and Measurement.”**

This directory provides reproducible workflows for comparing resilience measurement frameworks, scoring resistance and recovery coverage, evaluating adaptive-capacity visibility, buffer-capacity diagnostics, threshold sensitivity, justice visibility, data-quality transparency, and uncertainty-aware measurement choices.

## Correct article directory

```text
articles/resilience-metrics-and-measurement/
```

## Purpose

This scaffold supports a professional resilience-measurement workflow:

1. Define what system is being measured, to what disturbance, for whom, and over what time horizon.
2. Compare indicator dashboards, performance monitoring, stress-test frameworks, participatory assessment, and hybrid dynamic frameworks.
3. Score frameworks across resistance coverage, recovery insight, adaptive-capacity visibility, buffer visibility, justice visibility, data-quality transparency, and threshold blindness.
4. Use scenario-weighted comparison for balanced, recovery-first, adaptation-first, threshold-sensitive, justice-visible, and structural-balance priorities.
5. Model uncertainty using Monte Carlo simulation.
6. Diagnose when measurement frameworks reveal or obscure resilience.
7. Support responsible interpretation across ecological, infrastructure, institutional, climate, economic, public-health, and social-ecological systems.
8. Provide multi-language examples in Python, R, Julia, SQL, Rust, Go, C, C++, and Fortran.
9. Export reproducible tables, figures, documentation, and notebook placeholders.

## Responsible-use note

The data are synthetic and the models are methodological examples. They are intended for learning, reproducible article companions, dashboard prototyping, and professional modeling design. Real resilience measurement requires empirical data, system history, domain expertise, local knowledge, uncertainty review, community participation, and accountable governance.

Do not use these examples to claim exact resilience, rank communities, justify underinvestment, hide uncertainty, or replace public judgment with a single composite score.

## Quick start

Run the dependency-light Python workflow:

```bash
python3 python/resilience_metrics_standard.py
```

Optional advanced Python workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/resilience_metrics_advanced.py
```

Run smoke checks:

```bash
bash smoke-test.sh
```

## Directory structure

```text
articles/resilience-metrics-and-measurement/
├── python/       # Measurement framework scoring, uncertainty, diagnostics
├── r/            # Scenario-weighted framework comparison and plotting
├── julia/        # Resilience score and threshold-sensitivity examples
├── sql/          # Indicators, systems, events, recovery, thresholds, scenarios
├── rust/         # CLI metric-value diagnostic scaffold
├── go/           # Measurement-framework diagnostic utility
├── cpp/          # Fast framework scoring example
├── fortran/      # Dynamic resilience-function example
├── c/            # Low-level metric-value utility
├── docs/         # Modeling principles, validation, responsible use
├── data/         # Synthetic datasets
├── outputs/      # Generated tables, figures, and models
└── notebooks/    # Notebook placeholders
```
