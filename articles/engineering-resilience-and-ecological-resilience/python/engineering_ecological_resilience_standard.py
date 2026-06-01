#!/usr/bin/env python3
"""
Dependency-light workflow for comparing engineering resilience and ecological resilience.

This script reads synthetic system data, calculates engineering-resilience and
ecological-resilience scores, evaluates imbalance, runs a simple threshold
margin simulation, and exports results using only the Python standard library.

Run:
    python3 python/engineering_ecological_resilience_standard.py
"""

from __future__ import annotations

import csv
import math
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
SYSTEMS_PATH = ROOT / "data" / "raw" / "engineering_ecological_resilience_systems.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "disturbance_scenarios.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_TABLES.mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def f(row: dict[str, str], key: str) -> float:
    return float(row[key])


def engineering_score(row: dict[str, str]) -> float:
    return (
        0.28 * f(row, "return_speed")
        + 0.24 * f(row, "reliability")
        + 0.18 * f(row, "repair_capacity")
        + 0.15 * f(row, "backup_capacity")
        + 0.15 * f(row, "service_continuity")
    )


def ecological_score(row: dict[str, str]) -> float:
    return (
        0.20 * f(row, "threshold_distance")
        + 0.18 * f(row, "basin_width")
        + 0.18 * f(row, "adaptive_capacity")
        + 0.15 * f(row, "functional_diversity")
        + 0.13 * f(row, "redundancy")
        + 0.10 * f(row, "modularity")
        - 0.08 * f(row, "disturbance_exposure")
        - 0.08 * f(row, "regime_shift_sensitivity")
    )


def interpret_gap(gap: float) -> str:
    if gap <= -0.18:
        return "strong engineering return but weaker threshold persistence"
    if gap >= 0.18:
        return "stronger ecological adaptive capacity than operational return"
    return "more balanced engineering/ecological resilience profile"


def simulate_margin(row: dict[str, str], scenario: dict[str, str], steps: int = 60) -> list[dict[str, object]]:
    basin = f(row, "basin_width")
    adaptive = f(row, "adaptive_capacity")
    redundancy = f(row, "redundancy")
    modularity = f(row, "modularity")
    exposure = f(row, "disturbance_exposure")
    sensitivity = f(row, "regime_shift_sensitivity")

    disturbance_load = float(scenario["disturbance_load"])
    shock_intensity = float(scenario["shock_intensity"])
    compound_risk = float(scenario["compound_risk"])

    margin = basin + 0.5 * adaptive
    rows = []

    for t in range(1, steps + 1):
        pulse = shock_intensity if t in {12, 24, 36, 48} else 0.0
        recurring_pressure = disturbance_load * (0.55 + exposure) * (0.50 + sensitivity)
        protection = 0.30 * redundancy + 0.25 * modularity + 0.20 * adaptive
        erosion = (recurring_pressure + pulse + 0.20 * compound_risk) * (1.0 - 0.40 * protection)
        learning_repair = 0.012 * adaptive + 0.006 * redundancy

        margin = max(-1.0, min(1.5, margin - 0.045 * erosion + learning_repair))
        rows.append(
            {
                "system_id": row["system_id"],
                "system_type": row["system_type"],
                "scenario_id": scenario["scenario_id"],
                "scenario_name": scenario["scenario_name"],
                "time_step": t,
                "resilience_margin": round(margin, 4),
                "threshold_flag": "threshold risk" if margin < 0.20 else "viable margin",
            }
        )

    return rows


def main() -> None:
    systems = read_csv(SYSTEMS_PATH)
    scenarios = read_csv(SCENARIOS_PATH)

    profile_rows = []
    simulation_rows = []

    for row in systems:
        eng = engineering_score(row)
        eco = ecological_score(row)
        gap = eco - eng

        profile_rows.append(
            {
                "system_id": row["system_id"],
                "system_type": row["system_type"],
                "critical_function": row["critical_function"],
                "engineering_resilience": round(eng, 4),
                "ecological_resilience": round(eco, 4),
                "resilience_gap": round(gap, 4),
                "interpretation": interpret_gap(gap),
            }
        )

        for scenario in scenarios:
            simulation_rows.extend(simulate_margin(row, scenario))

    summary_rows = []
    for system in systems:
        sid = system["system_id"]
        subset = [r for r in simulation_rows if r["system_id"] == sid]
        summary_rows.append(
            {
                "system_id": sid,
                "system_type": system["system_type"],
                "minimum_margin": round(min(float(r["resilience_margin"]) for r in subset), 4),
                "average_margin": round(mean(float(r["resilience_margin"]) for r in subset), 4),
                "threshold_risk_steps": sum(1 for r in subset if r["threshold_flag"] == "threshold risk"),
            }
        )

    write_csv(OUT_TABLES / "engineering_ecological_profiles_standard.csv", profile_rows)
    write_csv(OUT_TABLES / "resilience_margin_simulation_standard.csv", simulation_rows)
    write_csv(OUT_TABLES / "resilience_margin_summary_standard.csv", summary_rows)

    print("Engineering vs ecological resilience workflow complete.")
    for row in profile_rows:
        print(f"  {row['system_type']}: eng={row['engineering_resilience']} eco={row['ecological_resilience']} gap={row['resilience_gap']}")


if __name__ == "__main__":
    main()
