#!/usr/bin/env python3
# Dependency-light Strategic Slack and Resilience workflow.
# Run: python3 python/strategic_slack_resilience_standard.py

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
    "financial_slack",
    "workforce_slack",
    "operational_slack",
    "knowledge_slack",
    "network_slack",
    "governance_slack",
    "ethical_safeguards",
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

def slack_resilience_value(row: dict[str, str]) -> float:
    return (
        0.13 * f(row, "financial_slack")
        + 0.14 * f(row, "workforce_slack")
        + 0.13 * f(row, "operational_slack")
        + 0.13 * f(row, "knowledge_slack")
        + 0.13 * f(row, "network_slack")
        + 0.14 * f(row, "governance_slack")
        + 0.13 * f(row, "ethical_safeguards")
        - 0.04 * f(row, "ethical_burden")
        - 0.03 * f(row, "implementation_burden")
    )

def adjusted_slack_value(row: dict[str, str], value: float) -> float:
    workforce_gap = max(0.0, 8.2 - f(row, "workforce_slack"))
    knowledge_gap = max(0.0, 8.2 - f(row, "knowledge_slack"))
    governance_gap = max(0.0, 8.2 - f(row, "governance_slack"))
    return value - 0.07 * workforce_gap - 0.06 * knowledge_gap - 0.06 * governance_gap

def score_portfolio(row: dict[str, str], scenario: dict[str, str]) -> float:
    return (
        f(scenario, "financial_slack_weight") * f(row, "financial_slack")
        + f(scenario, "workforce_slack_weight") * f(row, "workforce_slack")
        + f(scenario, "operational_slack_weight") * f(row, "operational_slack")
        + f(scenario, "knowledge_slack_weight") * f(row, "knowledge_slack")
        + f(scenario, "network_slack_weight") * f(row, "network_slack")
        + f(scenario, "governance_slack_weight") * f(row, "governance_slack")
        + f(scenario, "ethical_safeguards_weight") * f(row, "ethical_safeguards")
        - f(scenario, "ethical_burden_weight") * f(row, "ethical_burden")
        - f(scenario, "implementation_burden_weight") * f(row, "implementation_burden")
    )

def portfolio_diagnostic(row: dict[str, str], value: float) -> str:
    if f(row, "implementation_burden") >= 3.6:
        return "implementation-burden review needed"
    if f(row, "ethical_burden") >= 3.2:
        return "ethical-burden review needed"
    if f(row, "workforce_slack") < 7.6:
        return "workforce-slack review needed"
    if f(row, "knowledge_slack") < 7.6:
        return "knowledge-slack review needed"
    if f(row, "governance_slack") < 7.8:
        return "governance-slack review needed"
    if value >= 7.25:
        return "strong strategic slack portfolio candidate"
    return "promising but requires scenario testing"

def scenario_rankings(portfolios, scenarios):
    rows = []
    for scenario in scenarios:
        scored = sorted(
            [(score_portfolio(portfolio, scenario), portfolio) for portfolio in portfolios],
            key=lambda item: item[0],
            reverse=True,
        )
        for rank, (value, portfolio) in enumerate(scored, start=1):
            rows.append({
                "scenario": scenario["scenario"],
                "portfolio_id": portfolio["portfolio_id"],
                "portfolio": portfolio["portfolio"],
                "system_domain": portfolio["system_domain"],
                "rank": rank,
                "slack_resilience_value": round(value, 5),
                "ethical_burden": portfolio["ethical_burden"],
                "implementation_burden": portfolio["implementation_burden"],
                "critical_function": portfolio["critical_function"],
            })
    return rows

def initial_slack_stock(system: dict[str, str]) -> float:
    return (
        0.16 * f(system, "financial_slack")
        + 0.16 * f(system, "workforce_slack")
        + 0.15 * f(system, "operational_slack")
        + 0.15 * f(system, "knowledge_slack")
        + 0.14 * f(system, "network_slack")
        + 0.14 * f(system, "governance_slack")
        + 0.10 * f(system, "ethical_safeguards")
    )

