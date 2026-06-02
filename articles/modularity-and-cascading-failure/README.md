# Modularity and Cascading Failure

Companion repository folder for the article **“Modularity and Cascading Failure.”**

This directory provides reproducible workflows for modeling dependency networks, modular containment, cascading failure propagation, common-mode exposure, isolation capacity, justice-weighted impact, and uncertainty-aware cascade-risk analysis.

## Correct article directory

```text
articles/modularity-and-cascading-failure/
```

## Purpose

This scaffold supports a professional modularity-and-cascade analysis workflow:

1. Define system nodes, dependency links, coupling strength, redundancy, isolation capacity, and common-mode exposure.
2. Simulate cascade propagation after initial node failures.
3. Estimate probability of large cascades and justice-weighted impact.
4. Compare cascade-containment strategies across modularity, redundancy, dependency mapping, isolation capacity, coordination readiness, justice protection, and common-mode risk.
5. Model uncertainty using Monte Carlo simulation.
6. Diagnose critical nodes, bridge dependencies, common-mode failure, and fragile modules.
7. Support responsible interpretation across infrastructure, digital systems, ecosystems, institutions, public health, supply chains, and social-ecological systems.
8. Provide multi-language examples in Python, R, Julia, SQL, Rust, Go, C, C++, and Fortran.
9. Export reproducible tables, figures, documentation, and notebook placeholders.

## Responsible-use note

The data are synthetic and the models are methodological examples. They are intended for learning, reproducible article companions, dashboard prototyping, and professional modeling design. Real cascade-risk analysis requires empirical dependency data, domain expertise, engineering review, ecological knowledge, local knowledge, governance review, uncertainty analysis, and public accountability.

Do not use these examples to claim that a system is safe, rank communities, withdraw public protection, or replace field validation and participatory governance with model output.

## Quick start

Run the dependency-light Python workflow:

```bash
python3 python/modularity_cascade_standard.py
```

Optional advanced Python workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/modularity_cascade_advanced.py
```

Run smoke checks:

```bash
bash smoke-test.sh
```

## Directory structure

```text
articles/modularity-and-cascading-failure/
├── python/       # Cascade simulation, strategy scoring, uncertainty
├── r/            # Scenario-weighted containment strategy comparison
├── julia/        # Network cascade examples
├── sql/          # Nodes, dependencies, strategies, cascades, scenarios
├── rust/         # CLI containment-value diagnostic scaffold
├── go/           # Cascade diagnostic utility
├── cpp/          # Fast containment scoring example
├── fortran/      # Dynamic cascade propagation example
├── c/            # Low-level containment-value utility
├── docs/         # Modeling principles, validation, responsible use
├── data/         # Synthetic datasets
├── outputs/      # Generated tables, figures, and models
└── notebooks/    # Notebook placeholders
```
