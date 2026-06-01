# What Is Resilience Thinking?

Companion repository folder for the article **“What Is Resilience Thinking?”**

This directory provides reproducible, synthetic-data workflows for exploring disturbance, adaptation, threshold risk, system viability, redundancy, modularity, learning, and resilience diagnostics.

## Directory structure

```text
articles/what-is-resilience/
├── python/       # Standard-library and optional pandas/numpy/matplotlib workflows
├── r/            # Resilience profiles, vulnerability flags, and scenario summaries
├── julia/        # Nonlinear threshold and regime-shift examples
├── sql/          # Resilience schema, indicators, disturbances, scenarios, model runs
├── rust/         # CLI resilience diagnostics scaffold
├── go/           # Network dependency and resilience utility scaffold
├── cpp/          # Efficient repeated-disturbance simulation
├── fortran/      # Dynamic viability and disturbance-load example
├── c/            # Low-level viability simulation utility
├── docs/         # Article notes and modeling principles
├── data/         # Synthetic datasets
├── outputs/      # Generated outputs
└── notebooks/    # Notebook placeholders
```

## Purpose

The code is designed for professional learning, reproducible methods demonstration, and adaptation into resilience analysis workflows. It is not a predictive model and does not replace domain expertise, local knowledge, stakeholder participation, ecological monitoring, engineering review, or institutional analysis.

## Responsible-use note

These examples use synthetic data. They are intended for research, education, methods prototyping, and decision-support design. They should not be used as automatic ranking tools, policy justification machines, or substitutes for participatory resilience assessment. Resilience analysis should always ask: resilience of what, for whom, against what disturbance, and at whose cost?

## Quick start

Run the dependency-light Python workflow:

```bash
python3 python/resilience_diagnostics_standard.py
```

Optional advanced Python workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/resilience_diagnostics_advanced.py
```

Run smoke checks:

```bash
bash smoke-test.sh
```
