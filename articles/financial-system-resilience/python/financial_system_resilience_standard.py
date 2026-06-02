#!/usr/bin/env python3
# Dependency-light Financial System Resilience workflow.
# Run: python3 python/financial_system_resilience_standard.py

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
    "capital_strength",
    "liquidity_resilience",
    "infrastructure_robustness",
    "governance_capacity",
    "inclusive_resilience",
]

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

def financial_resilience_value(row: dict[str, str]) -> float:
    return (
        0.16 * f(row, "capital_strength")
        + 0.16 * f(row, "liquidity_resilience")
        + 0.16 * f(row, "infrastructure_robustness")
        + 0.16 * f(row, "governance_capacity")
        + 0.16 * f(row, "inclusive_resilience")
        - 0.12 * f(row, "systemic_exposure")
        - 0.08 * f(row, "implementation_burden")
    )

def adjusted_resilience_value(row: dict[str, str], value: float) -> float:
    inclusion_gap = max(0.0, 8.0 - f(row, "inclusive_resilience"))
    infrastructure_gap = max(0.0, 8.0 - f(row, "infrastructure_robustness"))
    liquidity_gap = max(0.0, 8.0 - f(row, "liquidity_resilience"))
    return value - 0.07 * inclusion_gap - 0.06 * infrastructure_gap - 0.05 * liquidity_gap

def score_strategy(row: dict[str, str], scenario: dict[str, str]) -> float:
    return (
        f(scenario, "capital_strength_weight") * f(row, "capital_strength")
        + f(scenario, "liquidity_resilience_weight") * f(row, "liquidity_resilience")
        + f(scenario, "infrastructure_robustness_weight") * f(row, "infrastructure_robustness")
        + f(scenario, "governance_capacity_weight") * f(row, "governance_capacity")
        + f(scenario, "inclusive_resilience_weight") * f(row, "inclusive_resilience")
        - f(scenario, "systemic_exposure_weight") * f(row, "systemic_exposure")
        - f(scenario, "implementation_burden_weight") * f(row, "implementation_burden")
    )

def strategy_diagnostic(row: dict[str, str], value: float) -> str:
    if f(row, "implementation_burden") >= 3.7:
        return "implementation-burden review needed"
    if f(row, "inclusive_resilience") < 7.5:
        return "financial-inclusion review needed"
    if f(row, "infrastructure_robustness") < 7.6:
        return "infrastructure-resilience review needed"
    if f(row, "systemic_exposure") >= 4.4:
        return "systemic-exposure review needed"
    if f(row, "liquidity_resilience") < 7.5:
        return "liquidity-resilience review needed"
    if value >= 4.80:
        return "strong financial resilience strategy candidate"
    return "promising but requires stress testing"

def scenario_rankings(strategies, scenarios):
    rows = []
    for scenario in scenarios:
        scored = sorted(
            [(score_strategy(strategy, scenario), strategy) for strategy in strategies],
            key=lambda item: item[0],
            reverse=True,
        )
        for rank, (value, strategy) in enumerate(scored, start=1):
            rows.append({
                "scenario": scenario["scenario"],
                "strategy_id": strategy["strategy_id"],
                "strategy": strategy["strategy"],
                "system_domain": strategy["system_domain"],
                "rank": rank,
                "financial_resilience_value": round(value, 5),
                "systemic_exposure": strategy["systemic_exposure"],
                "implementation_burden": strategy["implementation_burden"],
                "critical_function": strategy["critical_function"],
            })
    return rows

