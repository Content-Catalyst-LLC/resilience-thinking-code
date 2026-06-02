#!/usr/bin/env python3
"""
Dependency-light landscape resilience workflow.

Reads synthetic landscape profiles, patch tables, and disturbance-regime
scenarios. Calculates landscape resilience profiles, simulates disturbance
spread across patches, flags threshold risk, and exports outputs using only
the Python standard library.

Run:
    python3 python/landscape_resilience_standard.py
"""

from __future__ import annotations

import csv
import math
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
PROFILES_PATH = ROOT / "data" / "raw" / "landscape_resilience_profiles.csv"
PATCHES_PATH = ROOT / "data" / "raw" / "landscape_patch_table.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "disturbance_regime_scenarios.csv"
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


def landscape_resilience_profile(row: dict[str, str]) -> float:
    return (
        0.17 * f(row, "spatial_heterogeneity")
        + 0.15 * f(row, "viable_connectivity")
        + 0.17 * f(row, "refugia_capacity")
        + 0.17 * f(row, "ecological_memory")
        + 0.14 * f(row, "governance_capacity")
        - 0.11 * f(row, "disturbance_pressure")
        - 0.06 * f(row, "fragmentation")
        - 0.06 * f(row, "social_vulnerability")
    )


def disturbance_risk_index(row: dict[str, str]) -> float:
    return (
        0.28 * f(row, "disturbance_pressure")
        + 0.20 * f(row, "fragmentation")
        + 0.18 * f(row, "social_vulnerability")
        + 0.14 * (1.0 - f(row, "refugia_capacity"))
        + 0.10 * (1.0 - f(row, "ecological_memory"))
        + 0.10 * (1.0 - f(row, "governance_capacity"))
    )


def diagnostic(row: dict[str, str], profile: float, risk: float) -> str:
    if profile >= 0.55 and risk < 0.58:
        return "stronger landscape-resilience profile"
    if risk >= 0.68:
        return "high disturbance-regime risk"
    if f(row, "refugia_capacity") < 0.50 or f(row, "ecological_memory") < 0.50:
        return "refugia or ecological-memory concern"
    return "mixed landscape-resilience profile requiring monitoring"


def simulate_landscape(
    patches: list[dict[str, str]], scenario: dict[str, str], steps: int = 80
) -> list[dict[str, object]]:
    state = []
    for patch in patches:
        state.append(
            {
                "patch_id": patch["patch_id"],
                "landscape_id": patch["landscape_id"],
                "patch_type": patch["patch_type"],
                "condition": f(patch, "condition"),
                "exposure": f(patch, "exposure"),
                "buffer_capacity": f(patch, "buffer_capacity"),
                "ecological_memory": f(patch, "ecological_memory"),
                "recovery_capacity": f(patch, "recovery_capacity"),
                "refugia": int(float(patch["refugia"])),
                "connectivity_weight": f(patch, "connectivity_weight"),
                "social_exposure": f(patch, "social_exposure"),
                "disturbance": 0.08 + 0.10 * f(patch, "exposure"),
            }
        )

    disturbance_load = float(scenario["disturbance_load"])
    spread_amplifier = float(scenario["spread_amplifier"])
    climate_pressure = float(scenario["climate_pressure"])
    governance_response = float(scenario["governance_response"])

    rows = []

    for t in range(1, steps + 1):
        previous_disturbance = [p["disturbance"] for p in state]
        mean_disturbance = mean(previous_disturbance)
        shock = 0.24 if t in (18, 36, 55, 70) else 0.0
        seasonal = 0.04 + 0.025 * math.sin(t / 7.0)

        for idx, patch in enumerate(state):
            left = previous_disturbance[idx - 1] if idx > 0 else previous_disturbance[-1]
            right = previous_disturbance[(idx + 1) % len(previous_disturbance)]
            local_spread = 0.50 * (left + right) * patch["connectivity_weight"]

            incoming = (
                spread_amplifier * local_spread
                + 0.10 * spread_amplifier * mean_disturbance
            )

            disturbance = (
                previous_disturbance[idx]
                + disturbance_load
                + seasonal
                + shock
                + 0.18 * climate_pressure
                + 0.22 * patch["exposure"]
                + incoming
                - 0.26 * patch["buffer_capacity"]
                - 0.12 * patch["refugia"]
                - 0.06 * governance_response
            )
            disturbance = max(0.0, min(1.40, disturbance))

            condition = (
                patch["condition"]
                - 0.055 * disturbance
                + 0.018 * patch["ecological_memory"]
                + 0.015 * patch["recovery_capacity"]
                + 0.008 * patch["refugia"]
                + 0.006 * governance_response
            )
            condition = max(0.0, min(1.0, condition))
            patch["condition"] = condition
            patch["disturbance"] = disturbance

            resilience_margin = (
                condition
                + patch["buffer_capacity"]
                + patch["ecological_memory"]
                + patch["recovery_capacity"]
                + 0.25 * patch["refugia"]
                + 0.20 * governance_response
                - disturbance
                - patch["exposure"]
                - 0.30 * patch["social_exposure"]
            )

            rows.append(
                {
                    "scenario_id": scenario["scenario_id"],
                    "scenario_name": scenario["scenario_name"],
                    "time_step": t,
                    "patch_id": patch["patch_id"],
                    "landscape_id": patch["landscape_id"],
                    "patch_type": patch["patch_type"],
                    "condition": round(condition, 5),
                    "disturbance": round(disturbance, 5),
                    "resilience_margin": round(resilience_margin, 5),
                    "refugia": patch["refugia"],
                    "threshold_flag": "threshold risk" if resilience_margin < 0.75 else "viable margin",
                }
            )

    return rows


