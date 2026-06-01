# Engineering Resilience and Ecological Resilience

Companion repository folder for the article **“Engineering Resilience and Ecological Resilience.”**

This directory provides reproducible comparative modeling workflows for distinguishing engineering resilience from ecological resilience. It focuses on recovery speed, reliability, repair capacity, return-to-equilibrium behavior, threshold distance, basin width, adaptive capacity, functional diversity, redundancy, disturbance exposure, and regime-shift risk.

## Correct article directory

```text
articles/engineering-resilience-and-ecological-resilience/
```

## Purpose

This scaffold is designed to support a professional comparative workflow:

1. Define engineering-resilience variables: return speed, reliability, repair capacity, backup capacity, and service continuity.
2. Define ecological-resilience variables: threshold distance, basin width, adaptive capacity, functional diversity, redundancy, ecological memory, and disturbance exposure.
3. Compare how systems can score differently under the two resilience lenses.
4. Simulate return-to-equilibrium behavior versus threshold-dynamics behavior.
5. Identify systems that recover quickly but remain close to thresholds.
6. Generate scenario diagnostics and reproducible outputs.
7. Document modeling assumptions and responsible-use cautions.

## Responsible-use note

The data are synthetic and the models are methodological examples. They are intended for learning, reproducible article companions, dashboard prototyping, and professional modeling design. Real use requires system-specific evidence, engineering review, ecological expertise, uncertainty analysis, and stakeholder interpretation.

Do not use these examples to rank communities, ecosystems, or infrastructure assets without calibrated data, local review, and ethical safeguards.

## Quick start

Run the dependency-light Python workflow:

```bash
python3 python/engineering_ecological_resilience_standard.py
```

Optional advanced Python workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/engineering_ecological_resilience_advanced.py
```

Run smoke checks:

```bash
bash smoke-test.sh
```

## Directory structure

```text
articles/engineering-resilience-and-ecological-resilience/
├── python/       # Comparative scoring, simulations, scenario diagnostics
├── r/            # Engineering/ecological profile comparison and visualization
├── julia/        # Threshold dynamics and regime-shift examples
├── sql/          # System, disturbance, recovery, threshold, and model-run schemas
├── rust/         # CLI diagnostic scaffold
├── go/           # Scenario comparison utility
├── cpp/          # Fast return-vs-threshold simulation
├── fortran/      # Dynamic threshold-margin example
├── c/            # Low-level return-rate utility
├── docs/         # Modeling principles, validation, responsible use
├── data/         # Synthetic datasets
├── outputs/      # Generated tables, figures, and models
└── notebooks/    # Notebook placeholders
```
