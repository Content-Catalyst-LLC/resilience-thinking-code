#!/usr/bin/env python3
# Dependency-light Local Knowledge and Resilience Practice workflow.
# Run: python3 python/local_knowledge_standard.py

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
    "participation_access",
    "knowledge_diversity",
    "decision_influence",
    "trust_building",
    "knowledge_protection",
    "reciprocity",
    "implementation_accountability",
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

def knowledge_integration_value(row: dict[str, str]) -> float:
    return (
        0.14 * f(row, "participation_access")
        + 0.14 * f(row, "knowledge_diversity")
        + 0.15 * f(row, "decision_influence")
        + 0.14 * f(row, "trust_building")
        + 0.14 * f(row, "knowledge_protection")
        + 0.14 * f(row, "reciprocity")
        + 0.15 * f(row, "implementation_accountability")
        - 0.02 * f(row, "implementation_burden")
    )

def adjusted_knowledge_value(row: dict[str, str], value: float) -> float:
    extraction_risk_gap = max(0.0, f(row, "decision_influence") - f(row, "implementation_accountability"))
    protection_gap = max(0.0, 8.4 - f(row, "knowledge_protection"))
    participation_gap = max(0.0, 8.2 - f(row, "participation_access"))
    return value - 0.08 * extraction_risk_gap - 0.08 * protection_gap - 0.06 * participation_gap

def score_strategy(row: dict[str, str], scenario: dict[str, str]) -> float:
    return (
        f(scenario, "participation_access_weight") * f(row, "participation_access")
        + f(scenario, "knowledge_diversity_weight") * f(row, "knowledge_diversity")
        + f(scenario, "decision_influence_weight") * f(row, "decision_influence")
        + f(scenario, "trust_building_weight") * f(row, "trust_building")
        + f(scenario, "knowledge_protection_weight") * f(row, "knowledge_protection")
        + f(scenario, "reciprocity_weight") * f(row, "reciprocity")
        + f(scenario, "implementation_accountability_weight") * f(row, "implementation_accountability")
        - f(scenario, "implementation_burden_weight") * f(row, "implementation_burden")
    )

def strategy_diagnostic(row: dict[str, str], value: float) -> str:
    if f(row, "implementation_burden") >= 3.5:
        return "implementation-burden review needed"
    if f(row, "knowledge_protection") < 8.2:
        return "knowledge-protection safeguards need strengthening"
    if f(row, "decision_influence") < 8.0:
        return "decision-influence review needed"
    if f(row, "participation_access") < 8.2:
        return "participation-access review needed"
    if f(row, "implementation_accountability") < 8.2:
        return "implementation-accountability review needed"
    if value >= 8.30:
        return "strong local-knowledge integration strategy candidate"
    return "promising but requires community validation"

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
                "knowledge_integration_value": round(value, 5),
                "implementation_burden": strategy["implementation_burden"],
                "critical_function": strategy["critical_function"],
            })
    return rows