def main() -> None:
    profiles = read_csv(PROFILES_PATH)
    patches = read_csv(PATCHES_PATH)
    scenarios = read_csv(SCENARIOS_PATH)

    profile_rows = []
    for row in profiles:
        profile = landscape_resilience_profile(row)
        risk = disturbance_risk_index(row)
        profile_rows.append(
            {
                "landscape_id": row["landscape_id"],
                "landscape_type": row["landscape_type"],
                "dominant_disturbance": row["dominant_disturbance"],
                "critical_function": row["critical_function"],
                "landscape_resilience_profile": round(profile, 4),
                "disturbance_risk_index": round(risk, 4),
                "diagnostic": diagnostic(row, profile, risk),
            }
        )

    simulation_rows = []
    for scenario in scenarios:
        simulation_rows.extend(simulate_landscape(patches, scenario))

    summary_rows = []
    for scenario in scenarios:
        sid = scenario["scenario_id"]
        subset = [r for r in simulation_rows if r["scenario_id"] == sid]
        summary_rows.append(
            {
                "scenario_id": sid,
                "scenario_name": scenario["scenario_name"],
                "minimum_mean_condition": round(
                    min(
                        mean(float(r["condition"]) for r in subset if int(r["time_step"]) == t)
                        for t in sorted({int(r["time_step"]) for r in subset})
                    ),
                    4,
                ),
                "maximum_mean_disturbance": round(
                    max(
                        mean(float(r["disturbance"]) for r in subset if int(r["time_step"]) == t)
                        for t in sorted({int(r["time_step"]) for r in subset})
                    ),
                    4,
                ),
                "minimum_mean_resilience_margin": round(
                    min(
                        mean(float(r["resilience_margin"]) for r in subset if int(r["time_step"]) == t)
                        for t in sorted({int(r["time_step"]) for r in subset})
                    ),
                    4,
                ),
                "threshold_risk_patch_steps": sum(1 for r in subset if r["threshold_flag"] == "threshold risk"),
            }
        )

    write_csv(OUT_TABLES / "landscape_resilience_profiles_standard.csv", profile_rows)
    write_csv(OUT_TABLES / "landscape_disturbance_patch_simulation_standard.csv", simulation_rows)
    write_csv(OUT_TABLES / "landscape_disturbance_summary_standard.csv", summary_rows)
    write_csv(DATA_PROCESSED / "landscape_resilience_profiles_standard.csv", profile_rows)

    print("Landscape resilience workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    for row in profile_rows:
        print(
            f"  {row['landscape_type']}: profile={row['landscape_resilience_profile']} "
            f"risk={row['disturbance_risk_index']} diagnostic={row['diagnostic']}"
        )


if __name__ == "__main__":
    main()
