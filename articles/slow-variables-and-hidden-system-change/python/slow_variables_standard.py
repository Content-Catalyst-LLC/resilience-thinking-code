#!/usr/bin/env python3
"""
Dependency-light slow-variable and hidden-system-change workflow.

Reads synthetic slow-variable profiles and scenarios, calculates hidden-risk
profiles, simulates threshold distance and fast-shock interaction, and exports
outputs using only the Python standard library.

Run:
    python3 python/slow_variables_standard.py
"""

from __future__ import annotations

import csv
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
PROFILES_PATH = ROOT / "data" / "raw" / "slow_variable_profiles.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "slow_variable_scenarios.csv"
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


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def hidden_risk_score(row: dict[str, str]) -> float:
    return clamp(
        0.20 * f(row, "maintenance_backlog")
        + 0.18 * f(row, "climate_pressure")
        + 0.16 * f(row, "exposure")
        + 0.12 * (1.0 - f(row, "public_trust"))
        + 0.12 * (1.0 - f(row, "ecological_memory"))
        + 0.10 * (1.0 - f(row, "adaptive_capacity"))
        + 0.07 * (1.0 - f(row, "monitoring_quality"))
        + 0.05 * (1.0 - f(row, "justice_visibility"))
    )


def threshold_distance(row: dict[str, str]) -> float:
    return clamp(
        1.0
        - 0.26 * f(row, "maintenance_backlog")
        - 0.24 * f(row, "climate_pressure")
        - 0.16 * f(row, "exposure")
        - 0.12 * (1.0 - f(row, "public_trust"))
        - 0.12 * (1.0 - f(row, "ecological_memory"))
        - 0.10 * (1.0 - f(row, "adaptive_capacity"))
    )


def diagnostic(row: dict[str, str], risk: float, distance: float) -> str:
    if risk >= 0.58 and distance <= 0.45:
        return "high hidden-risk and narrowing threshold-distance concern"
    if f(row, "monitoring_quality") < 0.50:
        return "monitoring and signal-quality concern"
    if f(row, "justice_visibility") < 0.45:
        return "justice visibility and slow-harm concern"
    if f(row, "adaptive_capacity") < 0.48:
        return "adaptive-capacity concern"
    return "mixed slow-variable profile requiring monitoring"


def simulate_scenario(scenario: dict[str, str], steps: int = 120) -> list[dict[str, object]]:
    maintenance_backlog = 0.25
    public_trust = 0.72
    ecological_memory = 0.68
    climate_pressure = 0.22
    system_memory = 0.60
    monitoring_quality = 0.54
    justice_visibility = 0.48
    system_function = 0.86

    rows = []

    for t in range(1, steps + 1):
        adaptive_investment = float(scenario["adaptive_investment"])
        monitoring_improvement = float(scenario["monitoring_improvement"])
        justice_improvement = float(scenario["justice_improvement"])

        maintenance_backlog = clamp(
            maintenance_backlog
            + float(scenario["maintenance_growth"])
            - 0.006 * adaptive_investment
        )
        public_trust = clamp(
            public_trust
            - float(scenario["trust_decline"])
            + 0.007 * adaptive_investment
        )
        ecological_memory = clamp(
            ecological_memory
            - float(scenario["memory_decline"])
            + 0.005 * adaptive_investment
        )
        climate_pressure = clamp(
            climate_pressure
            + float(scenario["climate_growth"])
        )
        monitoring_quality = clamp(
            monitoring_quality + monitoring_improvement + 0.002 * adaptive_investment
        )
        justice_visibility = clamp(
            justice_visibility + justice_improvement + 0.0015 * adaptive_investment
        )
        system_memory = clamp(
            system_memory
            + 0.004 * monitoring_quality
            + 0.003 * public_trust
            - 0.002 * climate_pressure
        )

        adaptive_capacity = clamp(
            0.26 * public_trust
            + 0.22 * ecological_memory
            + 0.18 * (1.0 - maintenance_backlog)
            + 0.14 * (1.0 - climate_pressure)
            + 0.10 * system_memory
            + 0.06 * monitoring_quality
            + 0.04 * justice_visibility
        )

        distance = clamp(
            1.0
            - 0.30 * maintenance_backlog
            - 0.26 * climate_pressure
            - 0.18 * (1.0 - public_trust)
            - 0.16 * (1.0 - ecological_memory)
            - 0.10 * (1.0 - adaptive_capacity)
        )

        hidden_risk = clamp(
            0.28 * maintenance_backlog
            + 0.26 * climate_pressure
            + 0.18 * (1.0 - public_trust)
            + 0.14 * (1.0 - ecological_memory)
            + 0.08 * (1.0 - monitoring_quality)
            + 0.06 * (1.0 - justice_visibility)
        )

        fast_shock = (
            float(scenario["shock_magnitude"])
            if t in [int(float(scenario["shock_time_1"])), int(float(scenario["shock_time_2"]))]
            else 0.0
        )

        system_function = clamp(
            system_function
            - 0.22 * hidden_risk
            - 0.46 * fast_shock
            + 0.18 * adaptive_capacity
            + 0.04 * system_memory
        )

        rows.append(
            {
                "scenario_id": scenario["scenario_id"],
                "scenario_name": scenario["scenario_name"],
                "time_step": t,
                "maintenance_backlog": round(maintenance_backlog, 5),
                "public_trust": round(public_trust, 5),
                "ecological_memory": round(ecological_memory, 5),
                "climate_pressure": round(climate_pressure, 5),
                "system_memory": round(system_memory, 5),
                "monitoring_quality": round(monitoring_quality, 5),
                "justice_visibility": round(justice_visibility, 5),
                "adaptive_capacity": round(adaptive_capacity, 5),
                "threshold_distance": round(distance, 5),
                "hidden_risk": round(hidden_risk, 5),
                "fast_shock": round(fast_shock, 5),
                "system_function": round(system_function, 5),
            }
        )

    return rows


