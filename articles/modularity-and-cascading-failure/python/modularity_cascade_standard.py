#!/usr/bin/env python3
"""
Dependency-light modularity and cascading failure workflow.

Reads synthetic node, edge, strategy, and scenario data. Runs deterministic
and Monte Carlo cascade simulations using only the Python standard library.
Exports cascade summaries, justice-weighted impacts, containment strategy
rankings, and robustness summaries.

Run:
    python3 python/modularity_cascade_standard.py
"""

from __future__ import annotations

import csv
import random
from pathlib import Path
from statistics import mean, median


ROOT = Path(__file__).resolve().parents[1]
NODES_PATH = ROOT / "data" / "raw" / "cascade_nodes.csv"
EDGES_PATH = ROOT / "data" / "raw" / "cascade_edges.csv"
STRATEGIES_PATH = ROOT / "data" / "raw" / "containment_strategies.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "containment_scenarios.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
DATA_PROCESSED = ROOT / "data" / "processed"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

BENEFIT_CRITERIA = [
    "modularity",
    "redundancy",
    "dependency_mapping",
    "isolation_capacity",
    "coordination_readiness",
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


def base_containment_value(row: dict[str, str]) -> float:
    return (
        0.18 * f(row, "modularity")
        + 0.16 * f(row, "redundancy")
        + 0.16 * f(row, "dependency_mapping")
        + 0.18 * f(row, "isolation_capacity")
        + 0.14 * f(row, "coordination_readiness")
        + 0.10 * f(row, "justice_protection")
        - 0.08 * f(row, "common_mode_risk")
    )


def score_strategy(row: dict[str, str], scenario: dict[str, str]) -> float:
    return (
        f(scenario, "modularity_weight") * f(row, "modularity")
        + f(scenario, "redundancy_weight") * f(row, "redundancy")
        + f(scenario, "dependency_mapping_weight") * f(row, "dependency_mapping")
        + f(scenario, "isolation_capacity_weight") * f(row, "isolation_capacity")
        + f(scenario, "coordination_readiness_weight") * f(row, "coordination_readiness")
        + f(scenario, "justice_protection_weight") * f(row, "justice_protection")
        - f(scenario, "common_mode_risk_weight") * f(row, "common_mode_risk")
    )


def strategy_diagnostic(row: dict[str, str], value: float) -> str:
    if value >= 7.15 and f(row, "common_mode_risk") <= 3.6:
        return "strong containment profile with manageable common-mode risk"
    if f(row, "common_mode_risk") >= 4.0:
        return "common-mode failure review needed"
    if f(row, "coordination_readiness") < 7.5:
        return "coordination readiness constraint"
    if f(row, "justice_protection") < 7.5:
        return "justice protection needs strengthening"
    return "promising but requires stress testing and dependency validation"


def simulate_cascade(
    initial_failure: str,
    nodes_by_name: dict[str, dict[str, str]],
    outgoing_edges: dict[str, list[dict[str, str]]],
    seed: int,
    max_steps: int = 7,
) -> list[dict[str, object]]:
    rng = random.Random(seed)
    failed: set[str] = {initial_failure}
    rows: list[dict[str, object]] = []

    for step in range(max_steps):
        new_failures: set[str] = set()

        for source in list(failed):
            for edge in outgoing_edges.get(source, []):
                target = edge["target"]

                if target in failed:
                    continue

                target_node = nodes_by_name[target]
                propagation_probability = (
                    float(edge["coupling_strength"])
                    + 0.35 * f(target_node, "common_mode_exposure")
                    - 0.30 * f(target_node, "redundancy")
                    - 0.25 * f(target_node, "isolation_capacity")
                )
                propagation_probability = max(0.02, min(0.95, propagation_probability))

                if rng.random() < propagation_probability:
                    new_failures.add(target)

        failed.update(new_failures)

        rows.append(
            {
                "initial_failure": initial_failure,
                "step": step,
                "new_failures": len(new_failures),
                "total_failures": len(failed),
                "failed_nodes": "; ".join(sorted(failed)),
            }
        )

        if not new_failures:
            break

    return rows


def cascade_monte_carlo(
    nodes: list[dict[str, str]],
    edges: list[dict[str, str]],
    n: int = 2000,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    nodes_by_name = {row["node"]: row for row in nodes}
    outgoing_edges: dict[str, list[dict[str, str]]] = {}

    for edge in edges:
        outgoing_edges.setdefault(edge["source"], []).append(edge)

    simulation_rows: list[dict[str, object]] = []

    for node in nodes:
        initial = node["node"]
        for simulation_id in range(n):
            timeline = simulate_cascade(
                initial_failure=initial,
                nodes_by_name=nodes_by_name,
                outgoing_edges=outgoing_edges,
                seed=simulation_id + 1000 * int(node["node_id"][1:]),
            )
            final = timeline[-1]
            failed_nodes = [name.strip() for name in str(final["failed_nodes"]).split(";")]
            justice_weighted_impact = sum(f(nodes_by_name[name], "justice_sensitivity") for name in failed_nodes)

            simulation_rows.append(
                {
                    "initial_failure": initial,
                    "simulation_id": simulation_id,
                    "final_failures": final["total_failures"],
                    "cascade_steps": final["step"] + 1,
                    "justice_weighted_impact": round(justice_weighted_impact, 5),
                    "failed_nodes": final["failed_nodes"],
                }
            )

    summary_rows: list[dict[str, object]] = []

    for node in nodes:
        initial = node["node"]
        subset = [row for row in simulation_rows if row["initial_failure"] == initial]
        failures = [int(row["final_failures"]) for row in subset]
        impacts = [float(row["justice_weighted_impact"]) for row in subset]
        large_cascade_probability = 100 * sum(1 for value in failures if value >= 5) / n

        summary_rows.append(
            {
                "initial_failure": initial,
                "system_domain": node["system_domain"],
                "critical_function": node["critical_function"],
                "mean_final_failures": round(mean(failures), 5),
                "median_final_failures": round(median(failures), 5),
                "probability_large_cascade": round(large_cascade_probability, 2),
                "mean_justice_weighted_impact": round(mean(impacts), 5),
                "max_justice_weighted_impact": round(max(impacts), 5),
            }
        )

    summary_rows.sort(key=lambda row: row["probability_large_cascade"], reverse=True)
    return simulation_rows, summary_rows


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
                    "containment_value": round(value, 5),
                    "common_mode_risk": strategy["common_mode_risk"],
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
                    "containment_value": round(value, 5),
                    "winner": scored[0][1]["strategy"],
                }
            )

    robustness_rows = []
    strategy_count = len(strategies)

    for strategy in strategies:
        subset = [row for row in simulation_rows if row["strategy_id"] == strategy["strategy_id"]]
        ranks = [int(row["rank"]) for row in subset]
        values = [float(row["containment_value"]) for row in subset]
        robustness_rows.append(
            {
                "strategy_id": strategy["strategy_id"],
                "strategy": strategy["strategy"],
                "mean_containment_value": round(mean(values), 5),
                "median_containment_value": round(median(values), 5),
                "probability_ranked_first": round(100 * sum(1 for r in ranks if r == 1) / n, 2),
                "probability_top_two": round(100 * sum(1 for r in ranks if r <= 2) / n, 2),
                "probability_bottom_two": round(100 * sum(1 for r in ranks if r >= strategy_count - 1) / n, 2),
            }
        )

    robustness_rows.sort(key=lambda row: row["probability_ranked_first"], reverse=True)
    return simulation_rows, robustness_rows


