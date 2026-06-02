#!/usr/bin/env python3
# Dependency-light Small Business and Local Economic Resilience workflow.
# Run: python3 python/small_business_local_resilience_standard.py

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
    "liquidity_support",
    "workforce_capacity",
    "supply_resilience",
    "digital_readiness",
    "public_capacity",
    "community_wealth",
    "equity_access",
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

def local_resilience_value(row: dict[str, str]) -> float:
    return (
        0.14 * f(row, "liquidity_support")
        + 0.14 * f(row, "workforce_capacity")
        + 0.12 * f(row, "supply_resilience")
        + 0.12 * f(row, "digital_readiness")
        + 0.14 * f(row, "public_capacity")
        + 0.15 * f(row, "community_wealth")
        + 0.16 * f(row, "equity_access")
        - 0.07 * f(row, "inequality_risk")
        - 0.06 * f(row, "implementation_burden")
    )

def adjusted_local_value(row: dict[str, str], value: float) -> float:
    equity_gap = max(0.0, 8.5 - f(row, "equity_access"))
    liquidity_gap = max(0.0, 8.0 - f(row, "liquidity_support"))
    workforce_gap = max(0.0, 8.0 - f(row, "workforce_capacity"))
    return value - 0.08 * equity_gap - 0.06 * liquidity_gap - 0.06 * workforce_gap

def score_strategy(row: dict[str, str], scenario: dict[str, str]) -> float:
    return (
        f(scenario, "liquidity_support_weight") * f(row, "liquidity_support")
        + f(scenario, "workforce_capacity_weight") * f(row, "workforce_capacity")
        + f(scenario, "supply_resilience_weight") * f(row, "supply_resilience")
        + f(scenario, "digital_readiness_weight") * f(row, "digital_readiness")
        + f(scenario, "public_capacity_weight") * f(row, "public_capacity")
        + f(scenario, "community_wealth_weight") * f(row, "community_wealth")
        + f(scenario, "equity_access_weight") * f(row, "equity_access")
        - f(scenario, "inequality_risk_weight") * f(row, "inequality_risk")
        - f(scenario, "implementation_burden_weight") * f(row, "implementation_burden")
    )

def strategy_diagnostic(row: dict[str, str], value: float) -> str:
    if f(row, "implementation_burden") >= 3.7:
        return "implementation-burden review needed"
    if f(row, "inequality_risk") >= 3.1:
        return "inequality-risk review needed"
    if f(row, "liquidity_support") < 7.6:
        return "liquidity-support review needed"
    if f(row, "workforce_capacity") < 7.6:
        return "workforce-capacity review needed"
    if f(row, "equity_access") < 8.3:
        return "equity-access review needed"
    if value >= 7.35:
        return "strong local resilience strategy candidate"
    return "promising but requires local validation"

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
                "local_resilience_value": round(value, 5),
                "inequality_risk": strategy["inequality_risk"],
                "implementation_burden": strategy["implementation_burden"],
                "critical_function": strategy["critical_function"],
            })
    return rows

