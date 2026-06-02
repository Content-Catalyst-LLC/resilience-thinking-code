# Public Health System Resilience

Companion repository folder for the article **Public Health System Resilience**.

This directory provides reproducible workflows for public health system resilience strategy comparison, prevention-detection-service-continuity scoring, workforce and trust diagnostics, adaptive-governance review, equity-adjusted resilience value, implementation-burden review, health-system stress simulation, and uncertainty-aware resilience planning.

## Correct article directory

```text
articles/public-health-system-resilience/
```

## Purpose

This scaffold supports a professional public health system resilience modeling workflow:

1. Define strategies across prevention, detection, service continuity, workforce capacity, adaptive governance, trust, equity protection, and implementation burden.
2. Compare strategies under balanced, prevention-first, detection-first, continuity-first, workforce-first, trust-first, equity-first, and implementation-sensitive priorities.
3. Simulate public health system function under infectious disease surge, heatwave, water contamination, cyber disruption, workforce burnout, and compound events.
4. Estimate equity-adjusted health-system resilience value and unequal service-access risk.
5. Diagnose implementation-burden review triggers, trust and communication gaps, service-continuity constraints, workforce limits, and equity-protection gaps.
6. Model uncertainty using Monte Carlo simulation.
7. Support responsible interpretation across surveillance, laboratories, workforce, essential services, emergency response, supply chains, risk communication, environmental health, digital systems, and community trust.
8. Provide multi-language examples in Python, R, Julia, SQL, Rust, Go, C, C++, and Fortran.
9. Export reproducible tables, figures, documentation, and notebook placeholders.

## Responsible-use note

The data are synthetic and the models are methodological examples. They are intended for learning, reproducible article companions, dashboard prototyping, and professional modeling design. Real public health resilience analysis requires local epidemiology, clinical capacity data, public-health authority, laboratory data, workforce data, community participation, privacy review, equity review, emergency management review, environmental health data, and accountable governance.

Do not use these examples to triage real patients, allocate scarce health resources, rank communities, certify public safety, replace epidemiological or clinical judgment, automate emergency decisions, or hide unequal exposure and recovery behind a single resilience score.

## Quick start

Run the dependency-light Python workflow:

```bash
python3 python/public_health_resilience_standard.py
```

Optional advanced Python workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/public_health_resilience_advanced.py
```

Run smoke checks:

```bash
bash smoke-test.sh
```
