# The History of Resilience Theory

Companion repository folder for the article **“The History of Resilience Theory.”**

This directory provides reproducible analytical workflows for tracing the historical development of resilience theory from equilibrium-centered ecological thinking through Holling’s 1973 intervention, nonlinear ecological resilience, adaptive management, adaptive cycles, panarchy, social-ecological systems, sustainability science, disaster risk reduction, climate-resilient development, and critical resilience debates.

## Correct article directory

```text
articles/history-of-resilience-theory/
```

## Purpose

The scaffold turns the article’s intellectual history into a reproducible knowledge-modeling workflow. It includes:

1. A historical phase dataset.
2. Conceptual expansion scores.
3. Equilibrium-return versus threshold-dynamics simulations.
4. Timeline and influence summaries.
5. SQL schemas for historical concepts, sources, phases, and model runs.
6. Multi-language examples for resilience-theory modeling.

## Responsible-use note

This is an analytical and educational scaffold, not a definitive historiography or bibliometric study. Historical interpretation requires scholarly judgment, source criticism, and attention to disciplinary context. The included scores are stylized and synthetic; they are designed to illustrate method, not to replace historical scholarship.

## Quick start

Run the dependency-light Python workflow:

```bash
python3 python/history_resilience_theory_standard.py
```

Optional advanced Python workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/history_resilience_theory_advanced.py
```

Run smoke checks:

```bash
bash smoke-test.sh
```

## Directory structure

```text
articles/history-of-resilience-theory/
├── python/       # Historical timeline modeling and threshold simulations
├── r/            # Historical expansion profiles and visualization workflow
├── julia/        # Nonlinear threshold/regime-transition examples
├── sql/          # Historical phase, concept, source, and model-run schemas
├── rust/         # CLI concept-score diagnostic scaffold
├── go/           # Timeline and phase utility scaffold
├── cpp/          # Fast equilibrium-vs-threshold simulation
├── fortran/      # Dynamic threshold persistence example
├── c/            # Low-level equilibrium-return utility
├── docs/         # Modeling principles, source notes, and interpretation guidance
├── data/         # Synthetic historical datasets
├── outputs/      # Generated outputs
└── notebooks/    # Notebook placeholders
```