def simulate_business(business, events, seed, time_steps=96):
    rng = random.Random(seed)
    function = f(business, "initial_function")
    cash = f(business, "cash_runway")
    owner_strain = f(business, "initial_owner_strain")
    customer_demand = min(1.0, 0.72 + 0.10 * f(business, "community_embeddedness"))

    workforce = f(business, "workforce_capacity")
    supplier = f(business, "supplier_resilience")
    digital = f(business, "digital_readiness")
    community = f(business, "community_embeddedness")
    public_support = f(business, "public_support_access")
    equity = f(business, "equity_access")

    event_by_step = {8: events[0], 20: events[1], 35: events[2], 50: events[3], 66: events[4], 78: events[5], 88: events[6]}
    rows = []

    for t in range(time_steps):
        event = event_by_step.get(t)
        if event:
            shock = f(event, "shock_intensity")
            demand_loss = f(event, "demand_loss")
            supplier_disruption = f(event, "supplier_disruption")
            digital_disruption = f(event, "digital_disruption")
            rent_debt_pressure = f(event, "rent_debt_pressure")
            workforce_stress = f(event, "workforce_stress")
            insurance_gap = f(event, "insurance_gap")
            support_delay = f(event, "public_support_delay")
            inequality_pressure = f(event, "inequality_pressure")
            event_name = event["event_name"]
        else:
            shock = 0.05 + rng.random() * 0.02
            demand_loss = 0.10
            supplier_disruption = 0.08
            digital_disruption = 0.07
            rent_debt_pressure = 0.10 + 0.001 * t
            workforce_stress = 0.09
            insurance_gap = 0.08
            support_delay = 0.10
            inequality_pressure = 0.12
            event_name = "background local volatility"

        adaptive_capacity = (
            0.16 * cash
            + 0.16 * workforce
            + 0.14 * supplier
            + 0.14 * digital
            + 0.16 * community
            + 0.14 * public_support
            + 0.10 * equity
        )

        shock_load = (
            0.12 * shock
            + 0.15 * demand_loss
            + 0.13 * supplier_disruption
            + 0.12 * digital_disruption
            + 0.15 * rent_debt_pressure
            + 0.13 * workforce_stress
            + 0.10 * insurance_gap
            + 0.10 * support_delay
        )

        fragility_gap = max(0.0, shock_load - adaptive_capacity)

        revenue_pressure = (
            0.28 * shock_load
            + 0.18 * fragility_gap
            - 0.08 * community
            - 0.06 * digital
        )
        revenue_pressure = max(0.0, min(1.0, revenue_pressure))

        customer_demand = max(0.0, min(1.0, customer_demand - 0.16 * demand_loss + 0.06 * community + 0.03 * digital))

        cash = max(0.0, min(1.0, cash - 0.14 * revenue_pressure - 0.06 * rent_debt_pressure - 0.04 * insurance_gap + 0.07 * public_support + 0.04 * equity))

        strain_increase = 0.18 * shock_load + 0.15 * fragility_gap + 0.08 * max(0.0, 0.45 - cash)
        strain_recovery = 0.08 * workforce + 0.05 * community + 0.03 * public_support
        owner_strain = max(0.0, min(1.0, owner_strain + strain_increase - strain_recovery))

        function = (
            function
            - 0.30 * shock_load
            - 0.16 * fragility_gap
            + 0.16 * adaptive_capacity
            + 0.12 * cash
            + 0.09 * customer_demand
            - 0.10 * owner_strain
        )
        function = max(0.0, min(1.0, function))

        equity_adjusted_function = max(0.0, min(1.0, function * (0.72 + 0.28 * equity) - 0.08 * owner_strain - 0.05 * inequality_pressure))
        survival_risk = max(0.0, min(1.0, 0.35 * (1.0 - function) + 0.35 * (1.0 - cash) + 0.20 * owner_strain + 0.10 * fragility_gap))

        rows.append({
            "business_id": business["business_id"],
            "business": business["business"],
            "business_context": business["business_context"],
            "time": t,
            "event": event_name,
            "shock_load": round(shock_load, 5),
            "adaptive_capacity": round(adaptive_capacity, 5),
            "fragility_gap": round(fragility_gap, 5),
            "function": round(function, 5),
            "cash_runway": round(cash, 5),
            "customer_demand": round(customer_demand, 5),
            "owner_strain": round(owner_strain, 5),
            "equity_adjusted_function": round(equity_adjusted_function, 5),
            "survival_risk": round(survival_risk, 5),
        })
    return rows

def summarize_simulation(rows):
    summary = []
    for business in sorted(set(str(row["business"]) for row in rows)):
        subset = [row for row in rows if row["business"] == business]
        function = [float(row["function"]) for row in subset]
        cash = [float(row["cash_runway"]) for row in subset]
        strain = [float(row["owner_strain"]) for row in subset]
        gap = [float(row["fragility_gap"]) for row in subset]
        equity_function = [float(row["equity_adjusted_function"]) for row in subset]
        risk = [float(row["survival_risk"]) for row in subset]
        summary.append({
            "business": business,
            "mean_function": round(mean(function), 5),
            "minimum_function": round(min(function), 5),
            "final_function": round(function[-1], 5),
            "minimum_cash_runway": round(min(cash), 5),
            "final_cash_runway": round(cash[-1], 5),
            "maximum_owner_strain": round(max(strain), 5),
            "mean_fragility_gap": round(mean(gap), 5),
            "final_equity_adjusted_function": round(equity_function[-1], 5),
            "maximum_survival_risk": round(max(risk), 5),
            "final_survival_risk": round(risk[-1], 5),
        })
    summary.sort(key=lambda row: row["final_equity_adjusted_function"], reverse=True)
    return summary

