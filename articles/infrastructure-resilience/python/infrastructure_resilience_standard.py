#!/usr/bin/env python3
"""
Dependency-light Infrastructure Resilience workflow.

Reads synthetic strategy, scenario, infrastructure-system, and stress-event data.
Calculates infrastructure resilience rankings, equity-adjusted values,
cascade diagnostics, service-function simulations, and Monte Carlo robustness
using only the Python standard library.

Run:
    python3 python/infrastructure_resilience_standard.py
"""

from __future__ import annotations

import csv
import random
from pathlib import Path
from statistics import mean, median


ROOT = Path(__file__).resolve().parents[1]
STRATEGIES_PATH = ROOT / "data" / "raw" / "infrastructure_resilience_strategies.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "infrastructure_resilience_scenarios.csv"
SYSTEMS_PATH = ROOT / "data" / "raw" / "infrastructure_systems.csv"
EVENTS_PATH = ROOT / "data" / "raw" / "infrastructure_stress_events.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
DATA_PROCESSED = ROOT / "data" / "processed"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

BENEFIT_CRITERIA = [
    "service_continuity",
    "redundancy",
    "recovery_speed",
    "adaptive_capacity",
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
        0.22 * f(row, "service_continuity")
        + 0.20 * f(row, "redundancy")
        + 0.18 * f(row, "recovery_speed")
        + 0.16 * f(row, "adaptive_capacity")
        + 0.16 * f(row, "equity_protection")
        - 0.08 * f(row, "cascading_exposure")
    )


def score_strategy(row: dict[str, str], scenario: dict[str, str]) -> float:
    return (
        f(scenario, "service_continuity_weight") * f(row, "service_continuity")
        + f(scenario, "redundancy_weight") * f(row, "redundancy")
        + f(scenario, "recovery_speed_weight") * f(row, "recovery_speed")
        + f(scenario, "adaptive_capacity_weight") * f(row, "adaptive_capacity")
        + f(scenario, "equity_protection_weight") * f(row, "equity_protection")
        - f(scenario, "cascading_exposure_weight") * f(row, "cascading_exposure")
    )


def strategy_diagnostic(row: dict[str, str], value: float) -> str:
    if value >= 7.45 and f(row, "cascading_exposure") <= 3.6:
        return "strong infrastructure resilience profile with manageable cascade risk"
    if f(row, "cascading_exposure") >= 4.0:
        return "cascade review needed"
    if f(row, "equity_protection") < 7.8:
        return "equity protection needs strengthening"
    if f(row, "redundancy") < 7.8:
        return "redundancy constraint"
    if f(row, "adaptive_capacity") < 8.0:
        return "adaptive capacity constraint"
    return "promising but requires infrastructure scenario validation"


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
                    "cascading_exposure": strategy["cascading_exposure"],
                    "critical_service": strategy["critical_service"],
                }
            )
    return rows


def simulate_service_response(
    system: dict[str, str],
    events: list[dict[str, str]],
    seed: int,
    time_steps: int = 80,
) -> list[dict[str, object]]:
    rng = random.Random(seed)

    service_level = f(system, "baseline_service")
    redundancy = f(system, "redundancy_capacity")
    recovery = f(system, "recovery_capacity")
    adaptive = f(system, "adaptive_capacity")
    interdependence = f(system, "interdependence_coupling")
    equity_sensitivity = f(system, "equity_sensitivity")

    event_by_step = {12: events[0], 27: events[1], 42: events[2], 56: events[3], 70: events[4]}
    rows: list[dict[str, object]] = []

    for t in range(time_steps):
        event = event_by_step.get(t)

        if event:
            shock = f(event, "shock_intensity")
            chronic = f(event, "chronic_stress")
            compound = f(event, "compound_risk")
            cascade = f(event, "cascading_dependency")
            equity_burden = f(event, "equity_burden")
            event_name = event["event_name"]
        else:
            shock = 0.04 + rng.random() * 0.02
            chronic = 0.14 + 0.0028 * t
            compound = 0.10
            cascade = 0.12
            equity_burden = 0.20
            event_name = "background infrastructure stress"

        stress_load = (
            0.34 * shock
            + 0.18 * chronic
            + 0.18 * compound
            + 0.18 * cascade
            + 0.12 * interdependence
        )

        response_capacity = (
            0.33 * redundancy
            + 0.30 * recovery
            + 0.24 * adaptive
            - 0.20 * f(system, "shock_exposure")
            - 0.12 * f(system, "chronic_stress")
            - 0.16 * interdependence
        )
        response_capacity = max(0.0, min(1.0, response_capacity))

        service_level = (
            service_level
            - 0.32 * stress_load
            + 0.20 * response_capacity
            + 0.12 * recovery
            + 0.08 * adaptive
            - 0.08 * interdependence
        )
        service_level = max(0.0, min(1.0, service_level))

        interdependence = max(0.0, min(1.0, interdependence + 0.020 * stress_load - 0.012 * response_capacity))
        equity_adjusted_service = service_level * (0.72 + 0.28 * (1.0 - equity_burden + equity_sensitivity * 0.40))
        equity_adjusted_service = max(0.0, min(1.0, equity_adjusted_service))

        rows.append(
            {
                "system_id": system["system_id"],
                "system": system["system"],
                "system_domain": system["system_domain"],
                "time": t,
                "event": event_name,
                "stress_load": round(stress_load, 5),
                "response_capacity": round(response_capacity, 5),
                "service_level": round(service_level, 5),
                "interdependence_coupling": round(interdependence, 5),
                "equity_adjusted_service": round(equity_adjusted_service, 5),
            }
        )

    return rows


