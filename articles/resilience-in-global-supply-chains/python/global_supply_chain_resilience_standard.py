#!/usr/bin/env python3
# Dependency-light Global Supply Chain Resilience workflow.
# Run: python3 python/global_supply_chain_resilience_standard.py

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
    "redundancy",
    "flexibility",
    "visibility",
    "coordination",
    "adaptive_capacity",
    "equity_safeguards",
    "infrastructure_continuity",
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

def supply_chain_resilience_value(row: dict[str, str]) -> float:
    return (
        0.13 * f(row, "redundancy")
        + 0.13 * f(row, "flexibility")
        + 0.13 * f(row, "visibility")
        + 0.13 * f(row, "coordination")
        + 0.13 * f(row, "adaptive_capacity")
        + 0.13 * f(row, "equity_safeguards")
        + 0.13 * f(row, "infrastructure_continuity")
        - 0.06 * f(row, "systemic_exposure")
        - 0.03 * f(row, "implementation_burden")
    )

def adjusted_resilience_value(row: dict[str, str], value: float) -> float:
    equity_gap = max(0.0, 8.0 - f(row, "equity_safeguards"))
    infrastructure_gap = max(0.0, 8.0 - f(row, "infrastructure_continuity"))
    visibility_gap = max(0.0, 7.8 - f(row, "visibility"))
    return value - 0.08 * equity_gap - 0.06 * infrastructure_gap - 0.05 * visibility_gap

def score_strategy(row: dict[str, str], scenario: dict[str, str]) -> float:
    return (
        f(scenario, "redundancy_weight") * f(row, "redundancy")
        + f(scenario, "flexibility_weight") * f(row, "flexibility")
        + f(scenario, "visibility_weight") * f(row, "visibility")
        + f(scenario, "coordination_weight") * f(row, "coordination")
        + f(scenario, "adaptive_capacity_weight") * f(row, "adaptive_capacity")
        + f(scenario, "equity_safeguards_weight") * f(row, "equity_safeguards")
        + f(scenario, "infrastructure_continuity_weight") * f(row, "infrastructure_continuity")
        - f(scenario, "systemic_exposure_weight") * f(row, "systemic_exposure")
        - f(scenario, "implementation_burden_weight") * f(row, "implementation_burden")
    )

def strategy_diagnostic(row: dict[str, str], value: float) -> str:
    if f(row, "implementation_burden") >= 3.7:
        return "implementation-burden review needed"
    if f(row, "equity_safeguards") < 7.8:
        return "equity and labor safeguards need strengthening"
    if f(row, "infrastructure_continuity") < 7.8:
        return "infrastructure-continuity review needed"
    if f(row, "visibility") < 7.4:
        return "visibility and dependency-mapping review needed"
    if f(row, "redundancy") < 7.4:
        return "redundancy review needed"
    if value >= 6.95:
        return "strong supply chain resilience strategy candidate"
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
                "supply_chain_resilience_value": round(value, 5),
                "systemic_exposure": strategy["systemic_exposure"],
                "implementation_burden": strategy["implementation_burden"],
                "critical_function": strategy["critical_function"],
            })
    return rows

