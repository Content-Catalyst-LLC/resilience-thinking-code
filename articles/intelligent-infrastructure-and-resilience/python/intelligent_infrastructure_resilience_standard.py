#!/usr/bin/env python3
# Dependency-light Intelligent Infrastructure and Resilience workflow.
# Run: python3 python/intelligent_infrastructure_resilience_standard.py

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
    "monitoring_value",
    "predictive_maintenance",
    "cyber_physical_security",
    "digital_twin_capacity",
    "redundancy_and_fallback",
    "climate_adaptation",
    "governance_quality",
    "equity_performance",
    "ecological_integration",
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

def infrastructure_resilience_value(row: dict[str, str]) -> float:
    return (
        0.10 * f(row, "monitoring_value")
        + 0.11 * f(row, "predictive_maintenance")
        + 0.11 * f(row, "cyber_physical_security")
        + 0.10 * f(row, "digital_twin_capacity")
        + 0.11 * f(row, "redundancy_and_fallback")
        + 0.11 * f(row, "climate_adaptation")
        + 0.12 * f(row, "governance_quality")
        + 0.12 * f(row, "equity_performance")
        + 0.10 * f(row, "ecological_integration")
        - 0.04 * f(row, "fragility_risk")
        - 0.04 * f(row, "implementation_burden")
    )

def adjusted_infrastructure_value(row: dict[str, str], value: float) -> float:
    governance_gap = max(0.0, 8.5 - f(row, "governance_quality"))
    equity_gap = max(0.0, 8.5 - f(row, "equity_performance"))
    redundancy_gap = max(0.0, 8.5 - f(row, "redundancy_and_fallback"))
    maintenance_gap = max(0.0, 8.4 - f(row, "predictive_maintenance"))
    return value - 0.07 * governance_gap - 0.08 * equity_gap - 0.07 * redundancy_gap - 0.06 * maintenance_gap

def score_strategy(row: dict[str, str], scenario: dict[str, str]) -> float:
    return (
        f(scenario, "monitoring_value_weight") * f(row, "monitoring_value")
        + f(scenario, "predictive_maintenance_weight") * f(row, "predictive_maintenance")
        + f(scenario, "cyber_physical_security_weight") * f(row, "cyber_physical_security")
        + f(scenario, "digital_twin_capacity_weight") * f(row, "digital_twin_capacity")
        + f(scenario, "redundancy_and_fallback_weight") * f(row, "redundancy_and_fallback")
        + f(scenario, "climate_adaptation_weight") * f(row, "climate_adaptation")
        + f(scenario, "governance_quality_weight") * f(row, "governance_quality")
        + f(scenario, "equity_performance_weight") * f(row, "equity_performance")
        + f(scenario, "ecological_integration_weight") * f(row, "ecological_integration")
        - f(scenario, "fragility_risk_weight") * f(row, "fragility_risk")
        - f(scenario, "implementation_burden_weight") * f(row, "implementation_burden")
    )

def strategy_diagnostic(row: dict[str, str], value: float) -> str:
    if f(row, "implementation_burden") >= 3.9:
        return "implementation-burden review needed"
    if f(row, "fragility_risk") >= 3.1:
        return "hidden-fragility review needed"
    if f(row, "equity_performance") < 8.1:
        return "equity-performance review needed"
    if f(row, "governance_quality") < 8.3:
        return "governance review needed"
    if f(row, "cyber_physical_security") < 8.1:
        return "cyber-physical security review needed"
    if f(row, "predictive_maintenance") < 8.1:
        return "maintenance-capacity review needed"
    if value >= 7.65:
        return "strong intelligent infrastructure resilience strategy candidate"
    return "promising but requires field validation"

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
                "infrastructure_resilience_value": round(value, 5),
                "fragility_risk": strategy["fragility_risk"],
                "implementation_burden": strategy["implementation_burden"],
                "critical_function": strategy["critical_function"],
            })
    return rows

