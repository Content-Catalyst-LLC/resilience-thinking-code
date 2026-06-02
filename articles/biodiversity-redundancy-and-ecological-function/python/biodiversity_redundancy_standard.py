#!/usr/bin/env python3
"""
Dependency-light biodiversity, redundancy, and ecological-function workflow.

This script reads synthetic function and species-trait tables, calculates
functional resilience profiles, simulates ecological function loss under
disturbance, flags threshold risk, and exports results using only the Python
standard library.

Run:
    python3 python/biodiversity_redundancy_standard.py
"""

from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean, variance


ROOT = Path(__file__).resolve().parents[1]
FUNCTIONS_PATH = ROOT / "data" / "raw" / "ecological_function_profiles.csv"
TRAITS_PATH = ROOT / "data" / "raw" / "species_trait_table.csv"
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


def functional_resilience_profile(row: dict[str, str]) -> float:
    return (
        0.12 * f(row, "species_richness")
        + 0.19 * f(row, "functional_diversity")
        + 0.17 * f(row, "functional_redundancy")
        + 0.20 * f(row, "response_diversity")
        + 0.13 * f(row, "connectivity")
        + 0.16 * f(row, "ecological_memory")
        - 0.12 * f(row, "disturbance_exposure")
    )


def profile_diagnostic(row: dict[str, str], profile: float) -> str:
    if profile >= 0.58 and f(row, "response_diversity") >= 0.55:
        return "stronger function-resilience profile"
    if f(row, "functional_redundancy") < 0.50 or f(row, "response_diversity") < 0.50:
        return "redundancy or response-diversity concern"
    if f(row, "disturbance_exposure") >= 0.70:
        return "high disturbance exposure"
    return "mixed profile requiring monitoring"


def simulate_function_loss(traits: list[dict[str, str]], scenario: dict[str, str], steps: int = 100) -> list[dict[str, object]]:
    species = []
    for row in traits:
        species.append(
            {
                "species_id": row["species_id"],
                "species_name": row["species_name"],
                "functional_group": row["functional_group"],
                "trait_contribution": f(row, "trait_contribution"),
                "disturbance_sensitivity": f(row, "disturbance_sensitivity"),
                "recovery_capacity": f(row, "recovery_capacity"),
                "abundance": f(row, "initial_abundance"),
            }
        )

    disturbance_pressure = float(scenario["disturbance_pressure"])
    shock_intensity = float(scenario["shock_intensity"])
    shock_frequency = int(float(scenario["shock_frequency"]))
    recovery_support = float(scenario["recovery_support"])

    rows = []

    for t in range(1, steps + 1):
        seasonal = 0.055 + 0.025 * math.sin(t / 9.0)
        shock = shock_intensity if shock_frequency > 0 and t % shock_frequency == 0 else 0.0
        disturbance = disturbance_pressure + seasonal + shock

        grouped = defaultdict(list)

        for sp in species:
            mortality_pressure = disturbance * sp["disturbance_sensitivity"]
            recovery = 0.020 * sp["recovery_capacity"] + 0.006 * recovery_support
            sp["abundance"] = max(0.0, min(1.2, sp["abundance"] - mortality_pressure * 0.085 + recovery))
            sp["functional_output"] = sp["abundance"] * sp["trait_contribution"]
            grouped[sp["functional_group"]].append(sp)

        for group, members in grouped.items():
            present = [m for m in members if m["abundance"] > 0.10]
            sensitivities = [m["disturbance_sensitivity"] for m in members]
            response_var = variance(sensitivities) if len(sensitivities) > 1 else 0.0
            functional_output = sum(m["functional_output"] for m in members)
            redundancy = len(present)
            mean_abundance = mean(m["abundance"] for m in members)

            resilience_margin = functional_output + 0.055 * redundancy + response_var - disturbance

            rows.append(
                {
                    "scenario_id": scenario["scenario_id"],
                    "scenario_name": scenario["scenario_name"],
                    "time_step": t,
                    "functional_group": group,
                    "disturbance": round(disturbance, 5),
                    "species_present": redundancy,
                    "mean_abundance": round(mean_abundance, 5),
                    "functional_output": round(functional_output, 5),
                    "response_diversity": round(response_var, 5),
                    "resilience_margin": round(resilience_margin, 5),
                    "threshold_flag": "threshold risk" if resilience_margin < 1.20 else "viable margin",
                }
            )

    return rows


def main() -> None:
    functions = read_csv(FUNCTIONS_PATH)
    traits = read_csv(TRAITS_PATH)
    scenarios = read_csv(SCENARIOS_PATH)

    profile_rows = []
    for row in functions:
        profile = functional_resilience_profile(row)
        profile_rows.append(
            {
                "function_id": row["function_id"],
                "ecosystem_function": row["ecosystem_function"],
                "critical_role": row["critical_role"],
                "species_richness": row["species_richness"],
                "functional_diversity": row["functional_diversity"],
                "functional_redundancy": row["functional_redundancy"],
                "response_diversity": row["response_diversity"],
                "functional_resilience_profile": round(profile, 4),
                "diagnostic": profile_diagnostic(row, profile),
            }
        )

    simulation_rows = []
    for scenario in scenarios:
        simulation_rows.extend(simulate_function_loss(traits, scenario))

    summary_rows = []
    groups = sorted({r["functional_group"] for r in simulation_rows})
    scenarios_seen = sorted({r["scenario_id"] for r in simulation_rows})

    for sid in scenarios_seen:
        for group in groups:
            subset = [r for r in simulation_rows if r["scenario_id"] == sid and r["functional_group"] == group]
            if not subset:
                continue
            summary_rows.append(
                {
                    "scenario_id": sid,
                    "functional_group": group,
                    "minimum_functional_output": round(min(float(r["functional_output"]) for r in subset), 4),
                    "final_functional_output": round(float(subset[-1]["functional_output"]), 4),
                    "minimum_species_present": min(int(r["species_present"]) for r in subset),
                    "minimum_resilience_margin": round(min(float(r["resilience_margin"]) for r in subset), 4),
                    "threshold_risk_steps": sum(1 for r in subset if r["threshold_flag"] == "threshold risk"),
                }
            )

    write_csv(OUT_TABLES / "functional_diversity_redundancy_profiles_standard.csv", profile_rows)
    write_csv(OUT_TABLES / "function_loss_simulation_standard.csv", simulation_rows)
    write_csv(OUT_TABLES / "function_loss_summary_standard.csv", summary_rows)
    write_csv(DATA_PROCESSED / "functional_diversity_redundancy_profiles_standard.csv", profile_rows)

    print("Biodiversity redundancy workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    for row in profile_rows:
        print(
            f"  {row['ecosystem_function']}: profile={row['functional_resilience_profile']} "
            f"diagnostic={row['diagnostic']}"
        )


if __name__ == "__main__":
    main()