def simulate_financial_function(system, events, seed, time_steps=90):
    rng = random.Random(seed)
    financial_function = f(system, "baseline_financial_function")
    governance_capacity = f(system, "governance_capacity")
    inclusion_sensitivity = f(system, "inclusion_sensitivity")

    leverage_pressure = f(system, "leverage_pressure")
    liquidity_fragility = f(system, "liquidity_fragility")
    common_asset_exposure = f(system, "common_asset_exposure")
    operational_dependency = f(system, "operational_dependency")
    climate_financial_exposure = f(system, "climate_financial_exposure")
    nonbank_exposure = f(system, "nonbank_exposure")
    household_financial_fragility = f(system, "household_financial_fragility")

    event_by_step = {12: events[0], 26: events[1], 40: events[2], 54: events[3], 68: events[4], 80: events[5]}
    rows = []

    for t in range(time_steps):
        event = event_by_step.get(t)
        if event:
            shock = f(event, "shock_intensity")
            credit_loss = f(event, "credit_loss")
            liquidity_run = f(event, "liquidity_run")
            fire_sale = f(event, "market_fire_sale")
            operational = f(event, "operational_disruption")
            climate = f(event, "climate_repricing")
            nonbank = f(event, "nonbank_stress")
            household = f(event, "household_default_pressure")
            policy_stress = f(event, "policy_coordination_stress")
            inclusion_burden = f(event, "inclusion_burden")
            event_name = event["event_name"]
        else:
            shock = 0.05 + rng.random() * 0.02
            credit_loss = 0.10
            liquidity_run = 0.10 + 0.001 * t
            fire_sale = 0.10
            operational = 0.10
            climate = 0.10 + 0.001 * t
            nonbank = 0.10
            household = 0.11
            policy_stress = 0.10
            inclusion_burden = 0.24
            event_name = "background financial-system stress"

        systemic_exposure = (
            0.14 * leverage_pressure
            + 0.15 * liquidity_fragility
            + 0.14 * common_asset_exposure
            + 0.13 * operational_dependency
            + 0.13 * climate_financial_exposure
            + 0.13 * nonbank_exposure
            + 0.13 * household_financial_fragility
        )

        stress_load = (
            0.10 * shock
            + 0.12 * credit_loss
            + 0.14 * liquidity_run
            + 0.13 * fire_sale
            + 0.12 * operational
            + 0.12 * climate
            + 0.12 * nonbank
            + 0.10 * household
            + 0.10 * policy_stress
            + 0.08 * systemic_exposure
        )

        stabilizing_capacity = (
            0.14 * (1.0 - leverage_pressure)
            + 0.14 * (1.0 - liquidity_fragility)
            + 0.13 * (1.0 - common_asset_exposure)
            + 0.12 * (1.0 - operational_dependency)
            + 0.12 * (1.0 - climate_financial_exposure)
            + 0.12 * (1.0 - nonbank_exposure)
            + 0.12 * (1.0 - household_financial_fragility)
            + 0.18 * governance_capacity
        )
        stabilizing_capacity = max(0.0, min(1.0, stabilizing_capacity))

        inclusion_penalty = max(0.0, inclusion_burden + household_financial_fragility - 1.35) * 0.10
        liquidity_penalty = max(0.0, liquidity_fragility + liquidity_run - 1.35) * 0.08
        operational_penalty = max(0.0, operational_dependency + operational - 1.35) * 0.07

        financial_function = (
            financial_function
            - 0.32 * stress_load
            + 0.22 * stabilizing_capacity
            + 0.08 * governance_capacity
            - inclusion_penalty
            - liquidity_penalty
            - operational_penalty
        )
        financial_function = max(0.0, min(1.0, financial_function))

        liquidity_fragility = max(0.0, min(1.0, liquidity_fragility + 0.012 * liquidity_run + 0.010 * fire_sale - 0.010 * stabilizing_capacity))
        household_financial_fragility = max(0.0, min(1.0, household_financial_fragility + 0.012 * household + 0.010 * inclusion_burden - 0.010 * stabilizing_capacity))
        inclusion_adjusted_function = max(0.0, min(1.0, financial_function * (0.72 + 0.28 * (1.0 - inclusion_burden + inclusion_sensitivity * 0.40))))

        rows.append({
            "system_id": system["system_id"],
            "system": system["system"],
            "system_context": system["system_context"],
            "time": t,
            "event": event_name,
            "stress_load": round(stress_load, 5),
            "stabilizing_capacity": round(stabilizing_capacity, 5),
            "financial_function": round(financial_function, 5),
            "liquidity_fragility": round(liquidity_fragility, 5),
            "household_financial_fragility": round(household_financial_fragility, 5),
            "inclusion_adjusted_function": round(inclusion_adjusted_function, 5),
        })
    return rows

def summarize_simulation(rows):
    summary = []
    for system in sorted(set(str(row["system"]) for row in rows)):
        subset = [row for row in rows if row["system"] == system]
        function = [float(row["financial_function"]) for row in subset]
        inclusion = [float(row["inclusion_adjusted_function"]) for row in subset]
        liquidity = [float(row["liquidity_fragility"]) for row in subset]
        household = [float(row["household_financial_fragility"]) for row in subset]
        summary.append({
            "system": system,
            "mean_financial_function": round(mean(function), 5),
            "minimum_financial_function": round(min(function), 5),
            "final_financial_function": round(function[-1], 5),
            "mean_inclusion_adjusted_function": round(mean(inclusion), 5),
            "maximum_liquidity_fragility": round(max(liquidity), 5),
            "final_liquidity_fragility": round(liquidity[-1], 5),
            "maximum_household_financial_fragility": round(max(household), 5),
            "final_household_financial_fragility": round(household[-1], 5),
        })
    summary.sort(key=lambda row: row["mean_inclusion_adjusted_function"], reverse=True)
    return summary

