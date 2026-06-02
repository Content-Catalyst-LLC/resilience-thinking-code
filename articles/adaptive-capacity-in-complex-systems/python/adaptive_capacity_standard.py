#!/usr/bin/env python3
"""
Dependency-light adaptive capacity workflow.

Reads synthetic adaptive-capacity profiles and disturbance scenarios, calculates
adaptive-capacity profiles, adaptive vulnerability, response-space diagnostics,
viability simulations, and threshold-risk summaries using only the Python
standard library.

Run:
    python3 python/adaptive_capacity_standard.py
"""

from __future__ import annotations

import csv
import math
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
PROFILES_PATH = ROOT / "data" / "raw" / "adaptive_capacity_profiles.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "disturbance_scenarios.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
DATA_PROCESSED = ROOT / "data" / "processed"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def f(row: dict[str, str], key: str) -> float:
    return float(row[key])


def adaptive_capacity_score(row: dict[str, str]) -> float:
    return (
        0.18 * f(row, "learning")
        + 0.18 * f(row, "flexibility")
        + 0.17 * f(row, "diversity")
        + 0.17 * f(row, "governance_capacity")
        + 0.14 * f(row, "slack")
        + 0.16 * f(row, "trust_legitimacy")
        - 0.12 * f(row, "rigidity")
    )


def adaptive_vulnerability_score(row: dict[str, str]) -> float:
    return (
        0.34 * f(row, "exposure")
        + 0.24 * f(row, "rigidity")
        + 0.16 * (1.0 - f(row, "slack"))
        + 0.14 * (1.0 - f(row, "trust_legitimacy"))
        + 0.12 * (1.0 - f(row, "governance_capacity"))
    )


def diagnostic(row: dict[str, str], capacity: float, vulnerability: float) -> str:
    if capacity >= 0.58 and vulnerability < 0.55:
        return "stronger adaptive-capacity profile"
    if vulnerability >= 0.66:
        return "high adaptive-vulnerability concern"
    if f(row, "rigidity") >= 0.62:
        return "rigidity and lock-in concern"
    return "mixed adaptive-capacity profile requiring monitoring"


def simulate_viability(system: dict[str, str], scenario: dict[str, str], steps: int = 80) -> list[dict[str, object]]:
    capacity = adaptive_capacity_score(system)
    vulnerability = adaptive_vulnerability_score(system)
    rigidity = f(system, "rigidity")
    exposure = f(system, "exposure")
    viability = 1.0

    disturbance_load = float(scenario["disturbance_load"])
    shock_intensity = float(scenario["shock_intensity"])
    shock_frequency = int(float(scenario["shock_frequency"]))
    learning_gain = float(scenario["learning_gain"])
    rigidity_growth = float(scenario["rigidity_growth"])
    governance_response = float(scenario["governance_response"])

    rows = []

    for t in range(1, steps + 1):
        seasonal = 0.04 + 0.025 * math.sin(t / 8.0)
        shock = shock_intensity if shock_frequency > 0 and t % shock_frequency == 0 else 0.0
        disturbance = disturbance_load + seasonal + shock + 0.18 * exposure

        capacity = max(0.0, min(1.2, capacity + learning_gain + 0.006 * governance_response - 0.010 * rigidity))
        rigidity = max(0.0, min(1.0, rigidity + rigidity_growth + 0.004 * disturbance - 0.006 * governance_response))

        response_space = capacity + 0.35 * f(system, "slack") + 0.25 * f(system, "trust_legitimacy") - rigidity - 0.25 * vulnerability

        viability = (
            viability
            - 0.46 * disturbance
            + 0.25 * capacity
            + 0.08 * response_space
            - 0.12 * rigidity
        )
        viability = max(0.0, min(1.2, viability))

        rows.append(
            {
                "system_id": system["system_id"],
                "system_type": system["system_type"],
                "scenario_id": scenario["scenario_id"],
                "scenario_name": scenario["scenario_name"],
                "time_step": t,
                "disturbance": round(disturbance, 5),
                "adaptive_capacity": round(capacity, 5),
                "rigidity": round(rigidity, 5),
                "response_space": round(response_space, 5),
                "viability": round(viability, 5),
                "threshold_flag": "threshold risk" if viability < 0.45 else "viable margin",
            }
        )

    return rows


def main() -> None:
    systems = read_csv(PROFILES_PATH)
    scenarios = read_csv(SCENARIOS_PATH)

    profile_rows = []
    simulation_rows = []

    for system in systems:
        capacity = adaptive_capacity_score(system)
        vulnerability = adaptive_vulnerability_score(system)
        profile_rows.append(
            {
                "system_id": system["system_id"],
                "system_type": system["system_type"],
                "critical_function": system["critical_function"],
                "adaptive_capacity": round(capacity, 4),
                "adaptive_vulnerability": round(vulnerability, 4),
                "response_space_baseline": round(capacity - vulnerability, 4),
                "rigidity": system["rigidity"],
                "exposure": system["exposure"],
                "diagnostic": diagnostic(system, capacity, vulnerability),
            }
        )

        for scenario in scenarios:
            simulation_rows.extend(simulate_viability(system, scenario))

    summary_rows = []
    for system in systems:
        sid = system["system_id"]
        subset = [r for r in simulation_rows if r["system_id"] == sid]
        summary_rows.append(
            {
                "system_id": sid,
                "system_type": system["system_type"],
                "minimum_viability": round(min(float(r["viability"]) for r in subset), 4),
                "final_viability": round(float(subset[-1]["viability"]), 4),
                "average_response_space": round(mean(float(r["response_space"]) for r in subset), 4),
                "threshold_risk_steps": sum(1 for r in subset if r["threshold_flag"] == "threshold risk"),
            }
        )

    write_csv(OUT_TABLES / "adaptive_capacity_profiles_standard.csv", profile_rows)
    write_csv(OUT_TABLES / "adaptive_capacity_viability_simulation_standard.csv", simulation_rows)
    write_csv(OUT_TABLES / "adaptive_capacity_viability_summary_standard.csv", summary_rows)
    write_csv(DATA_PROCESSED / "adaptive_capacity_profiles_standard.csv", profile_rows)

    print("Adaptive capacity workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    for row in profile_rows:
        print(
            f"  {row['system_type']}: capacity={row['adaptive_capacity']} "
            f"vulnerability={row['adaptive_vulnerability']} diagnostic={row['diagnostic']}"
        )


if __name__ == "__main__":
    main()
