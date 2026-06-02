# Regime Shifts and Early Warning Signals

Companion repository folder for the article **“Regime Shifts and Early Warning Signals.”**

This directory provides reproducible workflows for nonlinear regime-shift simulation, critical slowing down, rolling variance, lag-1 autocorrelation, recovery-speed proxies, threshold-proximity scoring, scenario comparison, monitoring quality, and responsible interpretation of early warning signals.

## Correct article directory

```text
articles/regime-shifts-and-early-warning-signals/
```

## Purpose

This scaffold supports a professional regime-shift and early-warning workflow:

1. Simulate nonlinear transitions between alternative regimes.
2. Calculate rolling variance and lag-1 autocorrelation.
3. Estimate recovery-speed proxies and threshold-proximity scores.
4. Compare gradual pressure, fast pressure, noisy monitoring, and adaptive intervention scenarios.
5. Diagnose regime-shift risk from pressure, feedback, variance, persistence, recovery speed, adaptive capacity, memory, and monitoring quality.
6. Support responsible interpretation across ecological, infrastructure, institutional, climate, economic, public-health, and social-ecological systems.
7. Provide multi-language examples in Python, R, Julia, SQL, Rust, Go, C, C++, and Fortran.
8. Export reproducible tables, figures, documentation, and notebook placeholders.

## Responsible-use note

The data are synthetic and the models are methodological examples. They are intended for learning, reproducible article companions, dashboard prototyping, and professional modeling design. Real early-warning work requires empirical data, system history, domain expertise, local knowledge, uncertainty review, and accountable governance.

Do not use these examples to claim exact tipping points, rank communities, predict collapse timing, or justify coercive intervention without validated evidence and ethical review.

## Quick start

Run the dependency-light Python workflow:

```bash
python3 python/regime_shifts_standard.py
```

Optional advanced Python workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/regime_shifts_advanced.py
```

Run smoke checks:

```bash
bash smoke-test.sh
```

## Directory structure

```text
articles/regime-shifts-and-early-warning-signals/
├── python/       # Regime-shift, early-warning, and scenario workflows
├── r/            # Regime-shift visualization and early-warning diagnostics
├── julia/        # Critical-transition and early-warning examples
├── sql/          # Systems, regimes, thresholds, warning signals, scenarios, model-run schemas
├── rust/         # CLI regime-risk diagnostic scaffold
├── go/           # Regime-risk diagnostic utility
├── cpp/          # Fast nonlinear transition simulation example
├── fortran/      # Dynamic regime-shift example
├── c/            # Low-level regime-risk utility
├── docs/         # Modeling principles, validation, responsible use
├── data/         # Synthetic datasets
├── outputs/      # Generated tables, figures, and models
└── notebooks/    # Notebook placeholders
```