def strategy_monte_carlo(strategies, scenario, n=3000):
    rng = random.Random(42)
    simulation_rows = []
    for simulation_id in range(n):
        scored = []
        for strategy in strategies:
            sampled = dict(strategy)
            for criterion in BENEFIT_CRITERIA + ["systemic_exposure", "implementation_burden"]:
                sampled[criterion] = str(max(1.0, min(10.0, f(strategy, criterion) + rng.gauss(0, 0.6))))
            scored.append((score_strategy(sampled, scenario), strategy))
        scored.sort(key=lambda item: item[0], reverse=True)
        for rank, (value, strategy) in enumerate(scored, start=1):
            simulation_rows.append({
                "simulation_id": simulation_id,
                "strategy_id": strategy["strategy_id"],
                "strategy": strategy["strategy"],
                "rank": rank,
                "financial_resilience_value": round(value, 5),
                "winner": scored[0][1]["strategy"],
            })

    robustness_rows = []
    strategy_count = len(strategies)
    for strategy in strategies:
        subset = [row for row in simulation_rows if row["strategy_id"] == strategy["strategy_id"]]
        ranks = [int(row["rank"]) for row in subset]
        values = [float(row["financial_resilience_value"]) for row in subset]
        robustness_rows.append({
            "strategy_id": strategy["strategy_id"],
            "strategy": strategy["strategy"],
            "mean_financial_resilience_value": round(mean(values), 5),
            "median_financial_resilience_value": round(median(values), 5),
            "probability_ranked_first": round(100 * sum(1 for r in ranks if r == 1) / n, 2),
            "probability_top_two": round(100 * sum(1 for r in ranks if r <= 2) / n, 2),
            "probability_bottom_two": round(100 * sum(1 for r in ranks if r >= strategy_count - 1) / n, 2),
        })
    robustness_rows.sort(key=lambda row: row["probability_ranked_first"], reverse=True)
    return simulation_rows, robustness_rows

def main() -> None:
    strategies = read_csv(ROOT / "data/raw/financial_resilience_strategies.csv")
    scenarios = read_csv(ROOT / "data/raw/financial_resilience_scenarios.csv")
    systems = read_csv(ROOT / "data/raw/financial_system_profiles.csv")
    events = read_csv(ROOT / "data/raw/financial_stress_events.csv")

    strategy_profiles = []
    for row in strategies:
        value = financial_resilience_value(row)
        adjusted = adjusted_resilience_value(row, value)
        strategy_profiles.append({
            "strategy_id": row["strategy_id"],
            "strategy": row["strategy"],
            "system_domain": row["system_domain"],
            "critical_function": row["critical_function"],
            "financial_resilience_value": round(value, 5),
            "adjusted_financial_resilience_value": round(adjusted, 5),
            "inclusion_adjusted_value": round(value * (0.72 + 0.028 * f(row, "inclusive_resilience")), 5),
            "capital_strength": row["capital_strength"],
            "liquidity_resilience": row["liquidity_resilience"],
            "infrastructure_robustness": row["infrastructure_robustness"],
            "governance_capacity": row["governance_capacity"],
            "inclusive_resilience": row["inclusive_resilience"],
            "systemic_exposure": row["systemic_exposure"],
            "implementation_burden": row["implementation_burden"],
            "diagnostic": strategy_diagnostic(row, value),
        })

    rankings = scenario_rankings(strategies, scenarios)

    dynamic_rows = []
    for idx, system in enumerate(systems):
        dynamic_rows.extend(simulate_financial_function(system, events, seed=100 + idx))
    dynamic_summary = summarize_simulation(dynamic_rows)

    baseline = next(s for s in scenarios if s["scenario"] == "Balanced")
    strategy_simulation, robustness_rows = strategy_monte_carlo(strategies, baseline, n=3000)

    first_place_summary = {}
    for row in rankings:
        if int(row["rank"]) == 1:
            first_place_summary[row["strategy"]] = first_place_summary.get(row["strategy"], 0) + 1

    top_rank_rows = [
        {"strategy": strategy, "times_ranked_first": count}
        for strategy, count in sorted(first_place_summary.items(), key=lambda item: item[1], reverse=True)
    ]

    write_csv(OUT_TABLES / "financial_resilience_strategy_profiles_standard.csv", strategy_profiles)
    write_csv(OUT_TABLES / "financial_resilience_strategy_rankings_standard.csv", rankings)
    write_csv(OUT_TABLES / "financial_resilience_top_rank_summary_standard.csv", top_rank_rows)
    write_csv(OUT_TABLES / "financial_resilience_dynamic_simulation_standard.csv", dynamic_rows)
    write_csv(OUT_TABLES / "financial_resilience_dynamic_summary_standard.csv", dynamic_summary)
    write_csv(OUT_TABLES / "financial_resilience_monte_carlo_standard.csv", strategy_simulation)
    write_csv(OUT_TABLES / "financial_resilience_robustness_summary_standard.csv", robustness_rows)
    write_csv(DATA_PROCESSED / "financial_resilience_strategy_profiles_standard.csv", strategy_profiles)

    print("Financial system resilience workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    for row in strategy_profiles:
        print(f"  {row['strategy']}: value={row['financial_resilience_value']} diagnostic={row['diagnostic']}")

if __name__ == "__main__":
    main()
