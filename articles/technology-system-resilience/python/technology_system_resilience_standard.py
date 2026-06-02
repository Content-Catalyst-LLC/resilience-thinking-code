#!/usr/bin/env python3
# Dependency-light Technology System Resilience workflow.
# Run: python3 python/technology_system_resilience_standard.py

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
    "architecture",
    "redundancy",
    "observability",
    "cybersecurity",
    "data_integrity",
    "maintainability",
    "governance",
    "human_safeguards",
    "vendor_contingency",
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

def technology_resilience_value(row: dict[str, str]) -> float:
    return (
        0.10 * f(row, "architecture")
        + 0.10 * f(row, "redundancy")
        + 0.10 * f(row, "observability")
        + 0.11 * f(row, "cybersecurity")
        + 0.11 * f(row, "data_integrity")
        + 0.11 * f(row, "maintainability")
        + 0.11 * f(row, "governance")
        + 0.11 * f(row, "human_safeguards")
        + 0.10 * f(row, "vendor_contingency")
        - 0.03 * f(row, "technical_debt_risk")
        - 0.02 * f(row, "implementation_burden")
    )

def adjusted_technology_value(row: dict[str, str], value: float) -> float:
    maintainability_gap = max(0.0, 8.3 - f(row, "maintainability"))
    governance_gap = max(0.0, 8.3 - f(row, "governance"))
    human_gap = max(0.0, 8.2 - f(row, "human_safeguards"))
    vendor_gap = max(0.0, 8.0 - f(row, "vendor_contingency"))
    return value - 0.06 * maintainability_gap - 0.06 * governance_gap - 0.07 * human_gap - 0.05 * vendor_gap

def score_strategy(row: dict[str, str], scenario: dict[str, str]) -> float:
    return (
        f(scenario, "architecture_weight") * f(row, "architecture")
        + f(scenario, "redundancy_weight") * f(row, "redundancy")
        + f(scenario, "observability_weight") * f(row, "observability")
        + f(scenario, "cybersecurity_weight") * f(row, "cybersecurity")
        + f(scenario, "data_integrity_weight") * f(row, "data_integrity")
        + f(scenario, "maintainability_weight") * f(row, "maintainability")
        + f(scenario, "governance_weight") * f(row, "governance")
        + f(scenario, "human_safeguards_weight") * f(row, "human_safeguards")
        + f(scenario, "vendor_contingency_weight") * f(row, "vendor_contingency")
        - f(scenario, "technical_debt_risk_weight") * f(row, "technical_debt_risk")
        - f(scenario, "implementation_burden_weight") * f(row, "implementation_burden")
    )

def strategy_diagnostic(row: dict[str, str], value: float) -> str:
    if f(row, "implementation_burden") >= 3.7:
        return "implementation-burden review needed"
    if f(row, "technical_debt_risk") >= 3.3:
        return "technical-debt review needed"
    if f(row, "human_safeguards") < 8.1:
        return "human-safeguards review needed"
    if f(row, "maintainability") < 8.1:
        return "maintainability review needed"
    if f(row, "governance") < 8.3:
        return "governance review needed"
    if f(row, "vendor_contingency") < 7.9:
        return "vendor-contingency review needed"
    if value >= 7.55:
        return "strong technology resilience strategy candidate"
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
                "technology_resilience_value": round(value, 5),
                "technical_debt_risk": strategy["technical_debt_risk"],
                "implementation_burden": strategy["implementation_burden"],
                "critical_function": strategy["critical_function"],
            })
    return rows

