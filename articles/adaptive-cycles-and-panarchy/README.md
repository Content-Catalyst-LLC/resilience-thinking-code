# Adaptive Cycles and Panarchy

Companion repository folder for the article **“Adaptive Cycles and Panarchy.”**

This directory provides reproducible workflows for modeling adaptive-cycle phase dynamics, panarchy, cross-scale revolt and remember interactions, rigidity, memory, novelty, release thresholds, and reorganization pathways.

## Correct article directory

```text
articles/adaptive-cycles-and-panarchy/
```

## Purpose

This scaffold supports a professional adaptive-cycle and panarchy workflow:

1. Represent systems using potential, connectedness, resilience, rigidity, memory, novelty, and disturbance variables.
2. Simulate movement through growth or exploitation (`r`), conservation (`K`), release (`Omega`), and reorganization (`alpha`).
3. Diagnose when conservation becomes brittle through rising rigidity and falling resilience.
4. Model release thresholds and post-release reorganization.
5. Simulate cross-scale panarchy dynamics between fast and slow cycles.
6. Represent revolt effects from smaller/faster cycles to larger/slower cycles.
7. Represent remember effects from larger/slower cycles to smaller/faster cycles.
8. Compare scenarios and export reproducible tables, figures, and model outputs.
9. Provide multi-language examples in Python, R, Julia, SQL, Rust, Go, C, C++, and Fortran.

## Responsible-use note

The data are synthetic and the models are methodological examples. They are intended for learning, reproducible article companions, dashboard prototyping, and professional modeling design. Real adaptive-cycle or panarchy analysis requires empirical system history, domain expertise, ecological or institutional evidence, uncertainty analysis, and responsible interpretation.

Do not use these examples to claim precise collapse timing, rank communities, or justify crisis-driven restructuring without validated evidence and accountable public review.

## Quick start

Run the dependency-light Python workflow:

```bash
python3 python/adaptive_cycles_panarchy_standard.py
```

Optional advanced Python workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/adaptive_cycles_panarchy_advanced.py
```

Run smoke checks:

```bash
bash smoke-test.sh
```

## Directory structure

```text
articles/adaptive-cycles-and-panarchy/
├── python/       # Adaptive-cycle and panarchy simulations
├── r/            # Adaptive-cycle phase profiles and visualization
├── julia/        # Nonlinear phase-transition examples
├── sql/          # Systems, cycles, phases, indicators, scenarios, model-run schemas
├── rust/         # CLI diagnostic scaffold
├── go/           # Phase diagnostic utility
├── cpp/          # Fast adaptive-cycle simulation example
├── fortran/      # Dynamic phase-transition example
├── c/            # Low-level release-threshold utility
├── docs/         # Modeling principles, validation, responsible use
├── data/         # Synthetic datasets
├── outputs/      # Generated tables, figures, and models
└── notebooks/    # Notebook placeholders
```
