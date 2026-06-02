#!/usr/bin/env python3
"""
Dependency-light systems-resilience workflow.

This script reads synthetic systems-resilience profiles, calculates systems-
thinking and resilience-thinking scores, simulates feedback-driven vulnerability
stocks under disturbance, flags threshold risk, and exports results using only
the Python standard library.

Run:
    python3 python/systems_resilience_standard.py
"""

from __future__ import annotations

import csv
import math
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
PROFILES_PATH = ROOT / "data" / "raw" / "systems_resilience_profiles.csv"
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


def systems_thinking_score(row: dict[str, str]) -> float:
    return (
        0.28 * f(row, "feedback_visibility")
        + 0.24 * f(row, "boundary_clarity")
        + 0.24 * f(row, "leverage_capacity")
        + 0.24 * f(row, "delay_management")
    )


def resilience_thinking_score(row: dict[str, str]) -> float:
    return (
        0.24 * f(row, "adaptive_capacity")
        + 0.20 * f(row, "redundancy")
        + 0.22 * f(row, "threshold_distance")
        + 0.18 * f(row, "buffer_capacity")
        - 0.08 * f(row, "vulnerability_pressure")
        - 0.08 * f(row, "disturbance_exposure")
    )


def diagnostic(systems_score: float, resilience_score: float) -> str:
    if systems_score < 0.55 and resilience_score < 0.55:
        return "weak structure visibility and weak resilience capacity"
    if systems_score >= 0.65 and resilience_score >= 0.65:
        return "strong structural understanding and resilience capacity"
    if systems_score > resilience_score:
        return "structure is visible but resilience capacity needs strengthening"
    return "resilience capacity exists but system structure needs clearer mapping"


def simulate_system(row: dict[str, str], scenario: dict[str, str], steps: int = 80) -> list[dict[str, object]]:
    vulnerability_stock = f(row, "vulnerability_pressure")
    buffer_capacity = f(row, "buffer_capacity")
    adaptive_capacity = f(row, "adaptive_capacity")
    threshold_distance = f(row, "threshold_distance")
    reinforcing_vulnerability = f(row, "reinforcing_vulnerability")
    balancing_repair = f(row, "balancing_repair")
    feedback_delay = int(float(row["feedback_delay"]))

    disturbance_load = float(scenario["disturbance_load"])
    shock_intensity = float(scenario["shock_intensity"])
    shock_frequency = int(float(scenario["shock_frequency"]))
    delay_penalty = float(scenario["delay_penalty"])

    history_disturbance = []
    rows = []

    for t in range(1, steps + 1):
        periodic_shock = shock_intensity if shock_frequency > 0 and t % max(1, shock_frequency) == 0 else 0.0
        seasonal_wave = 0.04 + 0.025 * math.sin(t / 6.0)
        disturbance = disturbance_load + periodic_shock + seasonal_wave
        history_disturbance.append(disturbance)

        observed_index = max(0, len(history_disturbance) - 1 - feedback_delay)
        observed_disturbance = history_disturbance[observed_index]

        reinforcing_growth = reinforcing_vulnerability * vulnerability_stock
        disturbance_effect = 0.32 * disturbance
        delayed_repair = balancing_repair * observed_disturbance * (1.0 - 0.35 * delay_penalty)
        adaptive_response = 0.012 * adaptive_capacity + 0.006 * f(row, "redundancy")

        vulnerability_stock = vulnerability_stock + reinforcing_growth + disturbance_effect - delayed_repair - adaptive_response
        vulnerability_stock = max(0.0, min(2.0, vulnerability_stock))

        resilience_margin = (
            buffer_capacity
            + adaptive_capacity
            + 0.60 * threshold_distance
            - vulnerability_stock
            - 0.20 * disturbance
        )

        viability_threshold = 0.25

        rows.append(
            {
                "system_id": row["system_id"],
                "system_type": row["system_type"],
                "scenario_id": scenario["scenario_id"],
                "scenario_name": scenario["scenario_name"],
                "time_step": t,
                "disturbance": round(disturbance, 4),
                "vulnerability_stock": round(vulnerability_stock, 4),
                "resilience_margin": round(resilience_margin, 4),
                "threshold_flag": "threshold risk" if resilience_margin < viability_threshold else "viable margin",
            }
        )

    return rows


def main() -> None:
    systems = read_csv(PROFILES_PATH)
    scenarios = read_csv(SCENARIOS_PATH)

    profile_rows = []
    simulation_rows = []

    for row in systems:
        sys_score = systems_thinking_score(row)
        res_score = resilience_thinking_score(row)
        combined = 0.50 * sys_score + 0.50 * res_score

        profile_rows.append(
            {
                "system_id": row["system_id"],
                "system_type": row["system_type"],
                "critical_function": row["critical_function"],
                "systems_thinking_score": round(sys_score, 4),
                "resilience_thinking_score": round(res_score, 4),
                "combined_system_resilience": round(combined, 4),
                "diagnostic": diagnostic(sys_score, res_score),
            }
        )

        for scenario in scenarios:
            simulation_rows.extend(simulate_system(row, scenario))

    summary_rows = []
    for row in systems:
        sid = row["system_id"]
        subset = [r for r in simulation_rows if r["system_id"] == sid]
        summary_rows.append(
            {
                "system_id": sid,
                "system_type": row["system_type"],
                "minimum_margin": round(min(float(r["resilience_margin"]) for r in subset), 4),
                "average_margin": round(mean(float(r["resilience_margin"]) for r in subset), 4),
                "maximum_vulnerability_stock": round(max(float(r["vulnerability_stock"]) for r in subset), 4),
                "threshold_risk_steps": sum(1 for r in subset if r["threshold_flag"] == "threshold risk"),
            }
        )

    write_csv(OUT_TABLES / "systems_resilience_profiles_standard.csv", profile_rows)
    write_csv(OUT_TABLES / "systems_resilience_simulation_standard.csv", simulation_rows)
    write_csv(OUT_TABLES / "systems_resilience_summary_standard.csv", summary_rows)
    write_csv(DATA_PROCESSED / "systems_resilience_profiles_standard.csv", profile_rows)

    print("Systems-resilience workflow complete.")
    for row in profile_rows:
        print(
            f"  {row['system_type']}: systems={row['systems_thinking_score']} "
            f"resilience={row['resilience_thinking_score']} combined={row['combined_system_resilience']}"
        )


if __name__ == "__main__":
    main()
