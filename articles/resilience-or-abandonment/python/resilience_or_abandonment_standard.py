#!/usr/bin/env python3
from __future__ import annotations

import csv
import random
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "tables"
OUT.mkdir(parents=True, exist_ok=True)

BENEFITS = [
    "protective_effectiveness",
    "material_support",
    "accessible_recovery",
    "governance_inclusion",
    "transformation_potential",
    "exposure_reduction",
]
PENALTIES = ["burden_shift", "implementation_burden"]

def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(path, rows):
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

def x(row, key):
    return float(row[key])

def score(row, weights):
    value = 0.0
    for col in BENEFITS:
        value += x(weights, f"{col}_weight") * x(row, col)
    for col in PENALTIES:
        value -= x(weights, f"{col}_weight") * x(row, col)

    support_gap = max(0.0, 8.0 - x(row, "material_support"))
    recovery_gap = max(0.0, 8.0 - x(row, "accessible_recovery"))
    governance_gap = max(0.0, 8.0 - x(row, "governance_inclusion"))
    exposure_gap = max(0.0, 8.0 - x(row, "exposure_reduction"))

    abandonment_risk = (
        0.32 * support_gap
        + 0.24 * recovery_gap
        + 0.22 * governance_gap
        + 0.14 * x(row, "burden_shift")
        + 0.08 * exposure_gap
    )
    adjusted = value - abandonment_risk
    return value, adjusted, abandonment_risk

def diagnostic(row, abandonment_risk):
    if abandonment_risk >= 2.4:
        return "high abandonment-risk review needed"
    if x(row, "burden_shift") >= 5.5:
        return "burden-shifting review needed"
    if x(row, "material_support") < 6.0:
        return "material-support gap"
    if x(row, "accessible_recovery") < 6.0:
        return "recovery-access gap"
    if x(row, "governance_inclusion") < 6.0:
        return "participation and authority gap"
    return "support-oriented resilience candidate"

def rankings(strategies, scenarios):
    rows = []
    for scenario in scenarios:
        scored = []
        for strategy in strategies:
            raw, adjusted, risk = score(strategy, scenario)
            scored.append((adjusted, raw, risk, strategy))
        scored.sort(reverse=True, key=lambda item: item[0])
        for rank, (adjusted, raw, risk, strategy) in enumerate(scored, start=1):
            rows.append({
                "scenario": scenario["scenario"],
                "strategy_id": strategy["strategy_id"],
                "strategy": strategy["strategy"],
                "rank": rank,
                "support_resilience_value": round(raw, 5),
                "abandonment_risk": round(risk, 5),
                "adjusted_value": round(adjusted, 5),
                "diagnostic": diagnostic(strategy, risk),
                "critical_function": strategy["critical_function"],
            })
    return rows

def simulate_pathway(row, steps=60):
    rng = random.Random(42 + int(row["pathway_id"].replace("AP", "")))
    exposure = x(row, "initial_exposure")
    support = x(row, "material_support")
    recovery = x(row, "accessible_recovery")
    governance = x(row, "governance_inclusion")
    public_capacity = x(row, "public_capacity")
    burden = x(row, "burden_shift")
    transformation = x(row, "transformation")
    trust = 0.50

    rows = []
    shocks = {10: 0.32, 22: 0.36, 36: 0.38, 50: 0.40}

    for t in range(steps):
        shock = shocks.get(t, 0.04 + rng.random() * 0.02)
        climate_pressure = 0.18 + 0.008 * t + 0.25 * shock
        infrastructure_pressure = 0.20 + 0.006 * t + 0.20 * shock

        exposure = max(0.0, min(1.0, exposure + 0.04 * climate_pressure + 0.03 * infrastructure_pressure - 0.08 * transformation - 0.06 * public_capacity))
        recovery = max(0.0, min(1.0, recovery + 0.04 * support + 0.04 * public_capacity + 0.03 * governance - 0.05 * shock))
        trust = max(0.0, min(1.0, trust + 0.05 * governance + 0.04 * recovery + 0.03 * support - 0.07 * burden - 0.04 * shock))

        support_strength = max(0.0, min(1.0, 0.28 * support + 0.24 * recovery + 0.20 * governance + 0.16 * public_capacity + 0.12 * trust))
        abandonment_risk = max(0.0, min(1.0, exposure + 0.45 * burden + 0.25 * shock - support_strength))
        justice_adjusted_resilience = max(0.0, min(1.0, 0.32 * support_strength + 0.22 * recovery + 0.18 * trust + 0.16 * transformation + 0.12 * (1 - exposure) - 0.20 * abandonment_risk))

        rows.append({
            "pathway_id": row["pathway_id"],
            "pathway": row["pathway"],
            "time": t,
            "shock": round(shock, 5),
            "climate_pressure": round(climate_pressure, 5),
            "infrastructure_pressure": round(infrastructure_pressure, 5),
            "exposure": round(exposure, 5),
            "recovery_capacity": round(recovery, 5),
            "trust": round(trust, 5),
            "support_strength": round(support_strength, 5),
            "abandonment_risk": round(abandonment_risk, 5),
            "justice_adjusted_resilience": round(justice_adjusted_resilience, 5),
        })
    return rows

