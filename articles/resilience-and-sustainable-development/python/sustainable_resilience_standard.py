#!/usr/bin/env python3
# Dependency-light sustainable resilience workflow.
# Run: python3 python/sustainable_resilience_standard.py

from __future__ import annotations

import csv
import random
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parents[1]
OUT_TABLES = ROOT / "outputs" / "tables"
DATA_PROCESSED = ROOT / "data" / "processed"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

BENEFIT_CRITERIA = [
    "resilience",
    "ecological_integrity",
    "social_inclusion",
    "economic_sufficiency",
    "governance_capacity",
    "adaptive_capacity",
]
PENALTY_CRITERIA = ["resource_pressure", "implementation_burden"]

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

def viability_value(row: dict[str, str]) -> float:
    return (
        0.18 * f(row, "resilience")
        + 0.17 * f(row, "ecological_integrity")
        + 0.16 * f(row, "social_inclusion")
        + 0.14 * f(row, "economic_sufficiency")
        + 0.14 * f(row, "governance_capacity")
        + 0.15 * f(row, "adaptive_capacity")
        - 0.04 * f(row, "resource_pressure")
        - 0.02 * f(row, "implementation_burden")
    )

def boundary_adjusted_value(row: dict[str, str], value: float) -> float:
    resource_penalty = max(0.0, f(row, "resource_pressure") - 3.8) * 0.20
    equity_penalty = max(0.0, 8.2 - f(row, "social_inclusion")) * 0.12
    ecology_penalty = max(0.0, 8.2 - f(row, "ecological_integrity")) * 0.12
    return value - resource_penalty - equity_penalty - ecology_penalty

def score_pathway(row: dict[str, str], scenario: dict[str, str]) -> float:
    return (
        f(scenario, "resilience_weight") * f(row, "resilience")
        + f(scenario, "ecological_integrity_weight") * f(row, "ecological_integrity")
        + f(scenario, "social_inclusion_weight") * f(row, "social_inclusion")
        + f(scenario, "economic_sufficiency_weight") * f(row, "economic_sufficiency")
        + f(scenario, "governance_capacity_weight") * f(row, "governance_capacity")
        + f(scenario, "adaptive_capacity_weight") * f(row, "adaptive_capacity")
        - f(scenario, "resource_pressure_weight") * f(row, "resource_pressure")
        - f(scenario, "implementation_burden_weight") * f(row, "implementation_burden")
    )

def pathway_diagnostic(row: dict[str, str], value: float) -> str:
    if f(row, "resource_pressure") >= 4.2:
        return "resource-pressure review needed"
    if f(row, "social_inclusion") < 8.0:
        return "social-inclusion safeguards need strengthening"
    if f(row, "ecological_integrity") < 8.0:
        return "ecological-integrity safeguards need strengthening"
    if f(row, "governance_capacity") < 8.0:
        return "governance-capacity review needed"
    if f(row, "implementation_burden") >= 3.6:
        return "implementation-burden review needed"
    if value >= 8.0:
        return "strong sustainable resilience pathway candidate"
    return "promising but requires scenario validation"

def scenario_rankings(pathways, scenarios):
    rows = []
    for scenario in scenarios:
        scored = sorted(
            [(score_pathway(pathway, scenario), pathway) for pathway in pathways],
            key=lambda item: item[0],
            reverse=True,
        )
        for rank, (value, pathway) in enumerate(scored, start=1):
            rows.append({
                "scenario": scenario["scenario"],
                "pathway_id": pathway["pathway_id"],
                "pathway": pathway["pathway"],
                "system_domain": pathway["system_domain"],
                "rank": rank,
                "viability_value": round(value, 5),
                "resource_pressure": pathway["resource_pressure"],
                "implementation_burden": pathway["implementation_burden"],
                "critical_function": pathway["critical_function"],
            })
    return rows

