#!/usr/bin/env python3
# Dependency-light AI and Resilience Thinking workflow.
# Run: python3 python/ai_resilience_thinking_standard.py

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
    "forecasting_value",
    "scenario_value",
    "decision_support",
    "governance_quality",
    "equity_safeguards",
    "human_oversight",
    "local_knowledge",
    "security_resilience",
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

def ai_resilience_value(row: dict[str, str]) -> float:
    return (
        0.11 * f(row, "monitoring_value")
        + 0.10 * f(row, "forecasting_value")
        + 0.11 * f(row, "scenario_value")
        + 0.11 * f(row, "decision_support")
        + 0.12 * f(row, "governance_quality")
        + 0.12 * f(row, "equity_safeguards")
        + 0.12 * f(row, "human_oversight")
        + 0.10 * f(row, "local_knowledge")
        + 0.10 * f(row, "security_resilience")
        - 0.05 * f(row, "ai_risk")
        - 0.04 * f(row, "implementation_burden")
    )

def adjusted_ai_value(row: dict[str, str], value: float) -> float:
    governance_gap = max(0.0, 8.5 - f(row, "governance_quality"))
    equity_gap = max(0.0, 8.5 - f(row, "equity_safeguards"))
    human_gap = max(0.0, 8.5 - f(row, "human_oversight"))
    local_gap = max(0.0, 8.2 - f(row, "local_knowledge"))
    security_gap = max(0.0, 8.3 - f(row, "security_resilience"))
    return value - 0.07 * governance_gap - 0.08 * equity_gap - 0.08 * human_gap - 0.06 * local_gap - 0.06 * security_gap

def score_strategy(row: dict[str, str], scenario: dict[str, str]) -> float:
    return (
        f(scenario, "monitoring_value_weight") * f(row, "monitoring_value")
        + f(scenario, "forecasting_value_weight") * f(row, "forecasting_value")
        + f(scenario, "scenario_value_weight") * f(row, "scenario_value")
        + f(scenario, "decision_support_weight") * f(row, "decision_support")
        + f(scenario, "governance_quality_weight") * f(row, "governance_quality")
        + f(scenario, "equity_safeguards_weight") * f(row, "equity_safeguards")
        + f(scenario, "human_oversight_weight") * f(row, "human_oversight")
        + f(scenario, "local_knowledge_weight") * f(row, "local_knowledge")
        + f(scenario, "security_resilience_weight") * f(row, "security_resilience")
        - f(scenario, "ai_risk_weight") * f(row, "ai_risk")
        - f(scenario, "implementation_burden_weight") * f(row, "implementation_burden")
    )

def strategy_diagnostic(row: dict[str, str], value: float) -> str:
    if f(row, "implementation_burden") >= 3.8:
        return "implementation-burden review needed"
    if f(row, "ai_risk") >= 3.2:
        return "AI-risk review needed"
    if f(row, "equity_safeguards") < 8.0:
        return "equity-safeguards review needed"
    if f(row, "human_oversight") < 8.1:
        return "human-oversight review needed"
    if f(row, "local_knowledge") < 8.0:
        return "local-knowledge review needed"
    if f(row, "governance_quality") < 8.1:
        return "governance review needed"
    if value >= 7.55:
        return "strong AI-enabled resilience strategy candidate"
    return "promising but requires participatory validation"

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
                "ai_resilience_value": round(value, 5),
                "ai_risk": strategy["ai_risk"],
                "implementation_burden": strategy["implementation_burden"],
                "critical_function": strategy["critical_function"],
            })
    return rows

