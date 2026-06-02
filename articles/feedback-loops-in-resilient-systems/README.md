# Feedback Loops in Resilient Systems

Companion repository folder for the article **“Feedback Loops in Resilient Systems.”**

This directory provides reproducible workflows for modeling reinforcing feedback, balancing feedback, delayed balancing behavior, loop polarity, policy resistance, adaptive-capacity feedback, learning loops, feedback blindness, and threshold-risk diagnostics.

## Correct article directory

```text
articles/feedback-loops-in-resilient-systems/
```

## Purpose

This scaffold supports a professional feedback-loop modeling workflow:

1. Represent feedback loops using causal polarity, loop type, gain, delay, target, adaptive capacity, disturbance load, and signal quality.
2. Simulate reinforcing growth, balancing correction, combined feedback, delayed balancing, and oscillatory behavior.
3. Compare delay sensitivity and overshoot risk.
4. Diagnose policy resistance when interventions reduce symptoms while strengthening underlying feedback problems.
5. Model adaptive-capacity feedback through sensing, interpretation, memory, authority, and revision.
6. Calculate feedback-risk profiles for ecological, institutional, infrastructure, climate, and economic systems.
7. Provide multi-language examples in Python, R, Julia, SQL, Rust, Go, C, C++, and Fortran.
8. Export reproducible tables, figures, documentation, and notebook placeholders.

## Responsible-use note

The data are synthetic and the models are methodological examples. They are intended for learning, reproducible article companions, dashboard prototyping, and professional modeling design. Real feedback-loop analysis requires system history, domain expertise, participatory review, empirical evidence, local knowledge, and uncertainty analysis.

Do not use these examples to claim definitive causal truth, rank communities, or justify intervention without validated evidence and accountable review.

## Quick start

Run the dependency-light Python workflow:

```bash
python3 python/feedback_loops_standard.py
```

Optional advanced Python workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/feedback_loops_advanced.py
```

Run smoke checks:

```bash
bash smoke-test.sh
```
