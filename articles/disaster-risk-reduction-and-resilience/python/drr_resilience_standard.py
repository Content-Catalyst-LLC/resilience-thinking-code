#!/usr/bin/env python3
"""
Dependency-light Disaster Risk Reduction and resilience workflow.

Reads synthetic strategy, scenario, system, and disaster stress data.
Calculates DRR strategy rankings, justice-adjusted values,
maladaptation diagnostics, cascading stress-response simulations,
and Monte Carlo robustness using only the Python standard library.

Run:
    python3 python/drr_resilience_standard.py
"""

from __future__ import annotations

import csv
import random
from pathlib import Path
from statistics import mean, median


ROOT = Path(__file__).resolve().parents[1]
STRATEGIES_PATH = ROOT / "data" / "raw" / "drr_resilience_strategies.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "drr_resilience_scenarios.csv"
SYSTEMS_PATH = ROOT / "data" / "raw" / "drr_resilience_systems.csv"
EVENTS_PATH = ROOT / "data" / "raw" / "disaster_stress_events.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
DATA_PROCESSED = ROOT / "data" / "processed"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

BENEFIT_CRITERIA = [
    "hazard_reduction",
    "exposure_reduction",
    "vulnerability_reduction",
    "capacity_enhancement",
    "justice_protection",
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


def base_drr_value(row: dict[str, str]) -> float:
    return (
        0.17 * f(row, "hazard_reduction")
        + 0.18 * f(row, "exposure_reduction")
        + 0.18 * f(row, "vulnerability_reduction")
        + 0.17 * f(row, "capacity_enhancement")
        + 0.18 * f(row, "justice_protection")
        - 0.12 * f(row, "maladaptation_risk")
    )


def score_strategy(row: dict[str, str], scenario: dict[str, str]) -> float:
    return (
        f(scenario, "hazard_reduction_weight") * f(row, "hazard_reduction")
        + f(scenario, "exposure_reduction_weight") * f(row, "exposure_reduction")
        + f(scenario, "vulnerability_reduction_weight") * f(row, "vulnerability_reduction")
        + f(scenario, "capacity_enhancement_weight") * f(row, "capacity_enhancement")
        + f(scenario, "justice_protection_weight") * f(row, "justice_protection")
        - f(scenario, "maladaptation_risk_weight") * f(row, "maladaptation_risk")
    )


def strategy_diagnostic(row: dict[str, str], value: float) -> str:
    if value >= 7.35 and f(row, "maladaptation_risk") <= 2.7:
        return "strong DRR and resilience profile with manageable maladaptation risk"
    if f(row, "maladaptation_risk") >= 3.6:
        return "maladaptation review needed"
    if f(row, "justice_protection") < 7.5:
        return "justice protection needs strengthening"
    if f(row, "capacity_enhancement") < 7.2:
        return "capacity constraint"
    return "promising but requires scenario and implementation validation"


def scenario_rankings(strategies: list[dict[str, str]], scenarios: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    for scenario in scenarios:
        scored = []
        for strategy in strategies:
            value = score_strategy(strategy, scenario)
            scored.append((value, strategy))
        scored.sort(key=lambda item: item[0], reverse=True)

        for rank, (value, strategy) in enumerate(scored, start=1):
            rows.append(
                {
                    "scenario": scenario["scenario"],
                    "strategy_id": strategy["strategy_id"],
                    "strategy": strategy["strategy"],
                    "system_domain": strategy["system_domain"],
                    "rank": rank,
                    "drr_value": round(value, 5),
                    "maladaptation_risk": strategy["maladaptation_risk"],
                    "critical_function": strategy["critical_function"],
                }
            )
    return rows


def simulate_system_response(
    system: dict[str, str],
    events: list[dict[str, str]],
    seed: int,
    time_steps: int = 80,
) -> list[dict[str, object]]:
    rng = random.Random(seed)

    function_level = f(system, "baseline_function")
    preparedness = f(system, "preparedness_capacity")
    recovery = f(system, "recovery_capacity")
    dependency = f(system, "dependency_coupling")
    justice_sensitivity = f(system, "justice_sensitivity")

    event_by_step = {12: events[0], 28: events[1], 43: events[2], 59: events[3], 70: events[4]}
    rows: list[dict[str, object]] = []

    for t in range(time_steps):
        event = event_by_step.get(t)

        if event:
            shock = f(event, "shock_intensity")
            slow = f(event, "slow_stress")
            compound = f(event, "compound_risk")
            cascade = f(event, "cascading_dependency")
            justice_burden = f(event, "justice_burden")
            event_name = event["event_name"]
        else:
            shock = 0.04 + rng.random() * 0.02
            slow = 0.16 + 0.0025 * t
            compound = 0.10
            cascade = 0.12
            justice_burden = 0.20
            event_name = "background risk stress"

        stress_load = (
            0.38 * shock
            + 0.20 * slow
            + 0.18 * compound
            + 0.16 * cascade
            + 0.08 * dependency
        )

        response_capacity = (
            0.45 * preparedness
            + 0.34 * recovery
            - 0.24 * f(system, "hazard_exposure")
            - 0.18 * f(system, "vulnerability")
            - 0.12 * dependency
        )
        response_capacity = max(0.0, min(1.0, response_capacity))

        function_level = (
            function_level
            - 0.34 * stress_load
            + 0.23 * response_capacity
            + 0.13 * recovery
            - 0.07 * dependency
        )
        function_level = max(0.0, min(1.0, function_level))

        dependency = max(0.0, min(1.0, dependency + 0.018 * stress_load - 0.010 * response_capacity))
        justice_adjusted_function = function_level * (0.72 + 0.28 * (1.0 - justice_burden + justice_sensitivity * 0.45))
        justice_adjusted_function = max(0.0, min(1.0, justice_adjusted_function))

        rows.append(
            {
                "system_id": system["system_id"],
                "system": system["system"],
                "system_domain": system["system_domain"],
                "time": t,
                "event": event_name,
                "stress_load": round(stress_load, 5),
                "response_capacity": round(response_capacity, 5),
                "function_level": round(function_level, 5),
                "dependency_coupling": round(dependency, 5),
                "justice_adjusted_function": round(justice_adjusted_function, 5),
            }
        )

    return rows


def summarize_simulation(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    systems = sorted(set(str(row["system"]) for row in rows))
    summary: list[dict[str, object]] = []

    for system in systems:
        subset = [row for row in rows if row["system"] == system]
        functions = [float(row["function_level"]) for row in subset]
        justice = [float(row["justice_adjusted_function"]) for row in subset]
        dependencies = [float(row["dependency_coupling"]) for row in subset]

        summary.append(
            {
                "system": system,
                "mean_function": round(mean(functions), 5),
                "minimum_function": round(min(functions), 5),
                "final_function": round(functions[-1], 5),
                "mean_justice_adjusted_function": round(mean(justice), 5),
                "maximum_dependency_coupling": round(max(dependencies), 5),
                "final_dependency_coupling": round(dependencies[-1], 5),
            }
        )

    summary.sort(key=lambda row: row["mean_justice_adjusted_function"], reverse=True)
    return summary


def strategy_monte_carlo(
    strategies: list[dict[str, str]],
    scenario: dict[str, str],
    n: int = 3000,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rng = random.Random(42)
    simulation_rows = []

    for simulation_id in range(n):
        scored = []
        for strategy in strategies:
            sampled = dict(strategy)

            for criterion in BENEFIT_CRITERIA + ["maladaptation_risk"]:
                sampled_value = max(1.0, min(10.0, f(strategy, criterion) + rng.gauss(0, 0.6)))
                sampled[criterion] = str(sampled_value)

            value = score_strategy(sampled, scenario)
            scored.append((value, strategy))

        scored.sort(key=lambda item: item[0], reverse=True)

        for rank, (value, strategy) in enumerate(scored, start=1):
            simulation_rows.append(
                {
                    "simulation_id": simulation_id,
                    "strategy_id": strategy["strategy_id"],
                    "strategy": strategy["strategy"],
                    "rank": rank,
                    "drr_value": round(value, 5),
                    "winner": scored[0][1]["strategy"],
                }
            )

    robustness_rows = []
    strategy_count = len(strategies)

    for strategy in strategies:
        subset = [row for row in simulation_rows if row["strategy_id"] == strategy["strategy_id"]]
        ranks = [int(row["rank"]) for row in subset]
        values = [float(row["drr_value"]) for row in subset]
        robustness_rows.append(
            {
                "strategy_id": strategy["strategy_id"],
                "strategy": strategy["strategy"],
                "mean_drr_value": round(mean(values), 5),
                "median_drr_value": round(median(values), 5),
                "probability_ranked_first": round(100 * sum(1 for r in ranks if r == 1) / n, 2),
                "probability_top_two": round(100 * sum(1 for r in ranks if r <= 2) / n, 2),
                "probability_bottom_two": round(100 * sum(1 for r in ranks if r >= strategy_count - 1) / n, 2),
            }
        )

    robustness_rows.sort(key=lambda row: row["probability_ranked_first"], reverse=True)
    return simulation_rows, robustness_rows


def main() -> None:
    strategies = read_csv(STRATEGIES_PATH)
    scenarios = read_csv(SCENARIOS_PATH)
    systems = read_csv(SYSTEMS_PATH)
    events = read_csv(EVENTS_PATH)

    strategy_profiles = []
    for row in strategies:
        value = base_drr_value(row)
        strategy_profiles.append(
            {
                "strategy_id": row["strategy_id"],
                "strategy": row["strategy"],
                "system_domain": row["system_domain"],
                "critical_function": row["critical_function"],
                "base_drr_value": round(value, 5),
                "justice_adjusted_value": round(value * (0.72 + 0.028 * f(row, "justice_protection")), 5),
                "hazard_reduction": row["hazard_reduction"],
                "exposure_reduction": row["exposure_reduction"],
                "vulnerability_reduction": row["vulnerability_reduction"],
                "capacity_enhancement": row["capacity_enhancement"],
                "justice_protection": row["justice_protection"],
                "maladaptation_risk": row["maladaptation_risk"],
                "diagnostic": strategy_diagnostic(row, value),
            }
        )

    rankings = scenario_rankings(strategies, scenarios)

    dynamic_rows = []
    for idx, system in enumerate(systems):
        dynamic_rows.extend(simulate_system_response(system, events, seed=100 + idx))

    dynamic_summary = summarize_simulation(dynamic_rows)

    baseline = next(s for s in scenarios if s["scenario"] == "Balanced")
    strategy_simulation, robustness_rows = strategy_monte_carlo(strategies, baseline, n=3000)

    first_place_summary: dict[str, int] = {}
    for row in rankings:
        if int(row["rank"]) == 1:
            first_place_summary[row["strategy"]] = first_place_summary.get(row["strategy"], 0) + 1

    top_rank_rows = [
        {"strategy": strategy, "times_ranked_first": count}
        for strategy, count in sorted(first_place_summary.items(), key=lambda item: item[1], reverse=True)
    ]

    write_csv(OUT_TABLES / "drr_resilience_strategy_profiles_standard.csv", strategy_profiles)
    write_csv(OUT_TABLES / "drr_resilience_strategy_rankings_standard.csv", rankings)
    write_csv(OUT_TABLES / "drr_resilience_top_rank_summary_standard.csv", top_rank_rows)
    write_csv(OUT_TABLES / "drr_resilience_dynamic_simulation_standard.csv", dynamic_rows)
    write_csv(OUT_TABLES / "drr_resilience_dynamic_summary_standard.csv", dynamic_summary)
    write_csv(OUT_TABLES / "drr_resilience_monte_carlo_standard.csv", strategy_simulation)
    write_csv(OUT_TABLES / "drr_resilience_robustness_summary_standard.csv", robustness_rows)
    write_csv(DATA_PROCESSED / "drr_resilience_strategy_profiles_standard.csv", strategy_profiles)

    print("DRR and resilience workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    print("Strategy diagnostics:")
    for row in strategy_profiles:
        print(
            f"  {row['strategy']}: value={row['base_drr_value']} "
            f"diagnostic={row['diagnostic']}"
        )
    print("System stress-response summary:")
    for row in dynamic_summary:
        print(
            f"  {row['system']}: mean justice-adjusted function="
            f"{row['mean_justice_adjusted_function']}, max dependency={row['maximum_dependency_coupling']}"
        )


if __name__ == "__main__":
    main()
