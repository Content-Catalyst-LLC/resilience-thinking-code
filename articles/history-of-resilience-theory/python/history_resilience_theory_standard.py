#!/usr/bin/env python3
"""
Dependency-light historical resilience-theory workflow.

This script reads a stylized historical phase dataset, computes an influence
score, exports summary tables, and simulates the conceptual shift from
equilibrium-return logic to threshold-persistence logic using only the Python
standard library.

Run:
    python3 python/history_resilience_theory_standard.py
"""

from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw" / "resilience_theory_historical_phases.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_TABLES.mkdir(parents=True, exist_ok=True)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def f(row: dict[str, str], key: str) -> float:
    return float(row[key])


def influence_score(row: dict[str, str]) -> float:
    return (
        0.35 * f(row, "conceptual_scope")
        + 0.25 * f(row, "governance_relevance")
        + 0.25 * f(row, "system_complexity")
        + 0.15 * f(row, "justice_relevance")
    )


def simulate_equilibrium_return(steps: int = 160) -> list[dict[str, float]]:
    x_star = 0.0
    a = 0.10
    x = 1.0
    rows = []

    for t in range(1, steps + 1):
        if t > 1:
            x = x - a * (x - x_star)
        rows.append({"time": t, "equilibrium_state": round(x, 6)})

    return rows


def simulate_threshold_dynamics(steps: int = 160) -> list[dict[str, float]]:
    x = -0.9
    r = 1.1
    dt = 0.05
    rows = []

    for t in range(1, steps + 1):
        pressure = -0.45 + (1.30 * (t - 1) / (steps - 1))
        if t > 1:
            x = x + dt * (r * x - x**3 + pressure)

        basin_width = 0.85 - 0.40 * ((t - 1) / (steps - 1))
        disturbance_load = 0.10 + 0.60 * ((t - 1) / (steps - 1))
        adaptive_capacity = 0.35 + 0.20 * math.sin(t / 18.0)
        resilience_margin = basin_width - disturbance_load + adaptive_capacity

        rows.append(
            {
                "time": t,
                "pressure": round(pressure, 6),
                "threshold_state": round(x, 6),
                "basin_width": round(basin_width, 6),
                "disturbance_load": round(disturbance_load, 6),
                "adaptive_capacity": round(adaptive_capacity, 6),
                "resilience_margin": round(resilience_margin, 6),
            }
        )

    return rows


def main() -> None:
    rows = read_rows(DATA)

    scored = []
    for row in rows:
        scored.append(
            {
                **row,
                "influence_score": round(influence_score(row), 4),
            }
        )

    scored_sorted = sorted(scored, key=lambda row: float(row["influence_score"]), reverse=True)

    eq = simulate_equilibrium_return()
    threshold = simulate_threshold_dynamics()

    merged = []
    for e, th in zip(eq, threshold):
        merged.append({**e, **{k: v for k, v in th.items() if k != "time"}})

    write_rows(OUT_TABLES / "history_phase_scores_standard.csv", scored)
    write_rows(OUT_TABLES / "history_phase_scores_ranked_standard.csv", scored_sorted)
    write_rows(OUT_TABLES / "equilibrium_vs_threshold_standard.csv", merged)

    print("Historical resilience-theory workflow complete.")
    print("Top historical phases by stylized influence score:")
    for row in scored_sorted[:5]:
        print(f"  {row['period']}: {row['influence_score']}")

    print(f"\nWrote outputs to: {OUT_TABLES.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