def simulate_development_response(system, events, seed, time_steps=80):
    rng = random.Random(seed)
    development_quality = f(system, "baseline_development_quality")
    adaptive = f(system, "adaptive_capacity")
    equity_sensitivity = f(system, "equity_sensitivity")
    resource_pressure = f(system, "resource_pressure")
    governance_constraint = f(system, "governance_constraint")
    rows = []

    event_by_step = {12: events[0], 27: events[1], 42: events[2], 56: events[3], 70: events[4]}

    for t in range(time_steps):
        event = event_by_step.get(t)
        if event:
            shock = f(event, "shock_intensity")
            climate = f(event, "climate_stress")
            overshoot = f(event, "ecological_overshoot")
            economic = f(event, "economic_shock")
            infrastructure = f(event, "infrastructure_disruption")
            governance = f(event, "governance_stress")
            equity_burden = f(event, "equity_burden")
            pressure_spike = f(event, "resource_pressure_spike")
            event_name = event["event_name"]
        else:
            shock = 0.05 + rng.random() * 0.02
            climate = 0.10 + rng.random() * 0.03
            overshoot = 0.11 + 0.0015 * t
            economic = 0.10
            infrastructure = 0.10
            governance = 0.11
            equity_burden = 0.22
            pressure_spike = 0.12
            event_name = "background sustainable-development stress"

        stress_load = (
            0.16 * shock
            + 0.16 * climate
            + 0.18 * overshoot
            + 0.13 * economic
            + 0.13 * infrastructure
            + 0.12 * governance
            + 0.12 * pressure_spike
            + 0.08 * resource_pressure
        )

        response_capacity = (
            0.18 * adaptive
            + 0.16 * (1.0 - f(system, "social_vulnerability"))
            + 0.15 * (1.0 - f(system, "economic_fragility"))
            + 0.15 * (1.0 - f(system, "infrastructure_exposure"))
            + 0.15 * (1.0 - governance_constraint)
            + 0.14 * (1.0 - f(system, "ecological_stress"))
            + 0.07 * (1.0 - f(system, "climate_exposure"))
        )
        response_capacity = max(0.0, min(1.0, response_capacity))

        boundary_penalty = max(0.0, resource_pressure + pressure_spike - 1.30) * 0.11
        equity_adjustment = 0.72 + 0.28 * (1.0 - equity_burden + equity_sensitivity * 0.40)

        development_quality = (
            development_quality
            - 0.32 * stress_load
            + 0.20 * response_capacity
            + 0.10 * adaptive
            - 0.09 * resource_pressure
            - 0.08 * governance_constraint
            - boundary_penalty
        )
        development_quality = max(0.0, min(1.0, development_quality))
        resource_pressure = max(0.0, min(1.0, resource_pressure + 0.015 * overshoot + 0.010 * pressure_spike - 0.010 * response_capacity))
        equity_adjusted_quality = max(0.0, min(1.0, development_quality * equity_adjustment))

        rows.append({
            "system_id": system["system_id"],
            "system": system["system"],
            "system_domain": system["system_domain"],
            "time": t,
            "event": event_name,
            "stress_load": round(stress_load, 5),
            "response_capacity": round(response_capacity, 5),
            "development_quality": round(development_quality, 5),
            "resource_pressure": round(resource_pressure, 5),
            "equity_adjusted_quality": round(equity_adjusted_quality, 5),
        })
    return rows

def summarize_simulation(rows):
    summary = []
    for system in sorted(set(str(row["system"]) for row in rows)):
        subset = [row for row in rows if row["system"] == system]
        quality = [float(row["development_quality"]) for row in subset]
        equity = [float(row["equity_adjusted_quality"]) for row in subset]
        pressure = [float(row["resource_pressure"]) for row in subset]
        summary.append({
            "system": system,
            "mean_development_quality": round(mean(quality), 5),
            "minimum_development_quality": round(min(quality), 5),
            "final_development_quality": round(quality[-1], 5),
            "mean_equity_adjusted_quality": round(mean(equity), 5),
            "maximum_resource_pressure": round(max(pressure), 5),
            "final_resource_pressure": round(pressure[-1], 5),
        })
    summary.sort(key=lambda row: row["mean_equity_adjusted_quality"], reverse=True)
    return summary