def simulate_ai_system(system, events, seed, time_steps=96):
    rng = random.Random(seed)
    function = f(system, "initial_function")
    ai_risk = f(system, "initial_ai_risk")
    drift = f(system, "initial_model_drift")
    human_strain = f(system, "initial_human_strain")

    baseline = f(system, "baseline_resilience")
    monitoring = f(system, "ai_monitoring")
    forecasting = f(system, "ai_forecasting")
    scenario = f(system, "scenario_capacity")
    decision = f(system, "decision_support")
    governance = f(system, "governance")
    equity = f(system, "equity_safeguards")
    human = f(system, "human_oversight")
    local = f(system, "local_knowledge")
    security = f(system, "security_resilience")

    event_by_step = {10: events[0], 22: events[1], 34: events[2], 46: events[3], 60: events[4], 72: events[5], 84: events[6], 90: events[7]}
    rows = []

    for t in range(time_steps):
        event = event_by_step.get(t)
        if event:
            shock = f(event, "shock_intensity")
            climate_infra = f(event, "climate_infrastructure_stress")
            data_shift = f(event, "data_shift_stress")
            public_trust = f(event, "public_trust_stress")
            cyber = f(event, "cyber_adversarial_stress")
            resource = f(event, "resource_constraint_stress")
            institutional = f(event, "institutional_learning_stress")
            equity_pressure = f(event, "equity_pressure")
            drift_pressure = f(event, "model_drift_pressure")
            event_name = event["event_name"]
        else:
            shock = 0.05 + rng.random() * 0.02
            climate_infra = 0.09
            data_shift = 0.08 + 0.001 * t
            public_trust = 0.08
            cyber = 0.08
            resource = 0.10
            institutional = 0.08
            equity_pressure = 0.10
            drift_pressure = 0.08 + 0.0015 * t
            event_name = "background system pressure"

        disturbance = (
            0.12 * shock
            + 0.13 * climate_infra
            + 0.13 * data_shift
            + 0.12 * public_trust
            + 0.13 * cyber
            + 0.13 * resource
            + 0.11 * institutional
            + 0.12 * equity_pressure
            + 0.11 * drift_pressure
        )

        ai_support = (
            0.17 * monitoring
            + 0.15 * forecasting
            + 0.15 * scenario
            + 0.15 * decision
            + 0.11 * governance
            + 0.09 * human
            + 0.08 * equity
            + 0.05 * local
            + 0.05 * security
        )
        ai_support = max(0.0, min(1.0, ai_support))

        governance_buffer = (
            0.25 * governance
            + 0.21 * human
            + 0.20 * equity
            + 0.16 * security
            + 0.12 * local
            + 0.06 * scenario
        )
        governance_buffer = max(0.0, min(1.0, governance_buffer))

        drift_growth = 0.020 * disturbance + 0.022 * drift_pressure + 0.016 * (1.0 - local) + 0.012 * (1.0 - monitoring)
        drift_control = 0.035 * governance + 0.025 * human + 0.020 * scenario + 0.016 * local
        drift = max(0.0, min(1.0, drift + drift_growth - drift_control))

        ai_risk_growth = 0.025 * disturbance + 0.035 * drift + 0.025 * (1.0 - governance) + 0.024 * (1.0 - equity) + 0.018 * cyber
        ai_risk_control = 0.035 * governance + 0.025 * security + 0.025 * human + 0.014 * local
        ai_risk = max(0.0, min(1.0, ai_risk + ai_risk_growth - ai_risk_control))

        fragility_gap = max(0.0, disturbance + 0.34 * ai_risk + 0.25 * drift - governance_buffer)

        strain_increase = 0.17 * disturbance + 0.15 * fragility_gap + 0.09 * ai_risk + 0.05 * resource
        strain_recovery = 0.08 * human + 0.06 * local + 0.05 * governance
        human_strain = max(0.0, min(1.0, human_strain + strain_increase - strain_recovery))

        equity_performance = max(0.0, min(1.0,
            0.36 * equity
            + 0.20 * local
            + 0.17 * governance
            + 0.11 * human
            + 0.08 * security
            - 0.12 * ai_risk
            - 0.10 * drift
            - 0.08 * equity_pressure
        ))

        function = (
            function
            - 0.28 * disturbance
            - 0.15 * fragility_gap
            + 0.16 * baseline
            + 0.18 * ai_support
            + 0.12 * governance_buffer
            + 0.10 * equity_performance
            - 0.11 * human_strain
        )
        function = max(0.0, min(1.0, function))

        ethical_adjusted_function = max(0.0, min(1.0, function * (0.70 + 0.30 * equity_performance) - 0.08 * human_strain - 0.08 * ai_risk))
        resilience_score = max(0.0, min(1.0,
            0.17 * function
            + 0.15 * baseline
            + 0.15 * ai_support
            + 0.13 * governance_buffer
            + 0.12 * equity_performance
            + 0.10 * (1.0 - ai_risk)
            + 0.08 * (1.0 - drift)
            + 0.06 * (1.0 - human_strain)
            + 0.04 * local
        ))

        rows.append({
            "system_id": system["system_id"],
            "system": system["system"],
            "system_context": system["system_context"],
            "time": t,
            "event": event_name,
            "disturbance": round(disturbance, 5),
            "ai_support": round(ai_support, 5),
            "governance_buffer": round(governance_buffer, 5),
            "model_drift": round(drift, 5),
            "ai_risk": round(ai_risk, 5),
            "fragility_gap": round(fragility_gap, 5),
            "human_strain": round(human_strain, 5),
            "equity_performance": round(equity_performance, 5),
            "function": round(function, 5),
            "ethical_adjusted_function": round(ethical_adjusted_function, 5),
            "resilience_score": round(resilience_score, 5),
        })
    return rows

