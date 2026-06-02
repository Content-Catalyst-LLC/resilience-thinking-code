#!/usr/bin/env python3
# Dependency-light Economic Resilience workflow.
# Run: python3 python/economic_resilience_standard.py

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
    "resistance",
    "recovery",
    "adaptability",
    "transformability",
    "equity_protection",
    "institutional_capacity",
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

def economic_resilience_value(row: dict[str, str]) -> float:
    return (
        0.16 * f(row, "resistance")
        + 0.16 * f(row, "recovery")
        + 0.17 * f(row, "adaptability")
        + 0.17 * f(row, "transformability")
        + 0.17 * f(row, "equity_protection")
        + 0.17 * f(row, "institutional_capacity")
        - 0.02 * f(row, "implementation_burden")
    )

def adjusted_resilience_value(row: dict[str, str], value: float) -> float:
    equity_gap = max(0.0, 8.3 - f(row, "equity_protection"))
    institutional_gap = max(0.0, 8.2 - f(row, "institutional_capacity"))
    transformation_gap = max(0.0, 8.0 - f(row, "transformability"))
    return value - 0.08 * equity_gap - 0.06 * institutional_gap - 0.05 * transformation_gap

def score_strategy(row: dict[str, str], scenario: dict[str, str]) -> float:
    return (
        f(scenario, "resistance_weight") * f(row, "resistance")
        + f(scenario, "recovery_weight") * f(row, "recovery")
        + f(scenario, "adaptability_weight") * f(row, "adaptability")
        + f(scenario, "transformability_weight") * f(row, "transformability")
        + f(scenario, "equity_protection_weight") * f(row, "equity_protection")
        + f(scenario, "institutional_capacity_weight") * f(row, "institutional_capacity")
        - f(scenario, "implementation_burden_weight") * f(row, "implementation_burden")
    )

def strategy_diagnostic(row: dict[str, str], value: float) -> str:
    if f(row, "implementation_burden") >= 3.6:
        return "implementation-burden review needed"
    if f(row, "equity_protection") < 8.0:
        return "equity safeguards need strengthening"
    if f(row, "institutional_capacity") < 8.0:
        return "institutional-capacity review needed"
    if f(row, "transformability") < 7.8:
        return "transformation pathway review needed"
    if f(row, "resistance") < 7.8:
        return "resistance-capacity review needed"
    if value >= 8.20:
        return "strong economic resilience strategy candidate"
    return "promising but requires scenario validation"

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
                "economic_resilience_value": round(value, 5),
                "implementation_burden": strategy["implementation_burden"],
                "critical_function": strategy["critical_function"],
            })
    return rows

