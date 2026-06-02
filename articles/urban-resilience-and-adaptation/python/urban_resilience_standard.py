#!/usr/bin/env python3
"""
Dependency-light Urban Resilience workflow.

Reads synthetic strategy, scenario, urban-system, and stress-event data.
Calculates resilience rankings, equity-adjusted values, maladaptation diagnostics,
urban stress-response simulations, and Monte Carlo robustness using only
the Python standard library.

Run:
    python3 python/urban_resilience_standard.py
"""

from __future__ import annotations

import csv
import random
from pathlib import Path
from statistics import mean, median


ROOT = Path(__file__).resolve().parents[1]
STRATEGIES_PATH = ROOT / "data" / "raw" / "urban_resilience_strategies.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "urban_resilience_scenarios.csv"
SYSTEMS_PATH = ROOT / "data" / "raw" / "urban_systems.csv"
EVENTS_PATH = ROOT / "data" / "raw" / "urban_stress_events.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
DATA_PROCESSED = ROOT / "data" / "processed"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

BENEFIT_CRITERIA = [
    "exposure_reduction",
    "vulnerability_reduction",
    "service_continuity",
    "adaptive_capacity",
    "ecological_buffering",
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
        0.16 * f(row, "exposure_reduction")
        + 0.17 * f(row, "vulnerability_reduction")
        + 0.17 * f(row, "service_continuity")
        + 0.15 * f(row, "adaptive_capacity")
        + 0.14 * f(row, "ecological_buffering")
        + 0.15 * f(row, "equity_protection")
        - 0.06 * f(row, "maladaptation_risk")
    )


def score_strategy(row: dict[str, str], scenario: dict[str, str]) -> float:
    return (
        f(scenario, "exposure_reduction_weight") * f(row, "exposure_reduction")
        + f(scenario, "vulnerability_reduction_weight") * f(row, "vulnerability_reduction")
        + f(scenario, "service_continuity_weight") * f(row, "service_continuity")
        + f(scenario, "adaptive_capacity_weight") * f(row, "adaptive_capacity")
        + f(scenario, "ecological_buffering_weight") * f(row, "ecological_buffering")
        + f(scenario, "equity_protection_weight") * f(row, "equity_protection")
        - f(scenario, "maladaptation_risk_weight") * f(row, "maladaptation_risk")
    )


def strategy_diagnostic(row: dict[str, str], value: float) -> str:
    if value >= 7.75 and f(row, "maladaptation_risk") <= 2.7:
        return "strong urban resilience profile with manageable maladaptation risk"
    if f(row, "maladaptation_risk") >= 3.4:
        return "maladaptation review needed"
    if f(row, "equity_protection") < 8.0:
        return "equity protection needs strengthening"
    if f(row, "ecological_buffering") < 7.5:
        return "ecological buffering needs strengthening"
    if f(row, "service_continuity") < 8.0:
        return "service continuity needs strengthening"
    return "promising but requires urban scenario validation"


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
                    "resilience_value": round(value, 5),
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
    infrastructure = f(system, "infrastructure_support")
    community = f(system, "community_capacity")
    ecology = f(system, "ecological_condition")
    adaptive = f(system, "adaptive_capacity")
    dependency = f(system, "dependency_coupling")
    equity_sensitivity = f(system, "equity_sensitivity")

    event_by_step = {12: events[0], 27: events[1], 42: events[2], 56: events[3], 70: events[4]}
    rows: list[dict[str, object]] = []

    for t in range(time_steps):
        event = event_by_step.get(t)

        if event:
            hazard = f(event, "hazard_intensity")
            infra_disruption = f(event, "infrastructure_disruption")
            health = f(event, "health_burden")
            housing = f(event, "housing_stress")
            market = f(event, "market_stress")
            equity_burden = f(event, "equity_burden")
            dependency_amplification = f(event, "dependency_amplification")
            event_name = event["event_name"]
        else:
            hazard = 0.05 + rng.random() * 0.02
            infra_disruption = 0.10
            health = 0.12 + rng.random() * 0.02
            housing = 0.14 + 0.0025 * t
            market = 0.12
            equity_burden = 0.22
            dependency_amplification = 0.14
            event_name = "background urban stress"

        stress_load = (
            0.25 * hazard
            + 0.19 * infra_disruption
            + 0.17 * health
            + 0.17 * housing
            + 0.10 * market
            + 0.12 * dependency_amplification
            + 0.10 * dependency
        )

        response_capacity = (
            0.26 * infrastructure
            + 0.24 * community
            + 0.20 * ecology
            + 0.24 * adaptive
            - 0.18 * f(system, "hazard_exposure")
            - 0.12 * f(system, "chronic_stress")
            - 0.12 * dependency
        )
        response_capacity = max(0.0, min(1.0, response_capacity))

        function_level = (
            function_level
            - 0.32 * stress_load
            + 0.18 * response_capacity
            + 0.10 * infrastructure
            + 0.09 * community
            + 0.08 * ecology
            + 0.08 * adaptive
            - 0.06 * dependency
        )
        function_level = max(0.0, min(1.0, function_level))

        dependency = max(0.0, min(1.0, dependency + 0.020 * stress_load - 0.011 * response_capacity))
        equity_adjusted_function = function_level * (0.72 + 0.28 * (1.0 - equity_burden + equity_sensitivity * 0.40))
        equity_adjusted_function = max(0.0, min(1.0, equity_adjusted_function))

        rows.append(
            {
                "system_id": system["system_id"],
                "system": system["system"],
                "system_domain": system["system_domain"],
                "time": t,
                "event": event_name,
                "stress_load": round(stress_load, 5),
                "response_capacity": round(response_capacity, 5),
                "urban_function": round(function_level, 5),
                "dependency_coupling": round(dependency, 5),
                "equity_adjusted_function": round(equity_adjusted_function, 5),
            }
        )

    return rows