def simulate_slack_system(system, events, seed, time_steps=90):
    rng = random.Random(seed)
    function = f(system, "initial_function")
    strain = f(system, "initial_strain")
    slack_stock = initial_slack_stock(system)

    financial = f(system, "financial_slack")
    workforce = f(system, "workforce_slack")
    operational = f(system, "operational_slack")
    knowledge = f(system, "knowledge_slack")
    network = f(system, "network_slack")
    governance = f(system, "governance_slack")
    ethical = f(system, "ethical_safeguards")

    event_by_step = {10: events[0], 22: events[1], 35: events[2], 48: events[3], 60: events[4], 72: events[5], 82: events[6]}
    rows = []

    for t in range(time_steps):
        event = event_by_step.get(t)
        if event:
            shock = f(event, "shock_intensity")
            financial_stress = f(event, "financial_stress")
            workforce_stress = f(event, "workforce_stress")
            operational_stress = f(event, "operational_stress")
            knowledge_stress = f(event, "knowledge_stress")
            network_stress = f(event, "network_stress")
            governance_stress = f(event, "governance_stress")
            ethical_burden = f(event, "ethical_burden")
            consumption_pressure = f(event, "slack_consumption_pressure")
            event_name = event["event_name"]
        else:
            shock = 0.05 + rng.random() * 0.02
            financial_stress = 0.10
            workforce_stress = 0.10
            operational_stress = 0.10
            knowledge_stress = 0.08 + 0.001 * t
            network_stress = 0.10
            governance_stress = 0.09
            ethical_burden = 0.20
            consumption_pressure = 0.12
            event_name = "background operating pressure"

        disruption_load = (
            0.10 * shock
            + 0.13 * financial_stress
            + 0.15 * workforce_stress
            + 0.14 * operational_stress
            + 0.12 * knowledge_stress
            + 0.13 * network_stress
            + 0.11 * governance_stress
            + 0.12 * ethical_burden
        )

        adaptive_response = (
            0.13 * financial
            + 0.17 * workforce
            + 0.14 * operational
            + 0.15 * knowledge
            + 0.13 * network
            + 0.16 * governance
            + 0.12 * ethical
        )
        adaptive_response = max(0.0, min(1.0, adaptive_response))

        fragility_gap = max(0.0, disruption_load - slack_stock)

        strain_increase = 0.20 * disruption_load + 0.18 * fragility_gap
        strain_recovery = 0.10 * workforce + 0.08 * ethical + 0.04 * governance
        strain = max(0.0, min(1.0, strain + strain_increase - strain_recovery))

        function = (
            function
            - 0.34 * disruption_load
            + 0.22 * adaptive_response
            + 0.18 * slack_stock
            + 0.08 * governance
            - 0.18 * strain
            - 0.10 * fragility_gap
        )
        function = max(0.0, min(1.0, function))

        slack_consumption = 0.09 * disruption_load + 0.08 * fragility_gap + 0.05 * consumption_pressure
        slack_rebuilding = 0.020 * financial + 0.020 * governance + 0.015 * knowledge + 0.010 * network
        slack_stock = max(0.0, min(1.0, slack_stock - slack_consumption + slack_rebuilding))

        ethical_adjusted_function = max(0.0, min(1.0, function * (0.72 + 0.28 * ethical) - 0.10 * strain - 0.06 * ethical_burden))
        resilience_score = max(0.0, min(1.0,
            0.20 * function
            + 0.18 * slack_stock
            + 0.16 * adaptive_response
            + 0.14 * ethical_adjusted_function
            + 0.12 * (1.0 - strain)
            + 0.10 * governance
            + 0.10 * ethical
        ))

        rows.append({
            "system_id": system["system_id"],
            "system": system["system"],
            "system_context": system["system_context"],
            "time": t,
            "event": event_name,
            "disruption_load": round(disruption_load, 5),
            "slack_stock": round(slack_stock, 5),
            "adaptive_response": round(adaptive_response, 5),
            "fragility_gap": round(fragility_gap, 5),
            "workforce_strain": round(strain, 5),
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
        slack = [float(row["slack_stock"]) for row in subset]
        strain = [float(row["workforce_strain"]) for row in subset]
        gap = [float(row["fragility_gap"]) for row in subset]
        ethical = [float(row["ethical_adjusted_function"]) for row in subset]
        score = [float(row["resilience_score"]) for row in subset]
        summary.append({
            "system": system,
            "mean_function": round(mean(function), 5),
            "minimum_function": round(min(function), 5),
            "final_function": round(function[-1], 5),
            "mean_slack_stock": round(mean(slack), 5),
            "minimum_slack_stock": round(min(slack), 5),
            "final_slack_stock": round(slack[-1], 5),
            "maximum_workforce_strain": round(max(strain), 5),
            "mean_fragility_gap": round(mean(gap), 5),
            "final_ethical_adjusted_function": round(ethical[-1], 5),
            "final_resilience_score": round(score[-1], 5),
        })
    summary.sort(key=lambda row: row["final_resilience_score"], reverse=True)
    return summary

def portfolio_monte_carlo(portfolios, scenario, n=3000):
    rng = random.Random(42)
    simulation_rows = []
    for simulation_id in range(n):
        scored = []
        for portfolio in portfolios:
            sampled = dict(portfolio)
            for criterion in BENEFIT_CRITERIA + ["ethical_burden", "implementation_burden"]:
                sampled[criterion] = str(max(1.0, min(10.0, f(portfolio, criterion) + rng.gauss(0, 0.55))))
            scored.append((score_portfolio(sampled, scenario), portfolio))
        scored.sort(key=lambda item: item[0], reverse=True)
        for rank, (value, portfolio) in enumerate(scored, start=1):
            simulation_rows.append({
                "simulation_id": simulation_id,
                "portfolio_id": portfolio["portfolio_id"],
                "portfolio": portfolio["portfolio"],
                "rank": rank,
                "slack_resilience_value": round(value, 5),
                "winner": scored[0][1]["portfolio"],
            })

    robustness_rows = []
    portfolio_count = len(portfolios)
    for portfolio in portfolios:
        subset = [row for row in simulation_rows if row["portfolio_id"] == portfolio["portfolio_id"]]
        ranks = [int(row["rank"]) for row in subset]
        values = [float(row["slack_resilience_value"]) for row in subset]
        robustness_rows.append({
            "portfolio_id": portfolio["portfolio_id"],
            "portfolio": portfolio["portfolio"],
            "mean_slack_resilience_value": round(mean(values), 5),
            "median_slack_resilience_value": round(median(values), 5),
            "probability_ranked_first": round(100 * sum(1 for r in ranks if r == 1) / n, 2),
            "probability_top_two": round(100 * sum(1 for r in ranks if r <= 2) / n, 2),
            "probability_bottom_two": round(100 * sum(1 for r in ranks if r >= portfolio_count - 1) / n, 2),
        })
    robustness_rows.sort(key=lambda row: row["probability_ranked_first"], reverse=True)
    return simulation_rows, robustness_rows

def main() -> None:
    portfolios = read_csv(ROOT / "data/raw/strategic_slack_portfolios.csv")
    scenarios = read_csv(ROOT / "data/raw/strategic_slack_scenarios.csv")
    systems = read_csv(ROOT / "data/raw/slack_system_profiles.csv")
    events = read_csv(ROOT / "data/raw/slack_disruption_events.csv")

    portfolio_profiles = []
    for row in portfolios:
        value = slack_resilience_value(row)
        adjusted = adjusted_slack_value(row, value)
        portfolio_profiles.append({
            "portfolio_id": row["portfolio_id"],
            "portfolio": row["portfolio"],
            "system_domain": row["system_domain"],
            "critical_function": row["critical_function"],
            "slack_resilience_value": round(value, 5),
            "adjusted_slack_resilience_value": round(adjusted, 5),
            "ethical_adjusted_value": round(value * (0.72 + 0.028 * f(row, "ethical_safeguards") - 0.010 * f(row, "ethical_burden")), 5),
            "financial_slack": row["financial_slack"],
            "workforce_slack": row["workforce_slack"],
            "operational_slack": row["operational_slack"],
            "knowledge_slack": row["knowledge_slack"],
            "network_slack": row["network_slack"],
            "governance_slack": row["governance_slack"],
            "ethical_safeguards": row["ethical_safeguards"],
            "ethical_burden": row["ethical_burden"],
            "implementation_burden": row["implementation_burden"],
            "diagnostic": portfolio_diagnostic(row, value),
        })

    rankings = scenario_rankings(portfolios, scenarios)

    dynamic_rows = []
    for idx, system in enumerate(systems):
        dynamic_rows.extend(simulate_slack_system(system, events, seed=100 + idx))
    dynamic_summary = summarize_simulation(dynamic_rows)

    baseline = next(s for s in scenarios if s["scenario"] == "Balanced")
    portfolio_simulation, robustness_rows = portfolio_monte_carlo(portfolios, baseline, n=3000)

    first_place_summary = {}
    for row in rankings:
        if int(row["rank"]) == 1:
            first_place_summary[row["portfolio"]] = first_place_summary.get(row["portfolio"], 0) + 1

    top_rank_rows = [
        {"portfolio": portfolio, "times_ranked_first": count}
        for portfolio, count in sorted(first_place_summary.items(), key=lambda item: item[1], reverse=True)
    ]

    write_csv(OUT_TABLES / "strategic_slack_portfolio_profiles_standard.csv", portfolio_profiles)
    write_csv(OUT_TABLES / "strategic_slack_portfolio_rankings_standard.csv", rankings)
    write_csv(OUT_TABLES / "strategic_slack_top_rank_summary_standard.csv", top_rank_rows)
    write_csv(OUT_TABLES / "strategic_slack_dynamic_simulation_standard.csv", dynamic_rows)
    write_csv(OUT_TABLES / "strategic_slack_dynamic_summary_standard.csv", dynamic_summary)
    write_csv(OUT_TABLES / "strategic_slack_monte_carlo_standard.csv", portfolio_simulation)
    write_csv(OUT_TABLES / "strategic_slack_robustness_summary_standard.csv", robustness_rows)
    write_csv(DATA_PROCESSED / "strategic_slack_portfolio_profiles_standard.csv", portfolio_profiles)

    print("Strategic slack resilience workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    for row in portfolio_profiles:
        print(f"  {row['portfolio']}: value={row['slack_resilience_value']} diagnostic={row['diagnostic']}")

if __name__ == "__main__":
    main()