def simulate_economic_function(system, events, seed, time_steps=80):
    rng = random.Random(seed)
    economic_function = f(system, "baseline_economic_function")
    institutional_capacity = f(system, "institutional_capacity")
    equity_sensitivity = f(system, "equity_sensitivity")

    sector_concentration = f(system, "sector_concentration")
    household_fragility = f(system, "household_fragility")
    firm_fragility = f(system, "firm_fragility")
    financial_exposure = f(system, "financial_exposure")
    labor_rigidity = f(system, "labor_market_rigidity")
    infrastructure_exposure = f(system, "infrastructure_exposure")
    climate_exposure = f(system, "climate_exposure")

    event_by_step = {12: events[0], 27: events[1], 42: events[2], 56: events[3], 70: events[4]}
    rows = []

    for t in range(time_steps):
        event = event_by_step.get(t)
        if event:
            shock = f(event, "shock_intensity")
            demand = f(event, "demand_shock")
            supply = f(event, "supply_shock")
            finance = f(event, "financial_stress")
            labor = f(event, "labor_disruption")
            infrastructure = f(event, "infrastructure_stress")
            climate = f(event, "climate_pressure")
            fiscal = f(event, "fiscal_pressure")
            equity_burden = f(event, "equity_burden")
            event_name = event["event_name"]
        else:
            shock = 0.05 + rng.random() * 0.02
            demand = 0.11
            supply = 0.10
            finance = 0.09 + 0.001 * t
            labor = 0.10
            infrastructure = 0.10
            climate = 0.11
            fiscal = 0.10 + 0.001 * t
            equity_burden = 0.22
            event_name = "background economic stress"

        fragility = (
            0.13 * sector_concentration
            + 0.15 * household_fragility
            + 0.13 * firm_fragility
            + 0.14 * financial_exposure
            + 0.12 * labor_rigidity
            + 0.13 * infrastructure_exposure
            + 0.13 * climate_exposure
        )

        stress_load = (
            0.13 * shock
            + 0.13 * demand
            + 0.13 * supply
            + 0.14 * finance
            + 0.12 * labor
            + 0.13 * infrastructure
            + 0.12 * climate
            + 0.12 * fiscal
            + 0.08 * fragility
        )

        adaptive_response = (
            0.16 * (1.0 - sector_concentration)
            + 0.14 * (1.0 - household_fragility)
            + 0.14 * (1.0 - firm_fragility)
            + 0.14 * (1.0 - financial_exposure)
            + 0.13 * (1.0 - labor_rigidity)
            + 0.13 * (1.0 - infrastructure_exposure)
            + 0.12 * (1.0 - climate_exposure)
            + 0.16 * institutional_capacity
        )
        adaptive_response = max(0.0, min(1.0, adaptive_response))

        equity_penalty = max(0.0, equity_burden + household_fragility - 1.35) * 0.10
        fiscal_penalty = max(0.0, fiscal + financial_exposure - 1.35) * 0.07

        economic_function = (
            economic_function
            - 0.32 * stress_load
            + 0.22 * adaptive_response
            + 0.08 * institutional_capacity
            - equity_penalty
            - fiscal_penalty
        )
        economic_function = max(0.0, min(1.0, economic_function))

        household_fragility = max(0.0, min(1.0, household_fragility + 0.012 * demand + 0.010 * labor + 0.010 * equity_burden - 0.010 * adaptive_response))
        firm_fragility = max(0.0, min(1.0, firm_fragility + 0.012 * supply + 0.012 * finance - 0.010 * adaptive_response))
        equity_adjusted_function = max(0.0, min(1.0, economic_function * (0.72 + 0.28 * (1.0 - equity_burden + equity_sensitivity * 0.40))))

        rows.append({
            "system_id": system["system_id"],
            "system": system["system"],
            "system_context": system["system_context"],
            "time": t,
            "event": event_name,
            "stress_load": round(stress_load, 5),
            "adaptive_response": round(adaptive_response, 5),
            "economic_function": round(economic_function, 5),
            "household_fragility": round(household_fragility, 5),
            "firm_fragility": round(firm_fragility, 5),
            "equity_adjusted_function": round(equity_adjusted_function, 5),
        })
    return rows

def summarize_simulation(rows):
    summary = []
    for system in sorted(set(str(row["system"]) for row in rows)):
        subset = [row for row in rows if row["system"] == system]
        function = [float(row["economic_function"]) for row in subset]
        equity = [float(row["equity_adjusted_function"]) for row in subset]
        household = [float(row["household_fragility"]) for row in subset]
        firm = [float(row["firm_fragility"]) for row in subset]
        summary.append({
            "system": system,
            "mean_economic_function": round(mean(function), 5),
            "minimum_economic_function": round(min(function), 5),
            "final_economic_function": round(function[-1], 5),
            "mean_equity_adjusted_function": round(mean(equity), 5),
            "maximum_household_fragility": round(max(household), 5),
            "final_household_fragility": round(household[-1], 5),
            "maximum_firm_fragility": round(max(firm), 5),
            "final_firm_fragility": round(firm[-1], 5),
        })
    summary.sort(key=lambda row: row["mean_equity_adjusted_function"], reverse=True)
    return summary