def simulate_infrastructure_system(system, events, seed, time_steps=96):
    rng = random.Random(seed)
    function = f(system, "initial_function")
    backlog = f(system, "initial_backlog")
    operator_strain = f(system, "initial_operator_strain")
    data_trust = f(system, "monitoring_value")

    physical = f(system, "physical_robustness")
    monitoring = f(system, "monitoring_value")
    maintenance = f(system, "predictive_maintenance")
    cyber_security = f(system, "cyber_physical_security")
    redundancy = f(system, "redundancy")
    governance = f(system, "governance")
    equity = f(system, "equity_performance")
    ecology = f(system, "ecological_adaptation")

    event_by_step = {10: events[0], 22: events[1], 34: events[2], 46: events[3], 58: events[4], 72: events[5], 86: events[6]}
    rows = []

    for t in range(time_steps):
        event = event_by_step.get(t)
        if event:
            shock = f(event, "shock_intensity")
            climate_stress = f(event, "climate_stress")
            cyber_stress = f(event, "cyber_stress")
            data_stress = f(event, "data_stress")
            dependency_stress = f(event, "dependency_stress")
            maintenance_stress = f(event, "maintenance_stress")
            operator_stress = f(event, "operator_stress")
            equity_pressure = f(event, "equity_pressure")
            governance_pressure = f(event, "governance_pressure")
            event_name = event["event_name"]
        else:
            shock = 0.05 + rng.random() * 0.02
            climate_stress = 0.08 + 0.001 * t
            cyber_stress = 0.06
            data_stress = 0.06
            dependency_stress = 0.08
            maintenance_stress = 0.10 + 0.0015 * t
            operator_stress = 0.08
            equity_pressure = 0.09
            governance_pressure = 0.08
            event_name = "background infrastructure pressure"

        disturbance = (
            0.11 * shock
            + 0.14 * climate_stress
            + 0.13 * cyber_stress
            + 0.12 * data_stress
            + 0.13 * dependency_stress
            + 0.13 * maintenance_stress
            + 0.10 * operator_stress
            + 0.07 * equity_pressure
            + 0.07 * governance_pressure
        )

        intelligence_value = (
            0.23 * data_trust
            + 0.21 * maintenance
            + 0.16 * governance
            + 0.14 * equity
            + 0.14 * ecology
            + 0.12 * monitoring
        )
        intelligence_value = max(0.0, min(1.0, intelligence_value))

        response_capacity = (
            0.17 * physical
            + 0.17 * redundancy
            + 0.17 * cyber_security
            + 0.17 * governance
            + 0.13 * maintenance
            + 0.12 * equity
            + 0.07 * ecology
        )
        response_capacity = max(0.0, min(1.0, response_capacity))

        fragility_gap = max(
            0.0,
            disturbance
            + 0.25 * backlog
            + 0.14 * cyber_stress
            + 0.12 * dependency_stress
            - response_capacity
        )

        backlog_growth = 0.018 + 0.030 * climate_stress + 0.024 * disturbance + 0.016 * maintenance_stress
        maintenance_investment = 0.046 * maintenance + 0.030 * governance + 0.014 * physical
        backlog = max(0.0, min(1.0, backlog + backlog_growth - maintenance_investment))

        data_trust = max(0.0, min(1.0,
            data_trust
            - 0.11 * data_stress
            - 0.08 * cyber_stress
            - 0.04 * dependency_stress
            + 0.060 * governance
            + 0.040 * cyber_security
            + 0.030 * monitoring
        ))

        strain_increase = 0.15 * disturbance + 0.13 * fragility_gap + 0.09 * backlog + 0.08 * dependency_stress + 0.05 * operator_stress
        strain_recovery = 0.08 * governance + 0.06 * redundancy + 0.04 * maintenance
        operator_strain = max(0.0, min(1.0, operator_strain + strain_increase - strain_recovery))

        equity_access = max(0.0, min(1.0,
            0.40 * equity
            + 0.18 * governance
            + 0.17 * redundancy
            + 0.12 * ecology
            + 0.08 * physical
            - 0.11 * fragility_gap
            - 0.07 * operator_strain
            - 0.06 * equity_pressure
        ))

        function = (
            function
            - 0.27 * disturbance
            - 0.16 * fragility_gap
            - 0.11 * backlog
            + 0.17 * response_capacity
            + 0.15 * intelligence_value
            + 0.10 * equity_access
            + 0.05 * data_trust
            - 0.09 * operator_strain
        )
        function = max(0.0, min(1.0, function))

        resilience_score = max(0.0, min(1.0,
            0.18 * function
            + 0.15 * response_capacity
            + 0.14 * intelligence_value
            + 0.12 * data_trust
            + 0.12 * equity_access
            + 0.10 * ecology
            + 0.10 * (1.0 - backlog)
            + 0.09 * (1.0 - operator_strain)
        ))

        rows.append({
            "system_id": system["system_id"],
            "system": system["system"],
            "system_context": system["system_context"],
            "time": t,
            "event": event_name,
            "disturbance": round(disturbance, 5),
            "intelligence_value": round(intelligence_value, 5),
            "response_capacity": round(response_capacity, 5),
            "fragility_gap": round(fragility_gap, 5),
            "maintenance_backlog": round(backlog, 5),
            "data_trust": round(data_trust, 5),
            "operator_strain": round(operator_strain, 5),
            "equity_access": round(equity_access, 5),
            "function": round(function, 5),
            "resilience_score": round(resilience_score, 5),
        })
    return rows

