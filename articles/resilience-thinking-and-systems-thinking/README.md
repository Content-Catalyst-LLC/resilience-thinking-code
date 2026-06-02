# Resilience Thinking and Systems Thinking

Companion repository folder for the article **“Resilience Thinking and Systems Thinking.”**

This directory provides reproducible systems-resilience modeling workflows for connecting systems thinking and resilience thinking. It focuses on feedback loops, stocks and flows, delay diagnostics, disturbance loads, resilience margins, threshold risk, leverage points, boundary clarity, adaptive capacity, redundancy, and vulnerability pressure.

## Correct article directory

```text
articles/resilience-thinking-and-systems-thinking/
```

## Purpose

This scaffold supports a professional systems-resilience workflow:

1. Represent systems through feedback visibility, boundary clarity, leverage capacity, and delay management.
2. Represent resilience through adaptive capacity, redundancy, threshold distance, buffer capacity, and vulnerability pressure.
3. Simulate reinforcing vulnerability and balancing repair feedback loops.
4. Track stocks, flows, disturbance, and resilience margin over time.
5. Flag threshold risk when resilience margin falls below a viability threshold.
6. Compare systems-thinking scores and resilience-thinking scores.
7. Map leverage points and identify whether intervention should target parameters, buffers, information flows, rules, goals, or paradigms.
8. Produce reproducible outputs across multiple languages.

## Responsible-use note

The included data are synthetic and the models are methodological examples. They are intended for learning, reproducible article companions, dashboard prototyping, and professional modeling design. Real use requires system-specific evidence, expert review, uncertainty analysis, affected-community interpretation, and ethical safeguards.

Do not use these examples to rank communities, ecosystems, institutions, or infrastructure assets without calibrated data and accountable review.

## Quick start

Run the dependency-light Python workflow:

```bash
python3 python/systems_resilience_standard.py
```

Optional advanced Python workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/systems_resilience_advanced.py
```

Run smoke checks:

```bash
bash smoke-test.sh
```

## Directory structure

```text
articles/resilience-thinking-and-systems-thinking/
├── python/       # Feedback, disturbance, resilience-margin, and leverage workflows
├── r/            # Systems/resilience indicator comparison and visualization
├── julia/        # Nonlinear feedback and threshold examples
├── sql/          # System, feedback, stock, flow, threshold, and model-run schemas
├── rust/         # CLI diagnostic scaffold
├── go/           # Systems-resilience indicator utility
├── cpp/          # Fast feedback and resilience-margin simulation
├── fortran/      # Dynamic stock-flow margin example
├── c/            # Low-level balancing feedback utility
├── docs/         # Modeling principles, validation, responsible use
├── data/         # Synthetic datasets
├── outputs/      # Generated tables, figures, and models
└── notebooks/    # Notebook placeholders
```