def summarize_simulation(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    systems = sorted(set(str(row["system"]) for row in rows))
    summary: list[dict[str, object]] = []

    for system in systems:
        subset = [row for row in rows if row["system"] == system]
        service = [float(row["service_level"]) for row in subset]
        equity = [float(row["equity_adjusted_service"]) for row in subset]
        interdependence = [float(row["interdependence_coupling"]) for row in subset]

        summary.append(
            {
                "system": system,
                "mean_service_level": round(mean(service), 5),
                "minimum_service_level": round(min(service), 5),
                "final_service_level": round(service[-1], 5),
                "mean_equity_adjusted_service": round(mean(equity), 5),
                "maximum_interdependence_coupling": round(max(interdependence), 5),
                "final_interdependence_coupling": round(interdependence[-1], 5),
            }
        )

    summary.sort(key=lambda row: row["mean_equity_adjusted_service"], reverse=True)
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

            for criterion in BENEFIT_CRITERIA + ["cascading_exposure"]:
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
                "critical_service": row["critical_service"],
                "base_resilience_value": round(value, 5),
                "equity_adjusted_value": round(value * (0.72 + 0.028 * f(row, "equity_protection")), 5),
                "service_continuity": row["service_continuity"],
                "redundancy": row["redundancy"],
                "recovery_speed": row["recovery_speed"],
                "adaptive_capacity": row["adaptive_capacity"],
                "equity_protection": row["equity_protection"],
                "cascading_exposure": row["cascading_exposure"],
                "diagnostic": strategy_diagnostic(row, value),
            }
        )

    rankings = scenario_rankings(strategies, scenarios)

    dynamic_rows = []
    for idx, system in enumerate(systems):
        dynamic_rows.extend(simulate_service_response(system, events, seed=100 + idx))

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

    write_csv(OUT_TABLES / "infrastructure_resilience_strategy_profiles_standard.csv", strategy_profiles)
    write_csv(OUT_TABLES / "infrastructure_resilience_strategy_rankings_standard.csv", rankings)
    write_csv(OUT_TABLES / "infrastructure_resilience_top_rank_summary_standard.csv", top_rank_rows)
    write_csv(OUT_TABLES / "infrastructure_service_dynamic_simulation_standard.csv", dynamic_rows)
    write_csv(OUT_TABLES / "infrastructure_service_dynamic_summary_standard.csv", dynamic_summary)
    write_csv(OUT_TABLES / "infrastructure_resilience_monte_carlo_standard.csv", strategy_simulation)
    write_csv(OUT_TABLES / "infrastructure_resilience_robustness_summary_standard.csv", robustness_rows)
    write_csv(DATA_PROCESSED / "infrastructure_resilience_strategy_profiles_standard.csv", strategy_profiles)

    print("Infrastructure resilience workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    print("Strategy diagnostics:")
    for row in strategy_profiles:
        print(
            f"  {row['strategy']}: value={row['base_resilience_value']} "
            f"diagnostic={row['diagnostic']}"
        )
    print("Service stress-response summary:")
    for row in dynamic_summary:
        print(
            f"  {row['system']}: mean equity-adjusted service="
            f"{row['mean_equity_adjusted_service']}, max interdependence={row['maximum_interdependence_coupling']}"
        )


if __name__ == "__main__":
    main()
