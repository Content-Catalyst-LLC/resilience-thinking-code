#!/usr/bin/env python3
# Dependency-light Institutional Resilience workflow.
# Run: python3 python/institutional_resilience_standard.py

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
    "legitimacy",
    "capacity",
    "flexibility",
    "coordination",
    "learning",
    "accountability",
    "equity_protection",
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

def base_resilience_value(row: dict[str, str]) -> float:
    return (
        0.14 * f(row, "legitimacy")
        + 0.14 * f(row, "capacity")
        + 0.13 * f(row, "flexibility")
        + 0.14 * f(row, "coordination")
        + 0.14 * f(row, "learning")
        + 0.14 * f(row, "accountability")
        + 0.15 * f(row, "equity_protection")
        - 0.02 * f(row, "implementation_burden")
    )

def score_strategy(row: dict[str, str], scenario: dict[str, str]) -> float:
    return (
        f(scenario, "legitimacy_weight") * f(row, "legitimacy")
        + f(scenario, "capacity_weight") * f(row, "capacity")
        + f(scenario, "flexibility_weight") * f(row, "flexibility")
        + f(scenario, "coordination_weight") * f(row, "coordination")
        + f(scenario, "learning_weight") * f(row, "learning")
        + f(scenario, "accountability_weight") * f(row, "accountability")
        + f(scenario, "equity_protection_weight") * f(row, "equity_protection")
        - f(scenario, "implementation_burden_weight") * f(row, "implementation_burden")
    )

def strategy_diagnostic(row: dict[str, str], value: float) -> str:
    if value >= 8.10 and f(row, "implementation_burden") <= 3.0:
        return "strong institutional resilience profile with manageable implementation burden"
    if f(row, "implementation_burden") >= 3.3:
        return "implementation burden review needed"
    if f(row, "equity_protection") < 7.8:
        return "equity protection needs strengthening"
    if f(row, "legitimacy") < 7.6:
        return "legitimacy and trust review needed"
    if f(row, "capacity") < 7.5:
        return "administrative capacity needs strengthening"
    if f(row, "coordination") < 7.6:
        return "coordination review needed"
    return "promising but requires institutional scenario validation"

def threshold_risk(row: dict[str, str]) -> float:
    critical_min = min(
        f(row, "legitimacy"),
        f(row, "capacity"),
        f(row, "coordination"),
        f(row, "accountability"),
        f(row, "equity_protection"),
    )
    return max(0.0, 8.0 - critical_min)

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
                "resilience_value": round(value, 5),
                "threshold_risk": round(threshold_risk(strategy), 5),
                "implementation_burden": strategy["implementation_burden"],
                "critical_function": strategy["critical_function"],
            })
    return rows

def simulate_institutional_response(system, events, seed, time_steps=80):
    rng = random.Random(seed)
    function_level = f(system, "baseline_function")
    legitimacy = f(system, "legitimacy")
    capacity = f(system, "capacity")
    flexibility = f(system, "flexibility")
    coordination = f(system, "coordination")
    learning = f(system, "learning")
    accountability = f(system, "accountability")
    dependency = f(system, "dependency_coupling")
    equity_sensitivity = f(system, "equity_sensitivity")

    event_by_step = {12: events[0], 27: events[1], 42: events[2], 56: events[3], 70: events[4]}
    rows = []

    for t in range(time_steps):
        event = event_by_step.get(t)
        if event:
            shock = f(event, "shock_intensity")
            legitimacy_pressure = f(event, "legitimacy_pressure")
            capacity_burden = f(event, "capacity_burden")
            coordination_stress = f(event, "coordination_stress")
            information_stress = f(event, "information_stress")
            legal_stress = f(event, "legal_accountability_stress")
            equity_burden = f(event, "equity_burden")
            dependency_amplification = f(event, "dependency_amplification")
            event_name = event["event_name"]
        else:
            shock = 0.05 + rng.random() * 0.02
            legitimacy_pressure = 0.10 + rng.random() * 0.03
            capacity_burden = 0.12
            coordination_stress = 0.10
            information_stress = 0.10
            legal_stress = 0.09 + 0.0015 * t
            equity_burden = 0.22
            dependency_amplification = 0.12
            event_name = "background institutional stress"

        stress_load = (
            0.18 * shock
            + 0.17 * legitimacy_pressure
            + 0.16 * capacity_burden
            + 0.16 * coordination_stress
            + 0.13 * information_stress
            + 0.12 * legal_stress
            + 0.10 * dependency_amplification
            + 0.08 * dependency
        )

        response_capacity = (
            0.17 * legitimacy
            + 0.18 * capacity
            + 0.14 * flexibility
            + 0.18 * coordination
            + 0.17 * learning
            + 0.16 * accountability
            - 0.16 * f(system, "stress_exposure")
            - 0.12 * f(system, "chronic_stress")
            - 0.10 * dependency
        )
        response_capacity = max(0.0, min(1.0, response_capacity))

        weakest_condition = min(legitimacy, capacity, coordination, accountability)
        threshold_penalty = max(0.0, 0.72 - weakest_condition) * 0.16

        function_level = (
            function_level
            - 0.34 * stress_load
            + 0.18 * response_capacity
            + 0.08 * legitimacy
            + 0.09 * capacity
            + 0.07 * flexibility
            + 0.09 * coordination
            + 0.08 * learning
            + 0.08 * accountability
            - 0.05 * dependency
            - threshold_penalty
        )
        function_level = max(0.0, min(1.0, function_level))
        dependency = max(0.0, min(1.0, dependency + 0.020 * stress_load - 0.011 * response_capacity))
        equity_adjusted_function = function_level * (0.72 + 0.28 * (1.0 - equity_burden + equity_sensitivity * 0.40))
        equity_adjusted_function = max(0.0, min(1.0, equity_adjusted_function))

        rows.append({
            "system_id": system["system_id"],
            "system": system["system"],
            "system_domain": system["system_domain"],
            "time": t,
            "event": event_name,
            "stress_load": round(stress_load, 5),
            "response_capacity": round(response_capacity, 5),
            "institutional_function": round(function_level, 5),
            "dependency_coupling": round(dependency, 5),
            "equity_adjusted_function": round(equity_adjusted_function, 5),
        })
    return rows

