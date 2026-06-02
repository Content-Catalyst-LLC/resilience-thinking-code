#!/usr/bin/env python3
"""
Dependency-light learning, memory, and adaptive management workflow.

Reads synthetic strategy, scenario, profile, and learning-event data.
Calculates adaptive-learning strategy rankings, event diagnostics,
memory dynamics, justice-weighted adaptive response, and Monte Carlo
robustness using only the Python standard library.

Run:
    python3 python/learning_memory_standard.py
"""

from __future__ import annotations

import csv
import random
from pathlib import Path
from statistics import mean, median


ROOT = Path(__file__).resolve().parents[1]
STRATEGIES_PATH = ROOT / "data" / "raw" / "adaptive_management_strategies.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "adaptive_management_scenarios.csv"
PROFILES_PATH = ROOT / "data" / "raw" / "adaptive_management_profiles.csv"
EVENTS_PATH = ROOT / "data" / "raw" / "learning_memory_events.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
DATA_PROCESSED = ROOT / "data" / "processed"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

BENEFIT_CRITERIA = [
    "monitoring_quality",
    "memory_retention",
    "feedback_use",
    "governance_flexibility",
    "community_knowledge",
    "justice_protection",
    "implementation_reliability",
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


def base_adaptive_value(row: dict[str, str]) -> float:
    return (
        0.15 * f(row, "monitoring_quality")
        + 0.15 * f(row, "memory_retention")
        + 0.17 * f(row, "feedback_use")
        + 0.14 * f(row, "governance_flexibility")
        + 0.12 * f(row, "community_knowledge")
        + 0.11 * f(row, "justice_protection")
        + 0.09 * f(row, "implementation_reliability")
        - 0.07 * f(row, "forgetting_pressure")
    )


def score_strategy(row: dict[str, str], scenario: dict[str, str]) -> float:
    return (
        f(scenario, "monitoring_quality_weight") * f(row, "monitoring_quality")
        + f(scenario, "memory_retention_weight") * f(row, "memory_retention")
        + f(scenario, "feedback_use_weight") * f(row, "feedback_use")
        + f(scenario, "governance_flexibility_weight") * f(row, "governance_flexibility")
        + f(scenario, "community_knowledge_weight") * f(row, "community_knowledge")
        + f(scenario, "justice_protection_weight") * f(row, "justice_protection")
        + f(scenario, "implementation_reliability_weight") * f(row, "implementation_reliability")
        - f(scenario, "forgetting_pressure_weight") * f(row, "forgetting_pressure")
    )


def strategy_diagnostic(row: dict[str, str], value: float) -> str:
    if value >= 7.2 and f(row, "forgetting_pressure") <= 3.1:
        return "strong adaptive-learning profile with manageable forgetting pressure"
    if f(row, "forgetting_pressure") >= 3.5:
        return "forgetting-pressure review needed"
    if f(row, "feedback_use") < 8.0:
        return "feedback-use constraint"
    if f(row, "justice_protection") < 7.5:
        return "justice protection needs strengthening"
    return "promising but requires implementation and governance validation"


def event_diagnostic(row: dict[str, str]) -> dict[str, object]:
    lesson_score = (
        0.20 * f(row, "monitoring_signal")
        + 0.22 * f(row, "lesson_capture")
        + 0.20 * f(row, "implementation_followthrough")
        + 0.18 * f(row, "community_input")
        + 0.14 * f(row, "justice_visibility")
        - 0.06 * f(row, "memory_loss_risk")
    )
    justice_weighted_learning = lesson_score * (0.70 + 0.30 * f(row, "justice_visibility"))

    if f(row, "implementation_followthrough") < 0.58:
        diagnostic = "lesson capture may not become institutional change"
    elif f(row, "community_input") < 0.55:
        diagnostic = "community knowledge integration is weak"
    elif f(row, "memory_loss_risk") > 0.44:
        diagnostic = "memory-loss risk threatens learning continuity"
    else:
        diagnostic = "moderate to strong learning signal"

    return {
        "event_id": row["event_id"],
        "event_name": row["event_name"],
        "system_domain": row["system_domain"],
        "disturbance_intensity": row["disturbance_intensity"],
        "lesson_score": round(lesson_score, 5),
        "justice_weighted_learning": round(justice_weighted_learning, 5),
        "diagnostic": diagnostic,
    }


def simulate_profile(row: dict[str, str], seed: int, time_steps: int = 80) -> list[dict[str, object]]:
    rng = random.Random(seed)
    function_level = 0.88
    memory = f(row, "memory_retention")
    adaptive_capacity = 0.55

    rows: list[dict[str, object]] = []
    shock_schedule = {15: 0.35, 32: 0.22, 50: 0.40, 67: 0.28}

    for t in range(time_steps):
        shock = shock_schedule.get(t, 0.04)

        monitoring_signal = max(
            0.0,
            min(1.0, f(row, "monitoring_quality") * shock + rng.gauss(0.0, 0.015)),
        )

        learning = (
            f(row, "learning_rate")
            * monitoring_signal
            * f(row, "feedback_use")
            * f(row, "governance_capacity")
        )

        memory = (
            f(row, "memory_retention") * memory
            + learning
            - 0.05 * f(row, "forgetting_pressure")
        )
        memory = max(0.0, min(1.0, memory))

        adaptive_capacity = (
            0.82 * adaptive_capacity
            + 0.12 * memory
            + 0.10 * f(row, "governance_capacity")
            - 0.06 * f(row, "forgetting_pressure")
        )
        adaptive_capacity = max(0.0, min(1.0, adaptive_capacity))

        function_level = (
            function_level
            - 0.42 * shock
            + 0.24 * adaptive_capacity
            + 0.10 * memory
            - 0.05 * f(row, "forgetting_pressure")
        )
        function_level = max(0.0, min(1.0, function_level))

        justice_adjusted_function = function_level * (0.75 + 0.25 * f(row, "justice_sensitivity"))

        rows.append(
            {
                "profile_id": row["profile_id"],
                "profile": row["profile"],
                "time": t,
                "disturbance": round(shock, 5),
                "monitoring_signal": round(monitoring_signal, 5),
                "learning": round(learning, 5),
                "memory": round(memory, 5),
                "adaptive_capacity": round(adaptive_capacity, 5),
                "function_level": round(function_level, 5),
                "justice_adjusted_function": round(justice_adjusted_function, 5),
            }
        )

    return rows


def simulation_summary(sim_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    profiles = sorted(set(str(row["profile"]) for row in sim_rows))
    summary_rows: list[dict[str, object]] = []

    for profile in profiles:
        subset = [row for row in sim_rows if row["profile"] == profile]
        functions = [float(row["function_level"]) for row in subset]
        memories = [float(row["memory"]) for row in subset]
        adaptive = [float(row["adaptive_capacity"]) for row in subset]
        justice = [float(row["justice_adjusted_function"]) for row in subset]

        summary_rows.append(
            {
                "profile": profile,
                "mean_function": round(mean(functions), 5),
                "min_function": round(min(functions), 5),
                "final_function": round(functions[-1], 5),
                "mean_memory": round(mean(memories), 5),
                "final_memory": round(memories[-1], 5),
                "mean_adaptive_capacity": round(mean(adaptive), 5),
                "mean_justice_adjusted_function": round(mean(justice), 5),
            }
        )

    summary_rows.sort(key=lambda row: row["mean_justice_adjusted_function"], reverse=True)
    return summary_rows


def scenario_rankings(strategies: list[dict[str, str]], scenarios: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
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
                    "adaptive_learning_value": round(value, 5),
                    "forgetting_pressure": strategy["forgetting_pressure"],
                    "critical_function": strategy["critical_function"],
                }
            )
    return rows


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

            for criterion in BENEFIT_CRITERIA + ["forgetting_pressure"]:
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
                    "adaptive_learning_value": round(value, 5),
                    "winner": scored[0][1]["strategy"],
                }
            )

    robustness_rows = []
    strategy_count = len(strategies)

    for strategy in strategies:
        subset = [row for row in simulation_rows if row["strategy_id"] == strategy["strategy_id"]]
        ranks = [int(row["rank"]) for row in subset]
        values = [float(row["adaptive_learning_value"]) for row in subset]
        robustness_rows.append(
            {
                "strategy_id": strategy["strategy_id"],
                "strategy": strategy["strategy"],
                "mean_adaptive_learning_value": round(mean(values), 5),
                "median_adaptive_learning_value": round(median(values), 5),
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
    profiles = read_csv(PROFILES_PATH)
    events = read_csv(EVENTS_PATH)

    profile_rows = []
    for row in strategies:
        value = base_adaptive_value(row)
        profile_rows.append(
            {
                "strategy_id": row["strategy_id"],
                "strategy": row["strategy"],
                "system_domain": row["system_domain"],
                "critical_function": row["critical_function"],
                "base_adaptive_learning_value": round(value, 5),
                "monitoring_quality": row["monitoring_quality"],
                "memory_retention": row["memory_retention"],
                "feedback_use": row["feedback_use"],
                "governance_flexibility": row["governance_flexibility"],
                "community_knowledge": row["community_knowledge"],
                "justice_protection": row["justice_protection"],
                "implementation_reliability": row["implementation_reliability"],
                "forgetting_pressure": row["forgetting_pressure"],
                "diagnostic": strategy_diagnostic(row, value),
            }
        )

    event_rows = [event_diagnostic(row) for row in events]
    dynamic_rows = []
    for idx, row in enumerate(profiles):
        dynamic_rows.extend(simulate_profile(row, seed=42 + idx))

    dynamic_summary = simulation_summary(dynamic_rows)
    rankings = scenario_rankings(strategies, scenarios)
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

    write_csv(OUT_TABLES / "adaptive_management_strategy_profiles_standard.csv", profile_rows)
    write_csv(OUT_TABLES / "learning_memory_event_diagnostics_standard.csv", event_rows)
    write_csv(OUT_TABLES / "learning_memory_dynamic_simulation_standard.csv", dynamic_rows)
    write_csv(OUT_TABLES / "learning_memory_dynamic_summary_standard.csv", dynamic_summary)
    write_csv(OUT_TABLES / "adaptive_management_strategy_rankings_standard.csv", rankings)
    write_csv(OUT_TABLES / "adaptive_management_top_rank_summary_standard.csv", top_rank_rows)
    write_csv(OUT_TABLES / "adaptive_management_monte_carlo_standard.csv", strategy_simulation)
    write_csv(OUT_TABLES / "adaptive_management_robustness_summary_standard.csv", robustness_rows)
    write_csv(DATA_PROCESSED / "adaptive_management_strategy_profiles_standard.csv", profile_rows)

    print("Learning, memory, and adaptive management workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    print("Dynamic learning profiles:")
    for row in dynamic_summary:
        print(
            f"  {row['profile']}: mean function={row['mean_function']}, "
            f"final memory={row['final_memory']}"
        )
    print("Strategy diagnostics:")
    for row in profile_rows:
        print(
            f"  {row['strategy']}: value={row['base_adaptive_learning_value']} "
            f"diagnostic={row['diagnostic']}"
        )


if __name__ == "__main__":
    main()
