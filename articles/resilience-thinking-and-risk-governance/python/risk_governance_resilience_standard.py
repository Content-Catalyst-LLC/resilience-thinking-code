#!/usr/bin/env python3
"""
Dependency-light risk-governance and resilience workflow.

This script reads synthetic profiles, calculates risk pressure, governance
capacity, resilience capacity, resilience margin, simulates disturbance over
time, flags threshold risk, and exports results using only the Python standard
library.

Run:
    python3 python/risk_governance_resilience_standard.py
"""

from __future__ import annotations

import csv
import math
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
PROFILES_PATH = ROOT / "data" / "raw" / "risk_governance_resilience_profiles.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "disturbance_scenarios.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
DATA_PROCESSED = ROOT / "data" / "processed"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)


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


def risk_pressure(row: dict[str, str]) -> float:
    return (
        f(row, "hazard_intensity")
        * f(row, "exposure")
        * f(row, "vulnerability")
        * (1.0 - 0.55 * f(row, "adaptive_capacity"))
    )


def governance_capacity(row: dict[str, str]) -> float:
    return (
        0.18 * f(row, "trust")
        + 0.17 * f(row, "participation_quality")
        + 0.17 * f(row, "knowledge_integration")
        + 0.18 * f(row, "coordination_quality")
        + 0.15 * f(row, "transparency")
        + 0.15 * f(row, "accountability")
    )


def resilience_capacity(row: dict[str, str], governance: float) -> float:
    return (
        0.26 * f(row, "buffer_capacity")
        + 0.28 * f(row, "adaptive_capacity")
        + 0.22 * f(row, "learning_capacity")
        + 0.24 * governance
    )


def resilience_margin(row: dict[str, str], rp: float, gc: float) -> float:
    return (
        f(row, "buffer_capacity")
        + f(row, "adaptive_capacity")
        + f(row, "learning_capacity")
        + gc
        - rp
        - f(row, "vulnerability")
    )


def diagnostic(margin: float) -> str:
    if margin < 1.05:
        return "high governance-resilience concern"
    if margin < 1.45:
        return "moderate governance-resilience concern"
    return "stronger governance-resilience position"


def simulate_system(row: dict[str, str], scenario: dict[str, str], base_margin: float, base_governance: float, steps: int = 84) -> list[dict[str, object]]:
    margin = base_margin
    vulnerability = f(row, "vulnerability")
    adaptive = f(row, "adaptive_capacity")
    learning = f(row, "learning_capacity")
    exposure = f(row, "exposure")

    disturbance_load = float(scenario["disturbance_load"])
    shock_intensity = float(scenario["shock_intensity"])
    shock_frequency = int(float(scenario["shock_frequency"]))
    governance_stress = float(scenario["governance_stress"])

    rows = []

    for t in range(1, steps + 1):
        seasonal = 0.05 + 0.025 * math.sin(t / 7.0)
        shock = shock_intensity if shock_frequency > 0 and t % shock_frequency == 0 else 0.0
        disturbance = disturbance_load + seasonal + shock

        governance_response = 0.018 * base_governance * (1.0 - 0.35 * governance_stress)
        adaptive_response = 0.014 * adaptive + 0.010 * learning
        vulnerability_amplification = 0.020 * vulnerability + 0.010 * exposure
        disturbance_effect = disturbance * (0.35 + 0.55 * exposure)

        margin = margin - disturbance_effect - vulnerability_amplification + governance_response + adaptive_response
        margin = max(-2.0, min(2.5, margin))

        rows.append(
            {
                "system_id": row["system_id"],
                "system_type": row["system_type"],
                "scenario_id": scenario["scenario_id"],
                "scenario_name": scenario["scenario_name"],
                "time_step": t,
                "disturbance": round(disturbance, 4),
                "resilience_margin": round(margin, 4),
                "threshold_flag": "threshold risk" if margin < 0.75 else "viable margin",
            }
        )

    return rows


def main() -> None:
    profiles = read_csv(PROFILES_PATH)
    scenarios = read_csv(SCENARIOS_PATH)

    profile_rows = []
    simulation_rows = []

    for row in profiles:
        rp = risk_pressure(row)
        gc = governance_capacity(row)
        rc = resilience_capacity(row, gc)
        rm = resilience_margin(row, rp, gc)

        profile_rows.append(
            {
                "system_id": row["system_id"],
                "system_type": row["system_type"],
                "critical_function": row["critical_function"],
                "risk_pressure": round(rp, 4),
                "governance_capacity": round(gc, 4),
                "resilience_capacity": round(rc, 4),
                "resilience_margin": round(rm, 4),
                "diagnostic": diagnostic(rm),
            }
        )

        for scenario in scenarios:
            simulation_rows.extend(simulate_system(row, scenario, rm, gc))

    summary_rows = []
    for row in profiles:
        sid = row["system_id"]
        subset = [r for r in simulation_rows if r["system_id"] == sid]
        summary_rows.append(
            {
                "system_id": sid,
                "system_type": row["system_type"],
                "minimum_margin": round(min(float(r["resilience_margin"]) for r in subset), 4),
                "average_margin": round(mean(float(r["resilience_margin"]) for r in subset), 4),
                "threshold_risk_steps": sum(1 for r in subset if r["threshold_flag"] == "threshold risk"),
            }
        )

    write_csv(OUT_TABLES / "risk_governance_profiles_standard.csv", profile_rows)
    write_csv(OUT_TABLES / "risk_governance_simulation_standard.csv", simulation_rows)
    write_csv(OUT_TABLES / "risk_governance_summary_standard.csv", summary_rows)
    write_csv(DATA_PROCESSED / "risk_governance_profiles_standard.csv", profile_rows)

    print("Risk-governance resilience workflow complete.")
    for row in profile_rows:
        print(
            f"  {row['system_type']}: risk={row['risk_pressure']} "
            f"governance={row['governance_capacity']} margin={row['resilience_margin']}"
        )


if __name__ == "__main__":
    main()