def summarize_simulation(rows):
    summary = []
    for system in sorted(set(str(row["system"]) for row in rows)):
        subset = [row for row in rows if row["system"] == system]
        function = [float(row["function"]) for row in subset]
        backlog = [float(row["maintenance_backlog"]) for row in subset]
        data_trust = [float(row["data_trust"]) for row in subset]
        strain = [float(row["operator_strain"]) for row in subset]
        equity = [float(row["equity_access"]) for row in subset]
        gap = [float(row["fragility_gap"]) for row in subset]
        score = [float(row["resilience_score"]) for row in subset]
        summary.append({
            "system": system,
            "mean_function": round(mean(function), 5),
            "minimum_function": round(min(function), 5),
            "final_function": round(function[-1], 5),
            "final_maintenance_backlog": round(backlog[-1], 5),
            "minimum_data_trust": round(min(data_trust), 5),
            "maximum_operator_strain": round(max(strain), 5),
            "mean_equity_access": round(mean(equity), 5),
            "mean_fragility_gap": round(mean(gap), 5),
            "final_resilience_score": round(score[-1], 5),
        })
    summary.sort(key=lambda row: row["final_resilience_score"], reverse=True)
    return summary

def strategy_monte_carlo(strategies, scenario, n=3000):
    rng = random.Random(42)
    simulation_rows = []
    for simulation_id in range(n):
        scored = []
        for strategy in strategies:
            sampled = dict(strategy)
            for criterion in BENEFIT_CRITERIA + ["fragility_risk", "implementation_burden"]:
                sampled[criterion] = str(max(1.0, min(10.0, f(strategy, criterion) + rng.gauss(0, 0.55))))
            scored.append((score_strategy(sampled, scenario), strategy))
        scored.sort(key=lambda item: item[0], reverse=True)
        for rank, (value, strategy) in enumerate(scored, start=1):
            simulation_rows.append({
                "simulation_id": simulation_id,
                "strategy_id": strategy["strategy_id"],
                "strategy": strategy["strategy"],
                "rank": rank,
                "infrastructure_resilience_value": round(value, 5),
                "winner": scored[0][1]["strategy"],
            })

    robustness_rows = []
    strategy_count = len(strategies)
    for strategy in strategies:
        subset = [row for row in simulation_rows if row["strategy_id"] == strategy["strategy_id"]]
        ranks = [int(row["rank"]) for row in subset]
        values = [float(row["infrastructure_resilience_value"]) for row in subset]
        robustness_rows.append({
            "strategy_id": strategy["strategy_id"],
            "strategy": strategy["strategy"],
            "mean_infrastructure_resilience_value": round(mean(values), 5),
            "median_infrastructure_resilience_value": round(median(values), 5),
            "probability_ranked_first": round(100 * sum(1 for r in ranks if r == 1) / n, 2),
            "probability_top_two": round(100 * sum(1 for r in ranks if r <= 2) / n, 2),
            "probability_bottom_two": round(100 * sum(1 for r in ranks if r >= strategy_count - 1) / n, 2),
        })
    robustness_rows.sort(key=lambda row: row["probability_ranked_first"], reverse=True)
    return simulation_rows, robustness_rows