def summarize_simulation(rows):
    summary = []
    for system in sorted(set(str(row["system"]) for row in rows)):
        subset = [row for row in rows if row["system"] == system]
        function = [float(row["function"]) for row in subset]
        drift = [float(row["model_drift"]) for row in subset]
        risk = [float(row["ai_risk"]) for row in subset]
        strain = [float(row["human_strain"]) for row in subset]
        equity = [float(row["equity_performance"]) for row in subset]
        gap = [float(row["fragility_gap"]) for row in subset]
        ethical = [float(row["ethical_adjusted_function"]) for row in subset]
        score = [float(row["resilience_score"]) for row in subset]
        summary.append({
            "system": system,
            "mean_function": round(mean(function), 5),
            "minimum_function": round(min(function), 5),
            "final_function": round(function[-1], 5),
            "final_model_drift": round(drift[-1], 5),
            "final_ai_risk": round(risk[-1], 5),
            "maximum_human_strain": round(max(strain), 5),
            "mean_equity_performance": round(mean(equity), 5),
            "mean_fragility_gap": round(mean(gap), 5),
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
            for criterion in BENEFIT_CRITERIA + ["ai_risk", "implementation_burden"]:
                sampled[criterion] = str(max(1.0, min(10.0, f(strategy, criterion) + rng.gauss(0, 0.55))))
            scored.append((score_strategy(sampled, scenario), strategy))
        scored.sort(key=lambda item: item[0], reverse=True)
        for rank, (value, strategy) in enumerate(scored, start=1):
            simulation_rows.append({
                "simulation_id": simulation_id,
                "strategy_id": strategy["strategy_id"],
                "strategy": strategy["strategy"],
                "rank": rank,
                "ai_resilience_value": round(value, 5),
                "winner": scored[0][1]["strategy"],
            })

    robustness_rows = []
    strategy_count = len(strategies)
    for strategy in strategies:
        subset = [row for row in simulation_rows if row["strategy_id"] == strategy["strategy_id"]]
        ranks = [int(row["rank"]) for row in subset]
        values = [float(row["ai_resilience_value"]) for row in subset]
        robustness_rows.append({
            "strategy_id": strategy["strategy_id"],
            "strategy": strategy["strategy"],
            "mean_ai_resilience_value": round(mean(values), 5),
            "median_ai_resilience_value": round(median(values), 5),
            "probability_ranked_first": round(100 * sum(1 for r in ranks if r == 1) / n, 2),
            "probability_top_two": round(100 * sum(1 for r in ranks if r <= 2) / n, 2),
            "probability_bottom_two": round(100 * sum(1 for r in ranks if r >= strategy_count - 1) / n, 2),
        })
    robustness_rows.sort(key=lambda row: row["probability_ranked_first"], reverse=True)
    return simulation_rows, robustness_rows

def main() -> None:
    strategies = read_csv(ROOT / "data/raw/ai_resilience_strategies.csv")
    scenarios = read_csv(ROOT / "data/raw/ai_resilience_scenarios.csv")
    systems = read_csv(ROOT / "data/raw/ai_enabled_resilience_systems.csv")
    events = read_csv(ROOT / "data/raw/ai_resilience_disruption_events.csv")

    strategy_profiles = []
    for row in strategies:
        value = ai_resilience_value(row)
        adjusted = adjusted_ai_value(row, value)
        strategy_profiles.append({
            "strategy_id": row["strategy_id"],
            "strategy": row["strategy"],
            "system_domain": row["system_domain"],
            "critical_function": row["critical_function"],
            "ai_resilience_value": round(value, 5),
            "adjusted_ai_resilience_value": round(adjusted, 5),
            "human_and_equity_adjusted_value": round(value * (0.70 + 0.020 * f(row, "human_oversight") + 0.020 * f(row, "equity_safeguards") - 0.010 * f(row, "ai_risk")), 5),
            "monitoring_value": row["monitoring_value"],
            "forecasting_value": row["forecasting_value"],
            "scenario_value": row["scenario_value"],
            "decision_support": row["decision_support"],
            "governance_quality": row["governance_quality"],
            "equity_safeguards": row["equity_safeguards"],
            "human_oversight": row["human_oversight"],
            "local_knowledge": row["local_knowledge"],
            "security_resilience": row["security_resilience"],
            "ai_risk": row["ai_risk"],
            "implementation_burden": row["implementation_burden"],
            "diagnostic": strategy_diagnostic(row, value),
        })

    rankings = scenario_rankings(strategies, scenarios)

    dynamic_rows = []
    for idx, system in enumerate(systems):
        dynamic_rows.extend(simulate_ai_system(system, events, seed=100 + idx))
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

    write_csv(OUT_TABLES / "ai_resilience_strategy_profiles_standard.csv", strategy_profiles)
    write_csv(OUT_TABLES / "ai_resilience_strategy_rankings_standard.csv", rankings)
    write_csv(OUT_TABLES / "ai_resilience_top_rank_summary_standard.csv", top_rank_rows)
    write_csv(OUT_TABLES / "ai_resilience_dynamic_simulation_standard.csv", dynamic_rows)
    write_csv(OUT_TABLES / "ai_resilience_dynamic_summary_standard.csv", dynamic_summary)
    write_csv(OUT_TABLES / "ai_resilience_monte_carlo_standard.csv", strategy_simulation)
    write_csv(OUT_TABLES / "ai_resilience_robustness_summary_standard.csv", robustness_rows)
    write_csv(DATA_PROCESSED / "ai_resilience_strategy_profiles_standard.csv", strategy_profiles)

    print("AI and resilience thinking workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    for row in strategy_profiles:
        print(f"  {row['strategy']}: value={row['ai_resilience_value']} diagnostic={row['diagnostic']}")

if __name__ == "__main__":
    main()