def simulate_knowledge_system_response(system, events, seed, time_steps=80):
    rng = random.Random(seed)
    knowledge_function = f(system, "baseline_knowledge_function")
    institutional_trust = f(system, "institutional_trust")
    participation_capacity = f(system, "participation_capacity")
    knowledge_diversity = f(system, "knowledge_diversity")
    decision_access = f(system, "decision_access")
    privacy_risk = f(system, "privacy_risk")
    community_control = f(system, "community_control")
    followthrough = f(system, "institutional_followthrough")
    equity_sensitivity = f(system, "equity_sensitivity")
    extraction_risk = f(system, "extraction_risk")

    event_by_step = {12: events[0], 27: events[1], 42: events[2], 56: events[3], 70: events[4]}
    rows = []

    for t in range(time_steps):
        event = event_by_step.get(t)
        if event:
            shock = f(event, "shock_intensity")
            participation_burden = f(event, "participation_burden")
            trust_pressure = f(event, "trust_pressure")
            information_stress = f(event, "information_stress")
            privacy_exposure = f(event, "privacy_exposure")
            decision_delay = f(event, "decision_delay")
            reciprocity_gap = f(event, "reciprocity_gap")
            accountability_gap = f(event, "accountability_gap")
            extraction_pressure = f(event, "extraction_pressure")
            event_name = event["event_name"]
        else:
            shock = 0.05 + rng.random() * 0.02
            participation_burden = 0.12 + rng.random() * 0.03
            trust_pressure = 0.10
            information_stress = 0.10
            privacy_exposure = 0.10
            decision_delay = 0.11 + 0.001 * t
            reciprocity_gap = 0.10
            accountability_gap = 0.11
            extraction_pressure = 0.12
            event_name = "background local-knowledge practice stress"

        knowledge_stress = (
            0.13 * shock
            + 0.14 * participation_burden
            + 0.14 * trust_pressure
            + 0.12 * information_stress
            + 0.15 * privacy_exposure
            + 0.12 * decision_delay
            + 0.10 * reciprocity_gap
            + 0.12 * accountability_gap
            + 0.13 * extraction_pressure
            + 0.08 * extraction_risk
        )

        protective_capacity = (
            0.15 * institutional_trust
            + 0.15 * participation_capacity
            + 0.14 * knowledge_diversity
            + 0.14 * decision_access
            + 0.15 * (1.0 - privacy_risk)
            + 0.14 * community_control
            + 0.15 * followthrough
            + 0.08 * equity_sensitivity
        )
        protective_capacity = max(0.0, min(1.0, protective_capacity))

        protection_penalty = max(0.0, privacy_risk + privacy_exposure - 1.35) * 0.10
        extraction_penalty = max(0.0, extraction_risk + extraction_pressure - 1.35) * 0.10
        participation_penalty = max(0.0, participation_burden - participation_capacity) * 0.08

        knowledge_function = (
            knowledge_function
            - 0.30 * knowledge_stress
            + 0.20 * protective_capacity
            + 0.08 * institutional_trust
            + 0.08 * participation_capacity
            + 0.08 * knowledge_diversity
            + 0.08 * decision_access
            + 0.08 * community_control
            + 0.08 * followthrough
            - protection_penalty
            - extraction_penalty
            - participation_penalty
        )
        knowledge_function = max(0.0, min(1.0, knowledge_function))

        institutional_trust = max(0.0, min(1.0, institutional_trust + 0.010 * followthrough - 0.012 * trust_pressure - 0.010 * extraction_pressure))
        extraction_risk = max(0.0, min(1.0, extraction_risk + 0.014 * extraction_pressure + 0.010 * privacy_exposure - 0.010 * community_control))
        equity_adjusted_function = max(0.0, min(1.0, knowledge_function * (0.72 + 0.28 * equity_sensitivity)))

        rows.append({
            "system_id": system["system_id"],
            "system": system["system"],
            "knowledge_context": system["knowledge_context"],
            "time": t,
            "event": event_name,
            "knowledge_stress": round(knowledge_stress, 5),
            "protective_capacity": round(protective_capacity, 5),
            "knowledge_function": round(knowledge_function, 5),
            "institutional_trust": round(institutional_trust, 5),
            "extraction_risk": round(extraction_risk, 5),
            "equity_adjusted_function": round(equity_adjusted_function, 5),
        })
    return rows