def simulate_technology_system(system, events, seed, time_steps=96):
    rng = random.Random(seed)
    function = f(system, "initial_function")
    technical_debt = f(system, "technical_debt")
    human_strain = f(system, "initial_human_strain")
    data_trust = f(system, "data_integrity")
    security_posture = f(system, "cybersecurity")

    architecture = f(system, "architecture")
    redundancy = f(system, "redundancy")
    observability = f(system, "observability")
    maintainability = f(system, "maintainability")
    governance = f(system, "governance")
    human = f(system, "human_safeguards")
    vendor = f(system, "vendor_contingency")

    event_by_step = {10: events[0], 22: events[1], 34: events[2], 46: events[3], 58: events[4], 70: events[5], 82: events[6], 90: events[7]}
    rows = []

    for t in range(time_steps):
        event = event_by_step.get(t)
        if event:
            shock = f(event, "shock_intensity")
            architecture_stress = f(event, "architecture_stress")
            cloud_vendor_stress = f(event, "cloud_vendor_stress")
            cyber_stress = f(event, "cyber_stress")
            data_stress = f(event, "data_integrity_stress")
            maintenance_stress = f(event, "maintenance_stress")
            operator_stress = f(event, "human_operator_stress")
            governance_stress = f(event, "governance_stress")
            model_drift = f(event, "model_drift_stress")
            critical_pressure = f(event, "critical_function_pressure")
            event_name = event["event_name"]
        else:
            shock = 0.05 + rng.random() * 0.02
            architecture_stress = 0.09
            cloud_vendor_stress = 0.08
            cyber_stress = 0.08
            data_stress = 0.08 + 0.001 * t
            maintenance_stress = 0.10 + 0.0015 * t
            operator_stress = 0.09
            governance_stress = 0.08
            model_drift = 0.08 + 0.001 * t
            critical_pressure = 0.12
            event_name = "background technology pressure"

        disruption_load = (
            0.10 * shock
            + 0.10 * architecture_stress
            + 0.12 * cloud_vendor_stress
            + 0.14 * cyber_stress
            + 0.13 * data_stress
            + 0.13 * maintenance_stress
            + 0.12 * operator_stress
            + 0.10 * governance_stress
            + 0.08 * model_drift
            + 0.08 * critical_pressure
        )

        fallback_capacity = (
            0.19 * architecture
            + 0.19 * redundancy
            + 0.12 * maintainability
            + 0.12 * governance
            + 0.11 * human
            + 0.14 * vendor
            + 0.13 * max(0.0, 1.0 - technical_debt)
        )
        fallback_capacity = max(0.0, min(1.0, fallback_capacity))

        recovery_capacity = (
            0.15 * observability
            + 0.15 * security_posture
            + 0.15 * data_trust
            + 0.15 * maintainability
            + 0.16 * governance
            + 0.14 * human
            + 0.10 * vendor
        )
        recovery_capacity = max(0.0, min(1.0, recovery_capacity))

        fragility_gap = max(0.0, disruption_load + 0.28 * technical_debt - fallback_capacity)

        strain_increase = 0.18 * disruption_load + 0.17 * fragility_gap + 0.07 * technical_debt + 0.04 * operator_stress
        strain_recovery = 0.08 * human + 0.06 * governance + 0.03 * observability
        human_strain = max(0.0, min(1.0, human_strain + strain_increase - strain_recovery))

        data_trust = max(0.0, min(1.0, data_trust - 0.12 * data_stress - 0.06 * model_drift + 0.07 * governance + 0.07 * maintainability))
        security_posture = max(0.0, min(1.0, security_posture - 0.12 * cyber_stress - 0.05 * cloud_vendor_stress + 0.07 * observability + 0.06 * governance))

        function = (
            function
            - 0.30 * disruption_load
            - 0.16 * fragility_gap
            + 0.17 * fallback_capacity
            + 0.17 * recovery_capacity
            + 0.08 * data_trust
            + 0.07 * security_posture
            - 0.12 * human_strain
        )
        function = max(0.0, min(1.0, function))

        complexity_growth = 0.018 + 0.028 * disruption_load + 0.015 * maintenance_stress
        maintenance_investment = 0.042 * maintainability + 0.026 * governance + 0.014 * architecture
        technical_debt = max(0.0, min(1.0, technical_debt + complexity_growth - maintenance_investment))

        ethical_adjusted_function = max(0.0, min(1.0, function * (0.70 + 0.30 * human) - 0.08 * human_strain - 0.05 * (1.0 - governance)))
        resilience_score = max(0.0, min(1.0,
            0.17 * function
            + 0.15 * fallback_capacity
            + 0.15 * recovery_capacity
            + 0.13 * data_trust
            + 0.13 * security_posture
            + 0.12 * governance
            + 0.08 * human
            + 0.07 * (1.0 - technical_debt)
        ))

        rows.append({
            "system_id": system["system_id"],
            "system": system["system"],
            "system_context": system["system_context"],
            "time": t,
            "event": event_name,
            "disruption_load": round(disruption_load, 5),
            "fallback_capacity": round(fallback_capacity, 5),
            "recovery_capacity": round(recovery_capacity, 5),
            "fragility_gap": round(fragility_gap, 5),
            "function": round(function, 5),
            "data_trust": round(data_trust, 5),
            "security_posture": round(security_posture, 5),
            "technical_debt": round(technical_debt, 5),
            "human_strain": round(human_strain, 5),
            "ethical_adjusted_function": round(ethical_adjusted_function, 5),
            "resilience_score": round(resilience_score, 5),
        })
    return rows