def summarize_simulation(rows):
    summary = []
    for system in sorted(set(str(row["system"]) for row in rows)):
        subset = [row for row in rows if row["system"] == system]
        function_values = [float(row["institutional_function"]) for row in subset]
        equity = [float(row["equity_adjusted_function"]) for row in subset]
        dependency = [float(row["dependency_coupling"]) for row in subset]
        summary.append({
            "system": system,
            "mean_institutional_function": round(mean(function_values), 5),
            "minimum_institutional_function": round(min(function_values), 5),
            "final_institutional_function": round(function_values[-1], 5),
            "mean_equity_adjusted_function": round(mean(equity), 5),
            "maximum_dependency_coupling": round(max(dependency), 5),
            "final_dependency_coupling": round(dependency[-1], 5),
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
                "resilience_value": round(value, 5),
                "winner": scored[0][1]["strategy"],
            })

    robustness_rows = []
    strategy_count = len(strategies)
    for strategy in strategies:
        subset = [row for row in simulation_rows if row["strategy_id"] == strategy["strategy_id"]]
        ranks = [int(row["rank"]) for row in subset]
        values = [float(row["resilience_value"]) for row in subset]
        robustness_rows.append({
            "strategy_id": strategy["strategy_id"],
            "strategy": strategy["strategy"],
            "mean_resilience_value": round(mean(values), 5),
            "median_resilience_value": round(median(values), 5),
            "probability_ranked_first": round(100 * sum(1 for r in ranks if r == 1) / n, 2),
            "probability_top_two": round(100 * sum(1 for r in ranks if r <= 2) / n, 2),
            "probability_bottom_two": round(100 * sum(1 for r in ranks if r >= strategy_count - 1) / n, 2),
        })
    robustness_rows.sort(key=lambda row: row["probability_ranked_first"], reverse=True)
    return simulation_rows, robustness_rows

def main() -> None:
    strategies = read_csv(ROOT / "data/raw/institutional_resilience_strategies.csv")
    scenarios = read_csv(ROOT / "data/raw/institutional_resilience_scenarios.csv")
    systems = read_csv(ROOT / "data/raw/institutional_systems.csv")
    events = read_csv(ROOT / "data/raw/institutional_stress_events.csv")

    strategy_profiles = []
    for row in strategies:
        value = base_resilience_value(row)
        strategy_profiles.append({
            "strategy_id": row["strategy_id"],
            "strategy": row["strategy"],
            "system_domain": row["system_domain"],
            "critical_function": row["critical_function"],
            "base_resilience_value": round(value, 5),
            "equity_adjusted_value": round(value * (0.72 + 0.028 * f(row, "equity_protection")), 5),
            "threshold_risk": round(threshold_risk(row), 5),
            "legitimacy": row["legitimacy"],
            "capacity": row["capacity"],
            "flexibility": row["flexibility"],
            "coordination": row["coordination"],
            "learning": row["learning"],
            "accountability": row["accountability"],
            "equity_protection": row["equity_protection"],
            "implementation_burden": row["implementation_burden"],
            "diagnostic": strategy_diagnostic(row, value),
        })

    rankings = scenario_rankings(strategies, scenarios)

    dynamic_rows = []
    for idx, system in enumerate(systems):
        dynamic_rows.extend(simulate_institutional_response(system, events, seed=100 + idx))
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

    write_csv(OUT_TABLES / "institutional_resilience_strategy_profiles_standard.csv", strategy_profiles)
    write_csv(OUT_TABLES / "institutional_resilience_strategy_rankings_standard.csv", rankings)
    write_csv(OUT_TABLES / "institutional_resilience_top_rank_summary_standard.csv", top_rank_rows)
    write_csv(OUT_TABLES / "institutional_dynamic_simulation_standard.csv", dynamic_rows)
    write_csv(OUT_TABLES / "institutional_dynamic_summary_standard.csv", dynamic_summary)
    write_csv(OUT_TABLES / "institutional_resilience_monte_carlo_standard.csv", strategy_simulation)
    write_csv(OUT_TABLES / "institutional_resilience_robustness_summary_standard.csv", robustness_rows)
    write_csv(DATA_PROCESSED / "institutional_resilience_strategy_profiles_standard.csv", strategy_profiles)

    print("Institutional resilience workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    for row in strategy_profiles:
        print(f"  {row['strategy']}: value={row['base_resilience_value']} diagnostic={row['diagnostic']}")

if __name__ == "__main__":
    main()
