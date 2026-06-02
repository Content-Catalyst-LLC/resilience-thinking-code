#!/usr/bin/env python3
"""
Dependency-light social-ecological systems workflow.

This script reads synthetic SES profiles and scenarios, calculates SES resilience
profiles and coupled vulnerability, simulates ecological condition and social
pressure over time, flags threshold risk, and exports results using only the
Python standard library.

Run:
    python3 python/social_ecological_systems_standard.py
"""

from __future__ import annotations

import csv
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
PROFILES_PATH = ROOT / "data" / "raw" / "social_ecological_system_profiles.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "coupled_scenarios.csv"
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


def ses_resilience_profile(row: dict[str, str]) -> float:
    return (
        0.18 * f(row, "ecological_condition")
        + 0.16 * f(row, "governance_quality")
        + 0.12 * f(row, "livelihood_diversity")
        + 0.12 * f(row, "infrastructure_support")
        + 0.13 * f(row, "knowledge_integration")
        + 0.11 * f(row, "social_trust")
        + 0.10 * f(row, "adaptive_capacity")
        - 0.09 * f(row, "market_pressure")
        - 0.07 * f(row, "climate_exposure")
        - 0.02 * f(row, "resource_dependency")
    )


def coupled_vulnerability(row: dict[str, str]) -> float:
    return (
        0.26 * f(row, "market_pressure")
        + 0.25 * f(row, "climate_exposure")
        + 0.18 * f(row, "resource_dependency")
        + 0.15 * (1.0 - f(row, "governance_quality"))
        + 0.10 * (1.0 - f(row, "livelihood_diversity"))
        + 0.06 * (1.0 - f(row, "social_trust"))
    )


def diagnostic(profile: float, vulnerability: float, governance: float) -> str:
    if profile >= 0.52 and vulnerability < 0.55:
        return "stronger SES resilience profile"
    if vulnerability >= 0.66:
        return "high coupled vulnerability"
    if governance < 0.58:
        return "governance capacity concern"
    return "mixed SES resilience profile"


def simulate_ses(scenario: dict[str, str], steps: int = 90) -> list[dict[str, object]]:
    ecology = f(scenario, "initial_ecology")
    social_pressure = f(scenario, "initial_social_pressure")
    governance = f(scenario, "governance_effectiveness")
    livelihood_pressure = f(scenario, "livelihood_pressure")
    climate_pressure = f(scenario, "climate_pressure")
    market_shock = f(scenario, "market_shock")

    r = 0.08
    k = 1.0
    q = 0.10

    rows = []

    for t in range(1, steps + 1):
        extraction = q * social_pressure * ecology
        ecological_growth = r * ecology * (1.0 - ecology / k)
        climate_effect = 0.022 * climate_pressure
        governance_repair = 0.017 * governance

        ecology = ecology + ecological_growth - extraction - climate_effect + governance_repair
        ecology = max(0.01, min(1.20, ecology))

        market_pulse = 0.035 * market_shock if t in (20, 42, 68) else 0.0
        social_pressure = (
            social_pressure
            + 0.050 * livelihood_pressure
            + 0.028 * (1.0 - governance)
            + market_pulse
            - 0.043 * ecology
        )
        social_pressure = max(0.05, min(1.20, social_pressure))

        resilience_margin = ecology + governance + 0.35 * (1.0 - livelihood_pressure) - social_pressure - 0.35 * climate_pressure

        rows.append(
            {
                "scenario_id": scenario["scenario_id"],
                "scenario_name": scenario["scenario_name"],
                "time_step": t,
                "ecology": round(ecology, 5),
                "social_pressure": round(social_pressure, 5),
                "extraction": round(extraction, 5),
                "resilience_margin": round(resilience_margin, 5),
                "threshold_flag": "threshold risk" if resilience_margin < 0.20 else "viable margin",
            }
        )

    return rows


def main() -> None:
    profiles = read_csv(PROFILES_PATH)
    scenarios = read_csv(SCENARIOS_PATH)

    profile_rows = []
    for row in profiles:
        profile = ses_resilience_profile(row)
        vulnerability = coupled_vulnerability(row)
        profile_rows.append(
            {
                "system_id": row["system_id"],
                "system_type": row["system_type"],
                "critical_function": row["critical_function"],
                "ses_resilience_profile": round(profile, 4),
                "coupled_vulnerability": round(vulnerability, 4),
                "governance_quality": row["governance_quality"],
                "ecological_condition": row["ecological_condition"],
                "diagnostic": diagnostic(profile, vulnerability, f(row, "governance_quality")),
            }
        )

    simulation_rows = []
    for scenario in scenarios:
        simulation_rows.extend(simulate_ses(scenario))

    summary_rows = []
    for scenario in scenarios:
        sid = scenario["scenario_id"]
        subset = [r for r in simulation_rows if r["scenario_id"] == sid]
        summary_rows.append(
            {
                "scenario_id": sid,
                "scenario_name": scenario["scenario_name"],
                "minimum_ecology": round(min(float(r["ecology"]) for r in subset), 4),
                "final_ecology": round(float(subset[-1]["ecology"]), 4),
                "maximum_social_pressure": round(max(float(r["social_pressure"]) for r in subset), 4),
                "minimum_resilience_margin": round(min(float(r["resilience_margin"]) for r in subset), 4),
                "threshold_risk_steps": sum(1 for r in subset if r["threshold_flag"] == "threshold risk"),
            }
        )

    write_csv(OUT_TABLES / "social_ecological_system_profiles_standard.csv", profile_rows)
    write_csv(OUT_TABLES / "social_ecological_coupled_simulation_standard.csv", simulation_rows)
    write_csv(OUT_TABLES / "social_ecological_simulation_summary_standard.csv", summary_rows)
    write_csv(DATA_PROCESSED / "social_ecological_system_profiles_standard.csv", profile_rows)

    print("Social-ecological systems workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    for row in profile_rows:
        print(
            f"  {row['system_type']}: profile={row['ses_resilience_profile']} "
            f"vulnerability={row['coupled_vulnerability']} diagnostic={row['diagnostic']}"
        )


if __name__ == "__main__":
    main()
