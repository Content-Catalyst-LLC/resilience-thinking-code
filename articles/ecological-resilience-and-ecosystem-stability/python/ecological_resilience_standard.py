#!/usr/bin/env python3
"""
Dependency-light ecological resilience workflow.

Run:
    python3 python/ecological_resilience_standard.py
"""

from __future__ import annotations

import csv
import math
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
PROFILES_PATH = ROOT / "data" / "raw" / "ecosystem_resilience_profiles.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "disturbance_scenarios.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_TABLES.mkdir(parents=True, exist_ok=True)


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


def resilience_profile(row: dict[str, str]) -> float:
    return (
        0.11 * f(row, "short_run_stability")
        + 0.13 * f(row, "biodiversity")
        + 0.13 * f(row, "functional_diversity")
        + 0.13 * f(row, "response_diversity")
        + 0.16 * f(row, "threshold_distance")
        + 0.14 * f(row, "basin_width")
        + 0.12 * f(row, "regenerative_capacity")
        + 0.10 * f(row, "ecological_memory")
        + 0.08 * f(row, "connectivity")
        - 0.06 * f(row, "disturbance_exposure")
        - 0.06 * f(row, "slow_variable_pressure")
    )


def diagnostic(row: dict[str, str], resilience: float) -> str:
    stability = f(row, "short_run_stability")
    threshold = f(row, "threshold_distance")
    if stability >= 0.70 and resilience < 0.55:
        return "appears stable but ecological resilience profile is weak"
    if resilience >= 0.62 and threshold >= 0.55:
        return "stronger ecological resilience profile"
    if threshold < 0.40:
        return "threshold-distance concern requiring close monitoring"
    return "mixed resilience profile requiring monitoring"


def simulate_margin(row: dict[str, str], scenario: dict[str, str], steps: int = 96) -> list[dict[str, object]]:
    margin = f(row, "basin_width") + 0.50 * f(row, "threshold_distance") + 0.30 * f(row, "regenerative_capacity")
    rows = []

    disturbance_load = float(scenario["disturbance_load"])
    external_pressure = float(scenario["external_pressure"])
    shock_frequency = int(float(scenario["shock_frequency"]))
    regenerative_support = float(scenario["regenerative_support"])

    for t in range(1, steps + 1):
        seasonal = 0.04 + 0.025 * math.sin(t / 7.0)
        shock = external_pressure if shock_frequency > 0 and t % shock_frequency == 0 else 0.0
        disturbance = disturbance_load + seasonal + shock

        recovery = (
            0.010 * f(row, "regenerative_capacity")
            + 0.008 * f(row, "ecological_memory")
            + 0.006 * f(row, "connectivity")
            + 0.006 * regenerative_support
        )
        erosion = (
            disturbance * (0.35 + f(row, "disturbance_exposure"))
            + 0.020 * f(row, "slow_variable_pressure")
        )

        margin = max(-1.0, min(2.0, margin - 0.055 * erosion + recovery))

        rows.append(
            {
                "ecosystem_id": row["ecosystem_id"],
                "ecosystem_type": row["ecosystem_type"],
                "scenario_id": scenario["scenario_id"],
                "scenario_name": scenario["scenario_name"],
                "time_step": t,
                "disturbance": round(disturbance, 4),
                "ecological_resilience_margin": round(margin, 4),
                "threshold_flag": "threshold risk" if margin < 0.25 else "viable margin",
            }
        )

    return rows


def simulate_regime_shift(steps: int = 140) -> list[dict[str, object]]:
    x = -0.9
    r = 1.1
    dt = 0.05
    rows = []

    for t in range(1, steps + 1):
        pressure = -0.6 + 1.45 * (t - 1) / (steps - 1)
        if t > 1:
            x = x + dt * (r * x - x**3 + pressure)

        basin_width = 0.85 - 0.47 * (t - 1) / (steps - 1)
        disturbance_load = 0.10 + 0.68 * (t - 1) / (steps - 1)
        regenerative_capacity = 0.36 + 0.18 * math.sin(t / 18.0)
        margin = basin_width - disturbance_load + regenerative_capacity

        rows.append(
            {
                "time_step": t,
                "external_pressure": round(pressure, 5),
                "ecosystem_state": round(x, 5),
                "basin_width": round(basin_width, 5),
                "disturbance_load": round(disturbance_load, 5),
                "regenerative_capacity": round(regenerative_capacity, 5),
                "resilience_margin": round(margin, 5),
                "threshold_flag": "threshold risk" if margin < 0.15 else "viable margin",
            }
        )

    return rows


def main() -> None:
    profiles = read_csv(PROFILES_PATH)
    scenarios = read_csv(SCENARIOS_PATH)

    profile_rows = []
    simulation_rows = []

    for row in profiles:
        stability = f(row, "short_run_stability")
        resilience = resilience_profile(row)

        profile_rows.append(
            {
                "ecosystem_id": row["ecosystem_id"],
                "ecosystem_type": row["ecosystem_type"],
                "critical_function": row["critical_function"],
                "stability_score": round(stability, 4),
                "ecological_resilience_profile": round(resilience, 4),
                "stability_resilience_gap": round(resilience - stability, 4),
                "threshold_distance": row["threshold_distance"],
                "diagnostic": diagnostic(row, resilience),
            }
        )

        for scenario in scenarios:
            simulation_rows.extend(simulate_margin(row, scenario))

    summary_rows = []
    for row in profiles:
        eid = row["ecosystem_id"]
        subset = [r for r in simulation_rows if r["ecosystem_id"] == eid]
        summary_rows.append(
            {
                "ecosystem_id": eid,
                "ecosystem_type": row["ecosystem_type"],
                "minimum_margin": round(min(float(r["ecological_resilience_margin"]) for r in subset), 4),
                "average_margin": round(mean(float(r["ecological_resilience_margin"]) for r in subset), 4),
                "threshold_risk_steps": sum(1 for r in subset if r["threshold_flag"] == "threshold risk"),
            }
        )

    write_csv(OUT_TABLES / "ecosystem_resilience_profiles_standard.csv", profile_rows)
    write_csv(OUT_TABLES / "ecosystem_resilience_margin_simulation_standard.csv", simulation_rows)
    write_csv(OUT_TABLES / "ecosystem_resilience_summary_standard.csv", summary_rows)
    write_csv(OUT_TABLES / "ecological_regime_shift_simulation_standard.csv", simulate_regime_shift())

    print("Ecological resilience workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    for row in profile_rows:
        print(f"  {row['ecosystem_type']}: stability={row['stability_score']} resilience={row['ecological_resilience_profile']}")


if __name__ == "__main__":
    main()