def summarize_simulation(rows):
    summary = []
    for system in sorted(set(str(row["system"]) for row in rows)):
        subset = [row for row in rows if row["system"] == system]
        function = [float(row["knowledge_function"]) for row in subset]
        equity = [float(row["equity_adjusted_function"]) for row in subset]
        extraction = [float(row["extraction_risk"]) for row in subset]
        trust = [float(row["institutional_trust"]) for row in subset]
        summary.append({
            "system": system,
            "mean_knowledge_function": round(mean(function), 5),
            "minimum_knowledge_function": round(min(function), 5),
            "final_knowledge_function": round(function[-1], 5),
            "mean_equity_adjusted_function": round(mean(equity), 5),
            "maximum_extraction_risk": round(max(extraction), 5),
            "final_extraction_risk": round(extraction[-1], 5),
            "minimum_institutional_trust": round(min(trust), 5),
            "final_institutional_trust": round(trust[-1], 5),
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
                "knowledge_integration_value": round(value, 5),
                "winner": scored[0][1]["strategy"],
            })

    robustness_rows = []
    strategy_count = len(strategies)
    for strategy in strategies:
        subset = [row for row in simulation_rows if row["strategy_id"] == strategy["strategy_id"]]
        ranks = [int(row["rank"]) for row in subset]
        values = [float(row["knowledge_integration_value"]) for row in subset]
        robustness_rows.append({
            "strategy_id": strategy["strategy_id"],
            "strategy": strategy["strategy"],
            "mean_knowledge_integration_value": round(mean(values), 5),
            "median_knowledge_integration_value": round(median(values), 5),
            "probability_ranked_first": round(100 * sum(1 for r in ranks if r == 1) / n, 2),
            "probability_top_two": round(100 * sum(1 for r in ranks if r <= 2) / n, 2),
            "probability_bottom_two": round(100 * sum(1 for r in ranks if r >= strategy_count - 1) / n, 2),
        })
    robustness_rows.sort(key=lambda row: row["probability_ranked_first"], reverse=True)
    return simulation_rows, robustness_rows

def main() -> None:
    strategies = read_csv(ROOT / "data/raw/local_knowledge_strategies.csv")
    scenarios = read_csv(ROOT / "data/raw/local_knowledge_scenarios.csv")
    systems = read_csv(ROOT / "data/raw/knowledge_systems.csv")
    events = read_csv(ROOT / "data/raw/knowledge_stress_events.csv")

    strategy_profiles = []
    for row in strategies:
        value = knowledge_integration_value(row)
        adjusted = adjusted_knowledge_value(row, value)
        strategy_profiles.append({
            "strategy_id": row["strategy_id"],
            "strategy": row["strategy"],
            "system_domain": row["system_domain"],
            "critical_function": row["critical_function"],
            "knowledge_integration_value": round(value, 5),
            "adjusted_knowledge_integration_value": round(adjusted, 5),
            "equity_adjusted_value": round(value * (0.72 + 0.028 * f(row, "participation_access")), 5),
            "participation_access": row["participation_access"],
            "knowledge_diversity": row["knowledge_diversity"],
            "decision_influence": row["decision_influence"],
            "trust_building": row["trust_building"],
            "knowledge_protection": row["knowledge_protection"],
            "reciprocity": row["reciprocity"],
            "implementation_accountability": row["implementation_accountability"],
            "implementation_burden": row["implementation_burden"],
            "diagnostic": strategy_diagnostic(row, value),
        })

    rankings = scenario_rankings(strategies, scenarios)

    dynamic_rows = []
    for idx, system in enumerate(systems):
        dynamic_rows.extend(simulate_knowledge_system_response(system, events, seed=100 + idx))
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

    write_csv(OUT_TABLES / "local_knowledge_strategy_profiles_standard.csv", strategy_profiles)
    write_csv(OUT_TABLES / "local_knowledge_strategy_rankings_standard.csv", rankings)
    write_csv(OUT_TABLES / "local_knowledge_top_rank_summary_standard.csv", top_rank_rows)
    write_csv(OUT_TABLES / "local_knowledge_dynamic_simulation_standard.csv", dynamic_rows)
    write_csv(OUT_TABLES / "local_knowledge_dynamic_summary_standard.csv", dynamic_summary)
    write_csv(OUT_TABLES / "local_knowledge_monte_carlo_standard.csv", strategy_simulation)
    write_csv(OUT_TABLES / "local_knowledge_robustness_summary_standard.csv", robustness_rows)
    write_csv(DATA_PROCESSED / "local_knowledge_strategy_profiles_standard.csv", strategy_profiles)

    print("Local knowledge workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    for row in strategy_profiles:
        print(f"  {row['strategy']}: value={row['knowledge_integration_value']} diagnostic={row['diagnostic']}")

if __name__ == "__main__":
    main()