def simulate_network_flow(network, events, seed, time_steps=80):
    rng = random.Random(seed)
    flow = f(network, "baseline_flow_performance")
    coordination = f(network, "coordination_capacity")
    equity_sensitivity = f(network, "equity_sensitivity")

    supplier_concentration = f(network, "supplier_concentration")
    chokepoint = f(network, "route_chokepoint_exposure")
    inventory_thinness = f(network, "inventory_thinness")
    climate_exposure = f(network, "climate_exposure")
    cyber_dependency = f(network, "cyber_dependency")
    labor_vulnerability = f(network, "labor_vulnerability")
    infrastructure_fragility = f(network, "infrastructure_fragility")

    event_by_step = {12: events[0], 27: events[1], 42: events[2], 56: events[3], 70: events[4]}
    rows = []

    for t in range(time_steps):
        event = event_by_step.get(t)
        if event:
            shock = f(event, "shock_intensity")
            supplier_failure = f(event, "supplier_failure")
            logistics = f(event, "logistics_disruption")
            demand = f(event, "demand_surge")
            inventory = f(event, "inventory_depletion")
            cyber = f(event, "cyber_disruption")
            climate = f(event, "climate_pressure")
            labor = f(event, "labor_disruption")
            coordination_stress = f(event, "coordination_stress")
            equity_burden = f(event, "equity_burden")
            event_name = event["event_name"]
        else:
            shock = 0.05 + rng.random() * 0.02
            supplier_failure = 0.10
            logistics = 0.10
            demand = 0.11
            inventory = 0.10 + 0.001 * t
            cyber = 0.10
            climate = 0.11
            labor = 0.10
            coordination_stress = 0.10
            equity_burden = 0.22
            event_name = "background supply-network stress"

        exposure = (
            0.14 * supplier_concentration
            + 0.14 * chokepoint
            + 0.13 * inventory_thinness
            + 0.13 * climate_exposure
            + 0.13 * cyber_dependency
            + 0.13 * labor_vulnerability
            + 0.14 * infrastructure_fragility
        )

        disruption_load = (
            0.10 * shock
            + 0.13 * supplier_failure
            + 0.13 * logistics
            + 0.11 * demand
            + 0.12 * inventory
            + 0.12 * cyber
            + 0.12 * climate
            + 0.10 * labor
            + 0.10 * coordination_stress
            + 0.08 * exposure
        )

        adaptive_response = (
            0.14 * (1.0 - supplier_concentration)
            + 0.14 * (1.0 - chokepoint)
            + 0.12 * (1.0 - inventory_thinness)
            + 0.12 * (1.0 - climate_exposure)
            + 0.12 * (1.0 - cyber_dependency)
            + 0.12 * (1.0 - labor_vulnerability)
            + 0.12 * (1.0 - infrastructure_fragility)
            + 0.16 * coordination
        )
        adaptive_response = max(0.0, min(1.0, adaptive_response))

        equity_penalty = max(0.0, equity_burden + labor_vulnerability - 1.35) * 0.10
        infrastructure_penalty = max(0.0, infrastructure_fragility + logistics + climate - 2.00) * 0.07
        cyber_penalty = max(0.0, cyber_dependency + cyber - 1.35) * 0.07

        flow = (
            flow
            - 0.32 * disruption_load
            + 0.22 * adaptive_response
            + 0.08 * coordination
            - equity_penalty
            - infrastructure_penalty
            - cyber_penalty
        )
        flow = max(0.0, min(1.0, flow))

        inventory_thinness = max(0.0, min(1.0, inventory_thinness + 0.012 * demand + 0.012 * inventory - 0.010 * adaptive_response))
        supplier_concentration = max(0.0, min(1.0, supplier_concentration + 0.010 * supplier_failure - 0.008 * adaptive_response))
        equity_adjusted_flow = max(0.0, min(1.0, flow * (0.72 + 0.28 * (1.0 - equity_burden + equity_sensitivity * 0.40))))

        rows.append({
            "network_id": network["network_id"],
            "network": network["network"],
            "network_context": network["network_context"],
            "time": t,
            "event": event_name,
            "disruption_load": round(disruption_load, 5),
            "adaptive_response": round(adaptive_response, 5),
            "flow_performance": round(flow, 5),
            "inventory_thinness": round(inventory_thinness, 5),
            "supplier_concentration": round(supplier_concentration, 5),
            "equity_adjusted_flow": round(equity_adjusted_flow, 5),
        })
    return rows

