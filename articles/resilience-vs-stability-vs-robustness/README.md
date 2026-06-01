# Resilience vs Stability vs Robustness

Companion repository folder for the article **“Resilience vs Stability vs Robustness.”**

This folder is an advanced predictive-model scaffold for comparing stability, robustness, reliability, recovery, and resilience under disturbance. It provides synthetic-data generation, feature engineering, baseline predictive modeling, scenario forecasting, threshold-risk diagnostics, and multi-language numerical examples.

## Correct article directory

```text
articles/resilience-vs-stability-vs-robustness/
```

## Purpose

The purpose of this scaffold is to demonstrate how a predictive model of resilience could be structured:

1. Define system features: stability, robustness, adaptive capacity, threshold distance, learning capacity, redundancy, modularity, exposure, sensitivity, and disturbance load.
2. Generate or ingest observation-level system data.
3. Engineer predictive features and outcome labels.
4. Train baseline predictive models for resilience outcome risk.
5. Evaluate model performance.
6. Produce scenario-level predictions.
7. Interpret predictions through the lens of thresholds, uncertainty, and ethical responsibility.

## Responsible-use warning

The included data are synthetic and the models are methodological examples. They are not validated real-world prediction tools. Any real predictive use requires:

- domain-specific data
- external validation
- uncertainty analysis
- model-governance documentation
- affected-community review where social systems are involved
- safeguards against using resilience scores to justify abandonment, austerity, or burden shifting

## Quick start

Run the dependency-light predictive pipeline:

```bash
python3 python/predictive_resilience_model_standard.py
```

Run the optional advanced Python pipeline:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/predictive_resilience_model_advanced.py
```

Run smoke checks:

```bash
bash smoke-test.sh
```

## Directory structure

```text
articles/resilience-vs-stability-vs-robustness/
├── python/       # Predictive pipelines and scenario forecasting
├── r/            # Predictive profile comparisons and validation workflow
├── julia/        # Nonlinear threshold prediction example
├── sql/          # Model input, prediction, metric, and scenario schemas
├── rust/         # CLI diagnostic scaffold
├── go/           # Network resilience forecast utility
├── cpp/          # Fast repeated-disturbance simulation
├── fortran/      # Dynamic threshold margin simulation
├── c/            # Low-level viability prediction utility
├── docs/         # Modeling principles, validation, and ethics
├── data/         # Synthetic model inputs
├── outputs/      # Generated predictions, metrics, models, and figures
└── notebooks/    # Notebook placeholders
```