def pathway_monte_carlo(pathways, scenario, n=3000):
    rng = random.Random(42)
    simulation_rows = []
    for simulation_id in range(n):
        scored = []
        for pathway in pathways:
            sampled = dict(pathway)
            for criterion in BENEFIT_CRITERIA + PENALTY_CRITERIA:
                sampled[criterion] = str(max(1.0, min(10.0, f(pathway, criterion) + rng.gauss(0, 0.6))))
            scored.append((score_pathway(sampled, scenario), pathway))
        scored.sort(key=lambda item: item[0], reverse=True)
        for rank, (value, pathway) in enumerate(scored, start=1):
            simulation_rows.append({
                "simulation_id": simulation_id,
                "pathway_id": pathway["pathway_id"],
                "pathway": pathway["pathway"],
                "rank": rank,
                "viability_value": round(value, 5),
                "winner": scored[0][1]["pathway"],
            })

    robustness_rows = []
    pathway_count = len(pathways)
    for pathway in pathways:
        subset = [row for row in simulation_rows if row["pathway_id"] == pathway["pathway_id"]]
        ranks = [int(row["rank"]) for row in subset]
        values = [float(row["viability_value"]) for row in subset]
        robustness_rows.append({
            "pathway_id": pathway["pathway_id"],
            "pathway": pathway["pathway"],
            "mean_viability_value": round(mean(values), 5),
            "median_viability_value": round(median(values), 5),
            "probability_ranked_first": round(100 * sum(1 for r in ranks if r == 1) / n, 2),
            "probability_top_two": round(100 * sum(1 for r in ranks if r <= 2) / n, 2),
            "probability_bottom_two": round(100 * sum(1 for r in ranks if r >= pathway_count - 1) / n, 2),
        })
    robustness_rows.sort(key=lambda row: row["probability_ranked_first"], reverse=True)
    return simulation_rows, robustness_rows

def main() -> None:
    pathways = read_csv(ROOT / "data/raw/sustainable_resilience_pathways.csv")
    scenarios = read_csv(ROOT / "data/raw/sustainable_resilience_scenarios.csv")
    systems = read_csv(ROOT / "data/raw/development_systems.csv")
    events = read_csv(ROOT / "data/raw/development_stress_events.csv")

    pathway_profiles = []
    for row in pathways:
        value = viability_value(row)
        adjusted = boundary_adjusted_value(row, value)
        pathway_profiles.append({
            "pathway_id": row["pathway_id"],
            "pathway": row["pathway"],
            "system_domain": row["system_domain"],
            "critical_function": row["critical_function"],
            "viability_value": round(value, 5),
            "boundary_adjusted_viability": round(adjusted, 5),
            "equity_adjusted_viability": round(value * (0.72 + 0.028 * f(row, "social_inclusion")), 5),
            "resilience": row["resilience"],
            "ecological_integrity": row["ecological_integrity"],
            "social_inclusion": row["social_inclusion"],
            "economic_sufficiency": row["economic_sufficiency"],
            "governance_capacity": row["governance_capacity"],
            "adaptive_capacity": row["adaptive_capacity"],
            "resource_pressure": row["resource_pressure"],
            "implementation_burden": row["implementation_burden"],
            "diagnostic": pathway_diagnostic(row, value),
        })

    rankings = scenario_rankings(pathways, scenarios)

    dynamic_rows = []
    for idx, system in enumerate(systems):
        dynamic_rows.extend(simulate_development_response(system, events, seed=100 + idx))
    dynamic_summary = summarize_simulation(dynamic_rows)

    baseline = next(s for s in scenarios if s["scenario"] == "Balanced")
    pathway_simulation, robustness_rows = pathway_monte_carlo(pathways, baseline, n=3000)

    first_place_summary = {}
    for row in rankings:
        if int(row["rank"]) == 1:
            first_place_summary[row["pathway"]] = first_place_summary.get(row["pathway"], 0) + 1

    top_rank_rows = [
        {"pathway": pathway, "times_ranked_first": count}
        for pathway, count in sorted(first_place_summary.items(), key=lambda item: item[1], reverse=True)
    ]

    write_csv(OUT_TABLES / "sustainable_resilience_pathway_profiles_standard.csv", pathway_profiles)
    write_csv(OUT_TABLES / "sustainable_resilience_pathway_rankings_standard.csv", rankings)
    write_csv(OUT_TABLES / "sustainable_resilience_top_rank_summary_standard.csv", top_rank_rows)
    write_csv(OUT_TABLES / "development_dynamic_simulation_standard.csv", dynamic_rows)
    write_csv(OUT_TABLES / "development_dynamic_summary_standard.csv", dynamic_summary)
    write_csv(OUT_TABLES / "sustainable_resilience_monte_carlo_standard.csv", pathway_simulation)
    write_csv(OUT_TABLES / "sustainable_resilience_robustness_summary_standard.csv", robustness_rows)
    write_csv(DATA_PROCESSED / "sustainable_resilience_pathway_profiles_standard.csv", pathway_profiles)

    print("Sustainable resilience workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    for row in pathway_profiles:
        print(f"  {row['pathway']}: value={row['viability_value']} diagnostic={row['diagnostic']}")

if __name__ == "__main__":
    main()
