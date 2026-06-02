#!/usr/bin/env python3
"""
Dependency-light ecosystem-service resilience workflow.

This script reads synthetic ecosystem-service profiles and scenarios, calculates
service-resilience profiles, simulates service-flow decline under disturbance,
flags threshold risk, and exports results using only the Python standard library.

Run:
    python3 python/ecosystem_services_resilience_standard.py
"""

from __future__ import annotations

import csv
import math
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
PROFILES_PATH = ROOT / "data" / "raw" / "ecosystem_service_profiles.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "service_disturbance_scenarios.csv"
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


def service_resilience_profile(row: dict[str, str]) -> float:
    return (
        0.10 * f(row, "current_service_flow")
        + 0.17 * f(row, "ecological_condition")
        + 0.15 * f(row, "functional_diversity")
        + 0.14 * f(row, "functional_redundancy")
        + 0.15 * f(row, "threshold_distance")
        + 0.12 * f(row, "governance_capacity")
        + 0.09 * f(row, "access_equity")
        + 0.12 * f(row, "ecological_memory")
        - 0.12 * f(row, "disturbance_exposure")
    )


def diagnostic(row: dict[str, str], profile: float) -> str:
    current_flow = f(row, "current_service_flow")
    threshold = f(row, "threshold_distance")
    access = f(row, "access_equity")

    if current_flow >= 0.70 and profile < 0.55:
        return "high current flow but weak resilience profile"
    if profile >= 0.60 and threshold >= 0.55:
        return "stronger service-resilience profile"
    if access < 0.50:
        return "equity and access concern"
    return "mixed service-resilience profile requiring monitoring"


def simulate_service(row: dict[str, str], scenario: dict[str, str], steps: int = 100) -> list[dict[str, object]]:
    condition = f(row, "ecological_condition")
    functional_capacity = f(row, "functional_diversity")
    redundancy = f(row, "functional_redundancy")
    memory = f(row, "ecological_memory")
    governance = f(row, "governance_capacity")
    exposure = f(row, "disturbance_exposure")
    access = f(row, "access_equity")

    disturbance_load = float(scenario["disturbance_load"])
    shock_intensity = float(scenario["shock_intensity"])
    shock_frequency = int(float(scenario["shock_frequency"]))
    governance_response = float(scenario["governance_response"])

    rows = []

    for t in range(1, steps + 1):
        seasonal_pressure = 0.04 + 0.020 * math.sin(t / 8.0)
        shock = shock_intensity if shock_frequency > 0 and t % shock_frequency == 0 else 0.0
        disturbance = disturbance_load + seasonal_pressure + shock + 0.16 * exposure

        repair = (
            0.010 * redundancy
            + 0.009 * memory
            + 0.007 * governance
            + 0.004 * governance_response
        )

        erosion = disturbance * (0.40 + exposure)

        condition = max(0.01, min(1.0, condition - 0.042 * erosion + repair))
        functional_capacity = max(0.01, min(1.0, functional_capacity - 0.028 * erosion + 0.006 * redundancy))

        service_flow = condition * functional_capacity * (1.0 - 0.33 * disturbance)
        service_flow = max(0.0, min(1.0, service_flow))

        resilience_margin = (
            condition
            + functional_capacity
            + redundancy
            + memory
            + governance
            + 0.35 * access
            - disturbance
            - exposure
        )

        rows.append(
            {
                "service_id": row["service_id"],
                "service": row["service"],
                "scenario_id": scenario["scenario_id"],
                "scenario_name": scenario["scenario_name"],
                "time_step": t,
                "disturbance": round(disturbance, 5),
                "ecosystem_condition": round(condition, 5),
                "functional_capacity": round(functional_capacity, 5),
                "service_flow": round(service_flow, 5),
                "resilience_margin": round(resilience_margin, 5),
                "threshold_flag": "threshold risk" if resilience_margin < 1.30 else "viable margin",
            }
        )

    return rows


def main() -> None:
    profiles = read_csv(PROFILES_PATH)
    scenarios = read_csv(SCENARIOS_PATH)

    profile_rows = []
    simulation_rows = []

    for row in profiles:
        profile = service_resilience_profile(row)
        profile_rows.append(
            {
                "service_id": row["service_id"],
                "service": row["service"],
                "service_category": row["service_category"],
                "ecosystem_type": row["ecosystem_type"],
                "critical_benefit": row["critical_benefit"],
                "current_service_flow": row["current_service_flow"],
                "service_resilience_profile": round(profile, 4),
                "service_resilience_gap": round(profile - f(row, "current_service_flow"), 4),
                "threshold_distance": row["threshold_distance"],
                "access_equity": row["access_equity"],
                "diagnostic": diagnostic(row, profile),
            }
        )

        for scenario in scenarios:
            simulation_rows.extend(simulate_service(row, scenario))

    summary_rows = []
    for row in profiles:
        sid = row["service_id"]
        subset = [r for r in simulation_rows if r["service_id"] == sid]
        summary_rows.append(
            {
                "service_id": sid,
                "service": row["service"],
                "minimum_service_flow": round(min(float(r["service_flow"]) for r in subset), 4),
                "final_service_flow": round(float(subset[-1]["service_flow"]), 4),
                "average_service_flow": round(mean(float(r["service_flow"]) for r in subset), 4),
                "minimum_resilience_margin": round(min(float(r["resilience_margin"]) for r in subset), 4),
                "threshold_risk_steps": sum(1 for r in subset if r["threshold_flag"] == "threshold risk"),
            }
        )

    write_csv(OUT_TABLES / "ecosystem_service_resilience_profiles_standard.csv", profile_rows)
    write_csv(OUT_TABLES / "ecosystem_service_disturbance_simulation_standard.csv", simulation_rows)
    write_csv(OUT_TABLES / "ecosystem_service_disturbance_summary_standard.csv", summary_rows)
    write_csv(DATA_PROCESSED / "ecosystem_service_resilience_profiles_standard.csv", profile_rows)

    print("Ecosystem-service resilience workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    for row in profile_rows:
        print(
            f"  {row['service']}: current_flow={row['current_service_flow']} "
            f"resilience={row['service_resilience_profile']} diagnostic={row['diagnostic']}"
        )


if __name__ == "__main__":
    main()
