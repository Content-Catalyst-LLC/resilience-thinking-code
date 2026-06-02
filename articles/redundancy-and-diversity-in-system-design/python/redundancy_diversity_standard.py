#!/usr/bin/env python3
"""
Dependency-light redundancy and diversity workflow.

Reads synthetic strategy and scenario data, calculates resilience design
rankings, common-mode diagnostics, and Monte Carlo robustness using only
the Python standard library.

Run:
    python3 python/redundancy_diversity_standard.py
"""

from __future__ import annotations

import csv
import random
from pathlib import Path
from statistics import mean, median


ROOT = Path(__file__).resolve().parents[1]
STRATEGIES_PATH = ROOT / "data" / "raw" / "redundancy_diversity_strategies.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "redundancy_diversity_scenarios.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
DATA_PROCESSED = ROOT / "data" / "processed"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

BENEFIT_CRITERIA = [
    "redundancy",
    "diversity",
    "response_diversity",
    "coordination_capacity",
    "justice_contribution",
    "maintenance_reliability",
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
        0.22 * f(row, "redundancy")
        + 0.18 * f(row, "diversity")
        + 0.22 * f(row, "response_diversity")
        + 0.13 * f(row, "coordination_capacity")
        + 0.10 * f(row, "justice_contribution")
        + 0.07 * f(row, "maintenance_reliability")
        - 0.08 * f(row, "common_mode_risk")
    )


def score_strategy(row: dict[str, str], scenario: dict[str, str]) -> float:
    return (
        f(scenario, "redundancy_weight") * f(row, "redundancy")
        + f(scenario, "diversity_weight") * f(row, "diversity")
        + f(scenario, "response_diversity_weight") * f(row, "response_diversity")
        + f(scenario, "coordination_capacity_weight") * f(row, "coordination_capacity")
        + f(scenario, "justice_contribution_weight") * f(row, "justice_contribution")
        + f(scenario, "maintenance_reliability_weight") * f(row, "maintenance_reliability")
        - f(scenario, "common_mode_risk_weight") * f(row, "common_mode_risk")
    )


def diagnostic(row: dict[str, str], value: float) -> str:
    if value >= 7.25 and f(row, "common_mode_risk") <= 3.7:
        return "strong diverse-redundancy profile with manageable common-mode risk"
    if f(row, "common_mode_risk") >= 4.0:
        return "common-mode failure review needed"
    if f(row, "coordination_capacity") < 7.5:
        return "coordination and interoperability constraint"
    if f(row, "justice_contribution") < 7.6:
        return "justice contribution needs stronger design"
    if f(row, "maintenance_reliability") < 7.4:
        return "maintenance reliability needs stronger evidence"
    return "promising but requires stress testing and validation"


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
                    "resilience_value": round(value, 5),
                    "common_mode_risk": strategy["common_mode_risk"],
                    "critical_function": strategy["critical_function"],
                }
            )
    return rows


def monte_carlo(
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
            for criterion in BENEFIT_CRITERIA + ["common_mode_risk"]:
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

    summary_rows = []
    strategy_count = len(strategies)

    for strategy in strategies:
        subset = [row for row in simulation_rows if row["strategy_id"] == strategy["strategy_id"]]
        ranks = [int(row["rank"]) for row in subset]
        values = [float(row["resilience_value"]) for row in subset]
        summary_rows.append(
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

    summary_rows.sort(key=lambda row: row["probability_ranked_first"], reverse=True)
    return simulation_rows, summary_rows


def main() -> None:
    strategies = read_csv(STRATEGIES_PATH)
    scenarios = read_csv(SCENARIOS_PATH)

    profile_rows = []
    for row in strategies:
        value = base_resilience_value(row)
        profile_rows.append(
            {
                "strategy_id": row["strategy_id"],
                "strategy": row["strategy"],
                "system_domain": row["system_domain"],
                "critical_function": row["critical_function"],
                "base_resilience_value": round(value, 5),
                "redundancy": row["redundancy"],
                "diversity": row["diversity"],
                "response_diversity": row["response_diversity"],
                "coordination_capacity": row["coordination_capacity"],
                "justice_contribution": row["justice_contribution"],
                "maintenance_reliability": row["maintenance_reliability"],
                "common_mode_risk": row["common_mode_risk"],
                "diagnostic": diagnostic(row, value),
            }
        )

    rankings = scenario_rankings(strategies, scenarios)
    baseline = next(s for s in scenarios if s["scenario"] == "Balanced")
    simulation_rows, robustness_rows = monte_carlo(strategies, baseline, n=3000)

    first_place_summary: dict[str, int] = {}
    for row in rankings:
        if int(row["rank"]) == 1:
            first_place_summary[row["strategy"]] = first_place_summary.get(row["strategy"], 0) + 1

    top_rank_rows = [
        {"strategy": strategy, "times_ranked_first": count}
        for strategy, count in sorted(first_place_summary.items(), key=lambda item: item[1], reverse=True)
    ]

    write_csv(OUT_TABLES / "redundancy_diversity_profiles_standard.csv", profile_rows)
    write_csv(OUT_TABLES / "redundancy_diversity_rankings_standard.csv", rankings)
    write_csv(OUT_TABLES / "redundancy_diversity_top_rank_summary_standard.csv", top_rank_rows)
    write_csv(OUT_TABLES / "redundancy_diversity_monte_carlo_standard.csv", simulation_rows)
    write_csv(OUT_TABLES / "redundancy_diversity_robustness_summary_standard.csv", robustness_rows)
    write_csv(DATA_PROCESSED / "redundancy_diversity_profiles_standard.csv", profile_rows)

    print("Redundancy and diversity workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    for row in profile_rows:
        print(
            f"  {row['strategy']}: value={row['base_resilience_value']} "
            f"diagnostic={row['diagnostic']}"
        )


if __name__ == "__main__":
    main()