def summarize_simulation(rows):
    summary = []
    for network in sorted(set(str(row["network"]) for row in rows)):
        subset = [row for row in rows if row["network"] == network]
        flow = [float(row["flow_performance"]) for row in subset]
        equity = [float(row["equity_adjusted_flow"]) for row in subset]
        inventory = [float(row["inventory_thinness"]) for row in subset]
        supplier = [float(row["supplier_concentration"]) for row in subset]
        summary.append({
            "network": network,
            "mean_flow_performance": round(mean(flow), 5),
            "minimum_flow_performance": round(min(flow), 5),
            "final_flow_performance": round(flow[-1], 5),
            "mean_equity_adjusted_flow": round(mean(equity), 5),
            "maximum_inventory_thinness": round(max(inventory), 5),
            "final_inventory_thinness": round(inventory[-1], 5),
            "maximum_supplier_concentration": round(max(supplier), 5),
            "final_supplier_concentration": round(supplier[-1], 5),
        })
    summary.sort(key=lambda row: row["mean_equity_adjusted_flow"], reverse=True)
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
                "supply_chain_resilience_value": round(value, 5),
                "winner": scored[0][1]["strategy"],
            })

    robustness_rows = []
    strategy_count = len(strategies)
    for strategy in strategies:
        subset = [row for row in simulation_rows if row["strategy_id"] == strategy["strategy_id"]]
        ranks = [int(row["rank"]) for row in subset]
        values = [float(row["supply_chain_resilience_value"]) for row in subset]
        robustness_rows.append({
            "strategy_id": strategy["strategy_id"],
            "strategy": strategy["strategy"],
            "mean_supply_chain_resilience_value": round(mean(values), 5),
            "median_supply_chain_resilience_value": round(median(values), 5),
            "probability_ranked_first": round(100 * sum(1 for r in ranks if r == 1) / n, 2),
            "probability_top_two": round(100 * sum(1 for r in ranks if r <= 2) / n, 2),
            "probability_bottom_two": round(100 * sum(1 for r in ranks if r >= strategy_count - 1) / n, 2),
        })
    robustness_rows.sort(key=lambda row: row["probability_ranked_first"], reverse=True)
    return simulation_rows, robustness_rows

def main() -> None:
    strategies = read_csv(ROOT / "data/raw/supply_chain_resilience_strategies.csv")
    scenarios = read_csv(ROOT / "data/raw/supply_chain_resilience_scenarios.csv")
    networks = read_csv(ROOT / "data/raw/supply_network_profiles.csv")
    events = read_csv(ROOT / "data/raw/supply_chain_stress_events.csv")

    strategy_profiles = []
    for row in strategies:
        value = supply_chain_resilience_value(row)
        adjusted = adjusted_resilience_value(row, value)
        strategy_profiles.append({
            "strategy_id": row["strategy_id"],
            "strategy": row["strategy"],
            "system_domain": row["system_domain"],
            "critical_function": row["critical_function"],
            "supply_chain_resilience_value": round(value, 5),
            "adjusted_supply_chain_resilience_value": round(adjusted, 5),
            "equity_adjusted_value": round(value * (0.72 + 0.028 * f(row, "equity_safeguards")), 5),
            "redundancy": row["redundancy"],
            "flexibility": row["flexibility"],
            "visibility": row["visibility"],
            "coordination": row["coordination"],
            "adaptive_capacity": row["adaptive_capacity"],
            "equity_safeguards": row["equity_safeguards"],
            "infrastructure_continuity": row["infrastructure_continuity"],
            "systemic_exposure": row["systemic_exposure"],
            "implementation_burden": row["implementation_burden"],
            "diagnostic": strategy_diagnostic(row, value),
        })

    rankings = scenario_rankings(strategies, scenarios)

    dynamic_rows = []
    for idx, network in enumerate(networks):
        dynamic_rows.extend(simulate_network_flow(network, events, seed=100 + idx))
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

    write_csv(OUT_TABLES / "global_supply_chain_strategy_profiles_standard.csv", strategy_profiles)
    write_csv(OUT_TABLES / "global_supply_chain_strategy_rankings_standard.csv", rankings)
    write_csv(OUT_TABLES / "global_supply_chain_top_rank_summary_standard.csv", top_rank_rows)
    write_csv(OUT_TABLES / "global_supply_chain_dynamic_simulation_standard.csv", dynamic_rows)
    write_csv(OUT_TABLES / "global_supply_chain_dynamic_summary_standard.csv", dynamic_summary)
    write_csv(OUT_TABLES / "global_supply_chain_monte_carlo_standard.csv", strategy_simulation)
    write_csv(OUT_TABLES / "global_supply_chain_robustness_summary_standard.csv", robustness_rows)
    write_csv(DATA_PROCESSED / "global_supply_chain_strategy_profiles_standard.csv", strategy_profiles)

    print("Global supply chain resilience workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    for row in strategy_profiles:
        print(f"  {row['strategy']}: value={row['supply_chain_resilience_value']} diagnostic={row['diagnostic']}")

if __name__ == "__main__":
    main()