def summarize_simulation(rows):
    summary = []
    for pathway in sorted({r["pathway"] for r in rows}):
        subset = [r for r in rows if r["pathway"] == pathway]
        risk = [float(r["abandonment_risk"]) for r in subset]
        resilience = [float(r["justice_adjusted_resilience"]) for r in subset]
        exposure = [float(r["exposure"]) for r in subset]
        trust = [float(r["trust"]) for r in subset]
        summary.append({
            "pathway": pathway,
            "mean_abandonment_risk": round(mean(risk), 5),
            "max_abandonment_risk": round(max(risk), 5),
            "final_abandonment_risk": round(risk[-1], 5),
            "mean_justice_adjusted_resilience": round(mean(resilience), 5),
            "final_justice_adjusted_resilience": round(resilience[-1], 5),
            "final_exposure": round(exposure[-1], 5),
            "final_trust": round(trust[-1], 5),
        })
    summary.sort(key=lambda r: r["final_justice_adjusted_resilience"], reverse=True)
    return summary

def monte_carlo(strategies, weights, n=2500):
    rng = random.Random(42)
    rows = []
    for sim in range(n):
        sampled = []
        for strategy in strategies:
            s = dict(strategy)
            for col in BENEFITS + PENALTIES:
                s[col] = str(max(1.0, min(10.0, x(strategy, col) + rng.gauss(0, 0.60))))
            raw, adjusted, risk = score(s, weights)
            sampled.append((adjusted, raw, risk, strategy))
        sampled.sort(reverse=True, key=lambda item: item[0])
        for rank, (adjusted, raw, risk, strategy) in enumerate(sampled, start=1):
            rows.append({
                "simulation_id": sim,
                "strategy_id": strategy["strategy_id"],
                "strategy": strategy["strategy"],
                "rank": rank,
                "adjusted_value": round(adjusted, 5),
                "abandonment_risk": round(risk, 5),
            })

    summary = []
    for strategy in strategies:
        subset = [r for r in rows if r["strategy_id"] == strategy["strategy_id"]]
        ranks = [int(r["rank"]) for r in subset]
        values = [float(r["adjusted_value"]) for r in subset]
        risks = [float(r["abandonment_risk"]) for r in subset]
        summary.append({
            "strategy_id": strategy["strategy_id"],
            "strategy": strategy["strategy"],
            "mean_adjusted_value": round(mean(values), 5),
            "median_adjusted_value": round(median(values), 5),
            "mean_abandonment_risk": round(mean(risks), 5),
            "probability_ranked_first": round(100 * sum(1 for r in ranks if r == 1) / n, 2),
            "probability_top_two": round(100 * sum(1 for r in ranks if r <= 2) / n, 2),
            "probability_bottom_two": round(100 * sum(1 for r in ranks if r >= len(strategies) - 1) / n, 2),
        })
    summary.sort(key=lambda r: r["probability_ranked_first"], reverse=True)
    return rows, summary

def main():
    strategies = read_csv(ROOT / "data/raw/resilience_or_abandonment_strategies.csv")
    scenarios = read_csv(ROOT / "data/raw/abandonment_priority_scenarios.csv")
    ranked = rankings(strategies, scenarios)

    pathways = read_csv(ROOT / "data/raw/abandonment_pathways.csv")
    simulation = []
    for pathway in pathways:
        simulation.extend(simulate_pathway(pathway))
    pathway_summary = summarize_simulation(simulation)

    balanced = next(s for s in scenarios if s["scenario"] == "Balanced")
    mc_rows, mc_summary = monte_carlo(strategies, balanced)

    first_place = {}
    for row in ranked:
        if int(row["rank"]) == 1:
            first_place[row["strategy"]] = first_place.get(row["strategy"], 0) + 1
    first_place_rows = [
        {"strategy": k, "times_ranked_first": v}
        for k, v in sorted(first_place.items(), key=lambda item: item[1], reverse=True)
    ]

    write_csv(OUT / "resilience_or_abandonment_strategy_rankings_standard.csv", ranked)
    write_csv(OUT / "resilience_or_abandonment_top_rank_summary_standard.csv", first_place_rows)
    write_csv(OUT / "resilience_or_abandonment_pathway_simulation_standard.csv", simulation)
    write_csv(OUT / "resilience_or_abandonment_pathway_summary_standard.csv", pathway_summary)
    write_csv(OUT / "resilience_or_abandonment_monte_carlo_standard.csv", mc_rows)
    write_csv(OUT / "resilience_or_abandonment_robustness_summary_standard.csv", mc_summary)

    print("Resilience or Abandonment workflow complete.")
    print(f"Wrote outputs to: {OUT}")
    for row in first_place_rows:
        print(f"  {row['strategy']}: ranked first in {row['times_ranked_first']} priority scenarios")

if __name__ == "__main__":
    main()