def summarize_simulation(rows):
    summary = []
    for system in sorted(set(str(row["system"]) for row in rows)):
        subset = [row for row in rows if row["system"] == system]
        function = [float(row["function"]) for row in subset]
        debt = [float(row["technical_debt"]) for row in subset]
        strain = [float(row["human_strain"]) for row in subset]
        gap = [float(row["fragility_gap"]) for row in subset]
        data = [float(row["data_trust"]) for row in subset]
        security = [float(row["security_posture"]) for row in subset]
        ethical = [float(row["ethical_adjusted_function"]) for row in subset]
        score = [float(row["resilience_score"]) for row in subset]
        summary.append({
            "system": system,
            "mean_function": round(mean(function), 5),
            "minimum_function": round(min(function), 5),
            "final_function": round(function[-1], 5),
            "final_technical_debt": round(debt[-1], 5),
            "maximum_human_strain": round(max(strain), 5),
            "mean_fragility_gap": round(mean(gap), 5),
            "minimum_data_trust": round(min(data), 5),
            "minimum_security_posture": round(min(security), 5),
            "final_ethical_adjusted_function": round(ethical[-1], 5),
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
            for criterion in BENEFIT_CRITERIA + ["technical_debt_risk", "implementation_burden"]:
                sampled[criterion] = str(max(1.0, min(10.0, f(strategy, criterion) + rng.gauss(0, 0.55))))
            scored.append((score_strategy(sampled, scenario), strategy))
        scored.sort(key=lambda item: item[0], reverse=True)
        for rank, (value, strategy) in enumerate(scored, start=1):
            simulation_rows.append({
                "simulation_id": simulation_id,
                "strategy_id": strategy["strategy_id"],
                "strategy": strategy["strategy"],
                "rank": rank,
                "technology_resilience_value": round(value, 5),
                "winner": scored[0][1]["strategy"],
            })

    robustness_rows = []
    strategy_count = len(strategies)
    for strategy in strategies:
        subset = [row for row in simulation_rows if row["strategy_id"] == strategy["strategy_id"]]
        ranks = [int(row["rank"]) for row in subset]
        values = [float(row["technology_resilience_value"]) for row in subset]
        robustness_rows.append({
            "strategy_id": strategy["strategy_id"],
            "strategy": strategy["strategy"],
            "mean_technology_resilience_value": round(mean(values), 5),
            "median_technology_resilience_value": round(median(values), 5),
            "probability_ranked_first": round(100 * sum(1 for r in ranks if r == 1) / n, 2),
            "probability_top_two": round(100 * sum(1 for r in ranks if r <= 2) / n, 2),
            "probability_bottom_two": round(100 * sum(1 for r in ranks if r >= strategy_count - 1) / n, 2),
        })
    robustness_rows.sort(key=lambda row: row["probability_ranked_first"], reverse=True)
    return simulation_rows, robustness_rows

def main() -> None:
    strategies = read_csv(ROOT / "data/raw/technology_resilience_strategies.csv")
    scenarios = read_csv(ROOT / "data/raw/technology_resilience_scenarios.csv")
    systems = read_csv(ROOT / "data/raw/technology_system_profiles.csv")
    events = read_csv(ROOT / "data/raw/technology_disruption_events.csv")

    strategy_profiles = []
    for row in strategies:
        value = technology_resilience_value(row)
        adjusted = adjusted_technology_value(row, value)
        strategy_profiles.append({
            "strategy_id": row["strategy_id"],
            "strategy": row["strategy"],
            "system_domain": row["system_domain"],
            "critical_function": row["critical_function"],
            "technology_resilience_value": round(value, 5),
            "adjusted_technology_resilience_value": round(adjusted, 5),
            "human_adjusted_value": round(value * (0.72 + 0.028 * f(row, "human_safeguards") - 0.010 * f(row, "technical_debt_risk")), 5),
            "architecture": row["architecture"],
            "redundancy": row["redundancy"],
            "observability": row["observability"],
            "cybersecurity": row["cybersecurity"],
            "data_integrity": row["data_integrity"],
            "maintainability": row["maintainability"],
            "governance": row["governance"],
            "human_safeguards": row["human_safeguards"],
            "vendor_contingency": row["vendor_contingency"],
            "technical_debt_risk": row["technical_debt_risk"],
            "implementation_burden": row["implementation_burden"],
            "diagnostic": strategy_diagnostic(row, value),
        })

    rankings = scenario_rankings(strategies, scenarios)

    dynamic_rows = []
    for idx, system in enumerate(systems):
        dynamic_rows.extend(simulate_technology_system(system, events, seed=100 + idx))
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

    write_csv(OUT_TABLES / "technology_resilience_strategy_profiles_standard.csv", strategy_profiles)
    write_csv(OUT_TABLES / "technology_resilience_strategy_rankings_standard.csv", rankings)
    write_csv(OUT_TABLES / "technology_resilience_top_rank_summary_standard.csv", top_rank_rows)
    write_csv(OUT_TABLES / "technology_system_resilience_dynamic_simulation_standard.csv", dynamic_rows)
    write_csv(OUT_TABLES / "technology_system_resilience_dynamic_summary_standard.csv", dynamic_summary)
    write_csv(OUT_TABLES / "technology_resilience_monte_carlo_standard.csv", strategy_simulation)
    write_csv(OUT_TABLES / "technology_resilience_robustness_summary_standard.csv", robustness_rows)
    write_csv(DATA_PROCESSED / "technology_resilience_strategy_profiles_standard.csv", strategy_profiles)

    print("Technology system resilience workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    for row in strategy_profiles:
        print(f"  {row['strategy']}: value={row['technology_resilience_value']} diagnostic={row['diagnostic']}")

if __name__ == "__main__":
    main()
