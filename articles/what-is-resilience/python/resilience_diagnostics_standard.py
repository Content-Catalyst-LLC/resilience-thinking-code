#!/usr/bin/env python3
"""
Dependency-light resilience diagnostics.

This standard-library workflow reads synthetic system data, calculates a
resilience profile, estimates risk pressure, flags threshold risk, simulates
viability under repeated disturbance, and exports CSV summaries.

Run:
    python3 python/resilience_diagnostics_standard.py
"""

from __future__ import annotations

import csv
import math
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw" / "synthetic_resilience_systems.csv"
OUTPUT_TABLES = ROOT / "outputs" / "tables"
OUTPUT_TABLES.mkdir(parents=True, exist_ok=True)


def f(value: str) -> float:
    return float(value)


def read_systems() -> list[dict[str, str]]:
    with DATA.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def resilience_profile(row: dict[str, str]) -> float:
    return (
        0.24 * f(row["adaptive_capacity"])
        + 0.20 * f(row["threshold_distance"])
        + 0.18 * f(row["learning_capacity"])
        + 0.14 * f(row["modularity"])
        + 0.14 * f(row["redundancy"])
        - 0.05 * f(row["exposure"])
        - 0.05 * f(row["sensitivity"])
    )


def risk_pressure(row: dict[str, str]) -> float:
    return 0.55 * f(row["exposure"]) + 0.45 * f(row["sensitivity"])


def flag_margin(margin: float) -> str:
    if margin < 0.15:
        return "high threshold risk"
    if margin < 0.30:
        return "moderate threshold risk"
    return "lower threshold risk"


def disturbance_series(steps: int = 60) -> list[float]:
    series = []
    for t in range(1, steps + 1):
        baseline = 0.055 + 0.025 * math.sin(t / 3.5)
        pulse = 0.0
        if t in {12, 24, 37, 48}:
            pulse = {12: 0.20, 24: 0.28, 37: 0.23, 48: 0.31}[t]
        series.append(max(0.0, baseline + pulse))
    return series


def simulate(row: dict[str, str], steps: int = 60) -> list[dict[str, object]]:
    profile = resilience_profile(row)
    pressure = risk_pressure(row)
    threshold_distance = f(row["threshold_distance"])

    viability = 1.0
    learning_memory = 0.0
    results = []

    for time_step, disturbance in enumerate(disturbance_series(steps), start=1):
        disturbance_load = disturbance * (0.65 + f(row["exposure"])) * (0.55 + f(row["sensitivity"]))
        protective_structure = 0.35 * f(row["redundancy"]) + 0.25 * f(row["modularity"])
        adaptive_response = 0.028 * f(row["adaptive_capacity"]) + 0.012 * f(row["learning_capacity"]) * (1 + learning_memory)

        net_impact = disturbance_load * (1 - 0.45 * protective_structure)
        viability = max(0.0, min(1.25, viability - net_impact + adaptive_response))
        learning_memory += 0.01 * f(row["learning_capacity"])

        margin = viability + threshold_distance - pressure

        results.append(
            {
                "system_id": row["system_id"],
                "system_type": row["system_type"],
                "time_step": time_step,
                "disturbance": round(disturbance, 4),
                "viability": round(viability, 4),
                "viability_margin": round(margin, 4),
                "threshold_flag": flag_margin(margin),
            }
        )

    return results


def main() -> None:
    systems = read_systems()

    profile_rows = []
    simulation_rows = []

    for row in systems:
        profile = resilience_profile(row)
        pressure = risk_pressure(row)
        margin = profile + f(row["threshold_distance"]) - pressure

        profile_rows.append(
            {
                "system_id": row["system_id"],
                "system_type": row["system_type"],
                "critical_function": row["critical_function"],
                "resilience_profile": round(profile, 4),
                "risk_pressure": round(pressure, 4),
                "initial_viability_margin": round(margin, 4),
                "risk_flag": flag_margin(margin),
            }
        )

        simulation_rows.extend(simulate(row))

    summary_rows = []
    for system in systems:
        sid = system["system_id"]
        subset = [r for r in simulation_rows if r["system_id"] == sid]
        summary_rows.append(
            {
                "system_id": sid,
                "system_type": system["system_type"],
                "minimum_viability": round(min(float(r["viability"]) for r in subset), 4),
                "average_viability": round(mean(float(r["viability"]) for r in subset), 4),
                "minimum_margin": round(min(float(r["viability_margin"]) for r in subset), 4),
                "threshold_risk_steps": sum(1 for r in subset if r["threshold_flag"] != "lower threshold risk"),
            }
        )

    for filename, rows in {
        "resilience_profiles_standard.csv": profile_rows,
        "resilience_simulation_standard.csv": simulation_rows,
        "resilience_summary_standard.csv": summary_rows,
    }.items():
        path = OUTPUT_TABLES / filename
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"Wrote {path.relative_to(ROOT)}")

    print("\nResilience diagnostics complete.")


if __name__ == "__main__":
    main()