def strategy_monte_carlo(strategies, scenario, n=3000):
    rng = random.Random(42)
    simulation_rows = []
    for simulation_id in range(n):
        scored = []
        for strategy in strategies:
            sampled = dict(strategy)
            for criterion in BENEFIT_CRITERIA + ["implementation_burden"]:
                sampled[criterion] = str(max(1.0, min(10.0, f(strategy, criterion) + rng.gauss(0, 0.6))))
            scored.append((score_strategy(sampled, scenario), strategy))
        scored.sort(key=lambda item: item[0], reverse=True)
        for rank, (value, strategy) in enumerate(scored, start=1):
            simulation_rows.append({
                "simulation_id": simulation_id,
                "strategy_id": strategy["strategy_id"],
                "strategy": strategy["strategy"],
                "rank": rank,
                "economic_resilience_value": round(value, 5),
                "winner": scored[0][1]["strategy"],
            })

    robustness_rows = []
    strategy_count = len(strategies)
    for strategy in strategies:
        subset = [row for row in simulation_rows if row["strategy_id"] == strategy["strategy_id"]]
        ranks = [int(row["rank"]) for row in subset]
        values = [float(row["economic_resilience_value"]) for row in subset]
        robustness_rows.append({
            "strategy_id": strategy["strategy_id"],
            "strategy": strategy["strategy"],
            "mean_economic_resilience_value": round(mean(values), 5),
            "median_economic_resilience_value": round(median(values), 5),
            "probability_ranked_first": round(100 * sum(1 for r in ranks if r == 1) / n, 2),
            "probability_top_two": round(100 * sum(1 for r in ranks if r <= 2) / n, 2),
            "probability_bottom_two": round(100 * sum(1 for r in ranks if r >= strategy_count - 1) / n, 2),
        })
    robustness_rows.sort(key=lambda row: row["probability_ranked_first"], reverse=True)
    return simulation_rows, robustness_rows

def main() -> None:
    strategies = read_csv(ROOT / "data/raw/economic_resilience_strategies.csv")
    scenarios = read_csv(ROOT / "data/raw/economic_resilience_scenarios.csv")
    systems = read_csv(ROOT / "data/raw/economic_system_profiles.csv")
    events = read_csv(ROOT / "data/raw/economic_stress_events.csv")

    strategy_profiles = []
    for row in strategies:
        value = economic_resilience_value(row)
        adjusted = adjusted_resilience_value(row, value)
        strategy_profiles.append({
            "strategy_id": row["strategy_id"],
            "strategy": row["strategy"],
            "system_domain": row["system_domain"],
            "critical_function": row["critical_function"],
            "economic_resilience_value": round(value, 5),
            "adjusted_economic_resilience_value": round(adjusted, 5),
            "equity_adjusted_value": round(value * (0.72 + 0.028 * f(row, "equity_protection")), 5),
            "resistance": row["resistance"],
            "recovery": row["recovery"],
            "adaptability": row["adaptability"],
            "transformability": row["transformability"],
            "equity_protection": row["equity_protection"],
            "institutional_capacity": row["institutional_capacity"],
            "implementation_burden": row["implementation_burden"],
            "diagnostic": strategy_diagnostic(row, value),
        })

    rankings = scenario_rankings(strategies, scenarios)

    dynamic_rows = []
    for idx, system in enumerate(systems):
        dynamic_rows.extend(simulate_economic_function(system, events, seed=100 + idx))
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

    write_csv(OUT_TABLES / "economic_resilience_strategy_profiles_standard.csv", strategy_profiles)
    write_csv(OUT_TABLES / "economic_resilience_strategy_rankings_standard.csv", rankings)
    write_csv(OUT_TABLES / "economic_resilience_top_rank_summary_standard.csv", top_rank_rows)
    write_csv(OUT_TABLES / "economic_resilience_dynamic_simulation_standard.csv", dynamic_rows)
    write_csv(OUT_TABLES / "economic_resilience_dynamic_summary_standard.csv", dynamic_summary)
    write_csv(OUT_TABLES / "economic_resilience_monte_carlo_standard.csv", strategy_simulation)
    write_csv(OUT_TABLES / "economic_resilience_robustness_summary_standard.csv", robustness_rows)
    write_csv(DATA_PROCESSED / "economic_resilience_strategy_profiles_standard.csv", strategy_profiles)

    print("Economic resilience workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    for row in strategy_profiles:
        print(f"  {row['strategy']}: value={row['economic_resilience_value']} diagnostic={row['diagnostic']}")

if __name__ == "__main__":
    main()