def main() -> None:
    strategies = read_csv(ROOT / "data/raw/intelligent_infrastructure_strategies.csv")
    scenarios = read_csv(ROOT / "data/raw/intelligent_infrastructure_scenarios.csv")
    systems = read_csv(ROOT / "data/raw/intelligent_infrastructure_systems.csv")
    events = read_csv(ROOT / "data/raw/intelligent_infrastructure_events.csv")

    strategy_profiles = []
    for row in strategies:
        value = infrastructure_resilience_value(row)
        adjusted = adjusted_infrastructure_value(row, value)
        strategy_profiles.append({
            "strategy_id": row["strategy_id"],
            "strategy": row["strategy"],
            "system_domain": row["system_domain"],
            "critical_function": row["critical_function"],
            "infrastructure_resilience_value": round(value, 5),
            "adjusted_infrastructure_resilience_value": round(adjusted, 5),
            "equity_and_governance_adjusted_value": round(value * (0.70 + 0.018 * f(row, "equity_performance") + 0.018 * f(row, "governance_quality") - 0.010 * f(row, "fragility_risk")), 5),
            "monitoring_value": row["monitoring_value"],
            "predictive_maintenance": row["predictive_maintenance"],
            "cyber_physical_security": row["cyber_physical_security"],
            "digital_twin_capacity": row["digital_twin_capacity"],
            "redundancy_and_fallback": row["redundancy_and_fallback"],
            "climate_adaptation": row["climate_adaptation"],
            "governance_quality": row["governance_quality"],
            "equity_performance": row["equity_performance"],
            "ecological_integration": row["ecological_integration"],
            "fragility_risk": row["fragility_risk"],
            "implementation_burden": row["implementation_burden"],
            "diagnostic": strategy_diagnostic(row, value),
        })

    rankings = scenario_rankings(strategies, scenarios)

    dynamic_rows = []
    for idx, system in enumerate(systems):
        dynamic_rows.extend(simulate_infrastructure_system(system, events, seed=100 + idx))
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

    write_csv(OUT_TABLES / "intelligent_infrastructure_strategy_profiles_standard.csv", strategy_profiles)
    write_csv(OUT_TABLES / "intelligent_infrastructure_strategy_rankings_standard.csv", rankings)
    write_csv(OUT_TABLES / "intelligent_infrastructure_top_rank_summary_standard.csv", top_rank_rows)
    write_csv(OUT_TABLES / "intelligent_infrastructure_dynamic_simulation_standard.csv", dynamic_rows)
    write_csv(OUT_TABLES / "intelligent_infrastructure_dynamic_summary_standard.csv", dynamic_summary)
    write_csv(OUT_TABLES / "intelligent_infrastructure_monte_carlo_standard.csv", strategy_simulation)
    write_csv(OUT_TABLES / "intelligent_infrastructure_robustness_summary_standard.csv", robustness_rows)
    write_csv(DATA_PROCESSED / "intelligent_infrastructure_strategy_profiles_standard.csv", strategy_profiles)

    print("Intelligent infrastructure resilience workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    for row in strategy_profiles:
        print(f"  {row['strategy']}: value={row['infrastructure_resilience_value']} diagnostic={row['diagnostic']}")

if __name__ == "__main__":
    main()