def main() -> None:
    profiles = read_csv(PROFILES_PATH)
    scenarios = read_csv(SCENARIOS_PATH)

    profile_rows = []
    for row in profiles:
        risk = hidden_risk_score(row)
        distance = threshold_distance(row)
        profile_rows.append(
            {
                "system_id": row["system_id"],
                "system_name": row["system_name"],
                "system_type": row["system_type"],
                "critical_function": row["critical_function"],
                "hidden_risk_score": round(risk, 5),
                "threshold_distance": round(distance, 5),
                "maintenance_backlog": row["maintenance_backlog"],
                "public_trust": row["public_trust"],
                "ecological_memory": row["ecological_memory"],
                "climate_pressure": row["climate_pressure"],
                "adaptive_capacity": row["adaptive_capacity"],
                "system_memory": row["system_memory"],
                "monitoring_quality": row["monitoring_quality"],
                "justice_visibility": row["justice_visibility"],
                "exposure": row["exposure"],
                "diagnostic": diagnostic(row, risk, distance),
            }
        )

    simulation_rows = []
    for scenario in scenarios:
        simulation_rows.extend(simulate_scenario(scenario))

    summary_rows = []
    for sid in sorted({r["scenario_id"] for r in simulation_rows}):
        subset = [r for r in simulation_rows if r["scenario_id"] == sid]
        summary_rows.append(
            {
                "scenario_id": sid,
                "scenario_name": subset[0]["scenario_name"],
                "final_system_function": subset[-1]["system_function"],
                "minimum_threshold_distance": round(min(float(r["threshold_distance"]) for r in subset), 5),
                "maximum_hidden_risk": round(max(float(r["hidden_risk"]) for r in subset), 5),
                "final_adaptive_capacity": subset[-1]["adaptive_capacity"],
                "shock_count": sum(1 for r in subset if float(r["fast_shock"]) > 0),
            }
        )

    write_csv(OUT_TABLES / "slow_variable_profiles_standard.csv", profile_rows)
    write_csv(OUT_TABLES / "slow_variables_hidden_change_simulation_standard.csv", simulation_rows)
    write_csv(OUT_TABLES / "slow_variables_scenario_summary_standard.csv", summary_rows)
    write_csv(DATA_PROCESSED / "slow_variable_profiles_standard.csv", profile_rows)

    print("Slow variables workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    for row in profile_rows:
        print(
            f"  {row['system_name']}: risk={row['hidden_risk_score']} "
            f"threshold_distance={row['threshold_distance']} diagnostic={row['diagnostic']}"
        )


if __name__ == "__main__":
    main()