def strategy_monte_carlo(strategies, scenario, n=3000):
    rng = random.Random(42)
    simulation_rows = []
    for simulation_id in range(n):
        scored = []
        for strategy in strategies:
            sampled = dict(strategy)
            for criterion in BENEFIT_CRITERIA + ["inequality_risk", "implementation_burden"]:
                sampled[criterion] = str(max(1.0, min(10.0, f(strategy, criterion) + rng.gauss(0, 0.55))))
            scored.append((score_strategy(sampled, scenario), strategy))
        scored.sort(key=lambda item: item[0], reverse=True)
        for rank, (value, strategy) in enumerate(scored, start=1):
            simulation_rows.append({
                "simulation_id": simulation_id,
                "strategy_id": strategy["strategy_id"],
                "strategy": strategy["strategy"],
                "rank": rank,
                "local_resilience_value": round(value, 5),
                "winner": scored[0][1]["strategy"],
            })

    robustness_rows = []
    strategy_count = len(strategies)
    for strategy in strategies:
        subset = [row for row in simulation_rows if row["strategy_id"] == strategy["strategy_id"]]
        ranks = [int(row["rank"]) for row in subset]
        values = [float(row["local_resilience_value"]) for row in subset]
        robustness_rows.append({
            "strategy_id": strategy["strategy_id"],
            "strategy": strategy["strategy"],
            "mean_local_resilience_value": round(mean(values), 5),
            "median_local_resilience_value": round(median(values), 5),
            "probability_ranked_first": round(100 * sum(1 for r in ranks if r == 1) / n, 2),
            "probability_top_two": round(100 * sum(1 for r in ranks if r <= 2) / n, 2),
            "probability_bottom_two": round(100 * sum(1 for r in ranks if r >= strategy_count - 1) / n, 2),
        })
    robustness_rows.sort(key=lambda row: row["probability_ranked_first"], reverse=True)
    return simulation_rows, robustness_rows

def main() -> None:
    strategies = read_csv(ROOT / "data/raw/local_economic_resilience_strategies.csv")
    scenarios = read_csv(ROOT / "data/raw/local_resilience_scenarios.csv")
    businesses = read_csv(ROOT / "data/raw/small_business_profiles.csv")
    events = read_csv(ROOT / "data/raw/local_disruption_events.csv")

    strategy_profiles = []
    for row in strategies:
        value = local_resilience_value(row)
        adjusted = adjusted_local_value(row, value)
        strategy_profiles.append({
            "strategy_id": row["strategy_id"],
            "strategy": row["strategy"],
            "system_domain": row["system_domain"],
            "critical_function": row["critical_function"],
            "local_resilience_value": round(value, 5),
            "adjusted_local_resilience_value": round(adjusted, 5),
            "equity_adjusted_value": round(value * (0.72 + 0.028 * f(row, "equity_access") - 0.010 * f(row, "inequality_risk")), 5),
            "liquidity_support": row["liquidity_support"],
            "workforce_capacity": row["workforce_capacity"],
            "supply_resilience": row["supply_resilience"],
            "digital_readiness": row["digital_readiness"],
            "public_capacity": row["public_capacity"],
            "community_wealth": row["community_wealth"],
            "equity_access": row["equity_access"],
            "inequality_risk": row["inequality_risk"],
            "implementation_burden": row["implementation_burden"],
            "diagnostic": strategy_diagnostic(row, value),
        })

    rankings = scenario_rankings(strategies, scenarios)

    dynamic_rows = []
    for idx, business in enumerate(businesses):
        dynamic_rows.extend(simulate_business(business, events, seed=100 + idx))
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

    write_csv(OUT_TABLES / "local_economic_resilience_strategy_profiles_standard.csv", strategy_profiles)
    write_csv(OUT_TABLES / "local_economic_resilience_strategy_rankings_standard.csv", rankings)
    write_csv(OUT_TABLES / "local_economic_resilience_top_rank_summary_standard.csv", top_rank_rows)
    write_csv(OUT_TABLES / "small_business_resilience_dynamic_simulation_standard.csv", dynamic_rows)
    write_csv(OUT_TABLES / "small_business_resilience_dynamic_summary_standard.csv", dynamic_summary)
    write_csv(OUT_TABLES / "local_economic_resilience_monte_carlo_standard.csv", strategy_simulation)
    write_csv(OUT_TABLES / "local_economic_resilience_robustness_summary_standard.csv", robustness_rows)
    write_csv(DATA_PROCESSED / "local_economic_resilience_strategy_profiles_standard.csv", strategy_profiles)

    print("Small business and local economic resilience workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    for row in strategy_profiles:
        print(f"  {row['strategy']}: value={row['local_resilience_value']} diagnostic={row['diagnostic']}")

if __name__ == "__main__":
    main()
