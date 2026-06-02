# Adaptive Capacity in Complex Systems

Companion repository folder for the article **“Adaptive Capacity in Complex Systems.”**

This directory provides reproducible workflows for modeling adaptive capacity across ecosystems, institutions, communities, infrastructures, urban climate systems, and regional food systems. It focuses on response space, learning, flexibility, diversity, governance capacity, slack, trust, rigidity, exposure, viability, threshold risk, and scenario comparison.

## Correct article directory

```text
articles/adaptive-capacity-in-complex-systems/
```

## Purpose

This scaffold supports a professional adaptive-capacity workflow:

1. Represent systems using learning, flexibility, diversity, governance capacity, slack, trust/legitimacy, rigidity, exposure, and disturbance variables.
2. Build adaptive-capacity and adaptive-vulnerability scores.
3. Simulate viability under repeated disturbance and changing rigidity.
4. Flag threshold-risk periods when viability falls below a critical function level.
5. Classify adaptive-capacity failure risk using synthetic training data.
6. Compare response-space, rigidity, and governance scenarios.
7. Provide multi-language examples in Python, R, Julia, SQL, Rust, Go, C, C++, and Fortran.

## Responsible-use note

The data are synthetic and the models are methodological examples. They are intended for learning, reproducible article companions, dashboard prototyping, and professional modeling design. Real adaptive-capacity assessment requires calibrated domain data, participatory review, institutional context, ecological or infrastructure evidence, uncertainty analysis, and ethical safeguards.

Do not use these examples to rank communities, institutions, ecosystems, or infrastructure systems without validated evidence and accountable review.

## Quick start

Run the dependency-light Python workflow:

```bash
python3 python/adaptive_capacity_standard.py
```

Optional advanced Python workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/adaptive_capacity_advanced.py
```

Run smoke checks:

```bash
bash smoke-test.sh
```

## Directory structure

```text
articles/adaptive-capacity-in-complex-systems/
├── python/       # Adaptive-capacity scoring, viability simulation, threshold classification
├── r/            # Adaptive-capacity profile comparison and visualization
├── julia/        # Nonlinear response-space and rigidity examples
├── sql/          # Systems, indicators, disturbances, scenarios, model-run schemas
├── rust/         # CLI diagnostic scaffold
├── go/           # Adaptive-capacity profile utility
├── cpp/          # Fast viability simulation example
├── fortran/      # Dynamic adaptive-capacity viability example
├── c/            # Low-level adaptive-capacity score utility
├── docs/         # Modeling principles, validation, responsible use
├── data/         # Synthetic datasets
├── outputs/      # Generated tables, figures, and models
└── notebooks/    # Notebook placeholders
```