def main() -> None:
    nodes = read_csv(NODES_PATH)
    edges = read_csv(EDGES_PATH)
    strategies = read_csv(STRATEGIES_PATH)
    scenarios = read_csv(SCENARIOS_PATH)

    profile_rows = []
    for row in strategies:
        value = base_containment_value(row)
        profile_rows.append(
            {
                "strategy_id": row["strategy_id"],
                "strategy": row["strategy"],
                "system_domain": row["system_domain"],
                "critical_function": row["critical_function"],
                "base_containment_value": round(value, 5),
                "modularity": row["modularity"],
                "redundancy": row["redundancy"],
                "dependency_mapping": row["dependency_mapping"],
                "isolation_capacity": row["isolation_capacity"],
                "coordination_readiness": row["coordination_readiness"],
                "justice_protection": row["justice_protection"],
                "common_mode_risk": row["common_mode_risk"],
                "diagnostic": strategy_diagnostic(row, value),
            }
        )

    cascade_rows, cascade_summary = cascade_monte_carlo(nodes, edges, n=2000)
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

    write_csv(OUT_TABLES / "modularity_cascade_strategy_profiles_standard.csv", profile_rows)
    write_csv(OUT_TABLES / "cascade_monte_carlo_standard.csv", cascade_rows)
    write_csv(OUT_TABLES / "cascade_summary_standard.csv", cascade_summary)
    write_csv(OUT_TABLES / "containment_strategy_rankings_standard.csv", rankings)
    write_csv(OUT_TABLES / "containment_strategy_top_rank_summary_standard.csv", top_rank_rows)
    write_csv(OUT_TABLES / "containment_strategy_monte_carlo_standard.csv", strategy_simulation)
    write_csv(OUT_TABLES / "containment_strategy_robustness_summary_standard.csv", robustness_rows)
    write_csv(DATA_PROCESSED / "modularity_cascade_strategy_profiles_standard.csv", profile_rows)

    print("Modularity and cascade workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    print("Highest cascade-risk initial failures:")
    for row in cascade_summary[:5]:
        print(
            f"  {row['initial_failure']}: large cascade probability="
            f"{row['probability_large_cascade']}%, mean impact={row['mean_justice_weighted_impact']}"
        )
    print("Containment strategy diagnostics:")
    for row in profile_rows:
        print(
            f"  {row['strategy']}: value={row['base_containment_value']} "
            f"diagnostic={row['diagnostic']}"
        )


if __name__ == "__main__":
    main()