def summarize_simulation(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    systems = sorted(set(str(row["system"]) for row in rows))
    summary: list[dict[str, object]] = []

    for system in systems:
        subset = [row for row in rows if row["system"] == system]
        function_values = [float(row["urban_function"]) for row in subset]
        equity = [float(row["equity_adjusted_function"]) for row in subset]
        dependency = [float(row["dependency_coupling"]) for row in subset]

        summary.append(
            {
                "system": system,
                "mean_urban_function": round(mean(function_values), 5),
                "minimum_urban_function": round(min(function_values), 5),
                "final_urban_function": round(function_values[-1], 5),
                "mean_equity_adjusted_function": round(mean(equity), 5),
                "maximum_dependency_coupling": round(max(dependency), 5),
                "final_dependency_coupling": round(dependency[-1], 5),
            }
        )

    summary.sort(key=lambda row: row["mean_equity_adjusted_function"], reverse=True)
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
                    "resilience_value": round(value, 5),
                    "winner": scored[0][1]["strategy"],
                }
            )

    robustness_rows = []
    strategy_count = len(strategies)

    for strategy in strategies:
        subset = [row for row in simulation_rows if row["strategy_id"] == strategy["strategy_id"]]
        ranks = [int(row["rank"]) for row in subset]
        values = [float(row["resilience_value"]) for row in subset]
        robustness_rows.append(
            {
                "strategy_id": strategy["strategy_id"],
                "strategy": strategy["strategy"],
                "mean_resilience_value": round(mean(values), 5),
                "median_resilience_value": round(median(values), 5),
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
        value = base_resilience_value(row)
        strategy_profiles.append(
            {
                "strategy_id": row["strategy_id"],
                "strategy": row["strategy"],
                "system_domain": row["system_domain"],
                "critical_function": row["critical_function"],
                "base_resilience_value": round(value, 5),
                "equity_adjusted_value": round(value * (0.72 + 0.028 * f(row, "equity_protection")), 5),
                "exposure_reduction": row["exposure_reduction"],
                "vulnerability_reduction": row["vulnerability_reduction"],
                "service_continuity": row["service_continuity"],
                "adaptive_capacity": row["adaptive_capacity"],
                "ecological_buffering": row["ecological_buffering"],
                "equity_protection": row["equity_protection"],
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

    write_csv(OUT_TABLES / "urban_resilience_strategy_profiles_standard.csv", strategy_profiles)
    write_csv(OUT_TABLES / "urban_resilience_strategy_rankings_standard.csv", rankings)
    write_csv(OUT_TABLES / "urban_resilience_top_rank_summary_standard.csv", top_rank_rows)
    write_csv(OUT_TABLES / "urban_dynamic_simulation_standard.csv", dynamic_rows)
    write_csv(OUT_TABLES / "urban_dynamic_summary_standard.csv", dynamic_summary)
    write_csv(OUT_TABLES / "urban_resilience_monte_carlo_standard.csv", strategy_simulation)
    write_csv(OUT_TABLES / "urban_resilience_robustness_summary_standard.csv", robustness_rows)
    write_csv(DATA_PROCESSED / "urban_resilience_strategy_profiles_standard.csv", strategy_profiles)

    print("Urban resilience workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    print("Strategy diagnostics:")
    for row in strategy_profiles:
        print(
            f"  {row['strategy']}: value={row['base_resilience_value']} "
            f"diagnostic={row['diagnostic']}"
        )
    print("Urban system stress-response summary:")
    for row in dynamic_summary:
        print(
            f"  {row['system']}: mean equity-adjusted function="
            f"{row['mean_equity_adjusted_function']}, max dependency={row['maximum_dependency_coupling']}"
        )


if __name__ == "__main__":
    main()
