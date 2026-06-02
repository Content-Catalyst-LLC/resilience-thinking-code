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
    "adaptive_capacity",
    "buffering_capacity",
    "transformability",
    "governance_quality",
    "equity_performance",
    "digital_resilience",
    "climate_readiness",
]
PENALTIES = ["systemic_exposure", "implementation_burden"]

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
    governance_gap = max(0.0, 8.5 - x(row, "governance_quality"))
    equity_gap = max(0.0, 8.5 - x(row, "equity_performance"))
    adjusted = value - 0.06 * governance_gap - 0.08 * equity_gap
    return value, adjusted

def diagnostic(row):
    if x(row, "implementation_burden") >= 3.9:
        return "implementation-burden review needed"
    if x(row, "systemic_exposure") >= 4.4:
        return "exposure reduction review needed"
    if x(row, "equity_performance") < 8.0:
        return "equity-performance review needed"
    if x(row, "governance_quality") < 8.0:
        return "governance-capacity review needed"
    if x(row, "digital_resilience") < 7.5:
        return "digital-resilience review needed"
    return "promising but requires scenario testing"

def rankings(strategies, scenarios):
    rows = []
    for scenario in scenarios:
        scored = []
        for strategy in strategies:
            raw, adjusted = score(strategy, scenario)
            scored.append((adjusted, raw, strategy))
        scored.sort(reverse=True, key=lambda item: item[0])
        for rank, (adjusted, raw, strategy) in enumerate(scored, start=1):
            rows.append({
                "scenario": scenario["scenario"],
                "strategy_id": strategy["strategy_id"],
                "strategy": strategy["strategy"],
                "rank": rank,
                "resilience_value": round(raw, 5),
                "adjusted_resilience_value": round(adjusted, 5),
                "diagnostic": diagnostic(strategy),
                "critical_function": strategy["critical_function"],
            })
    return rows

def monte_carlo(strategies, weights, n=3000):
    rng = random.Random(42)
    rows = []
    for sim in range(n):
        sampled = []
        for strategy in strategies:
            s = dict(strategy)
            for col in BENEFITS + PENALTIES:
                s[col] = str(max(1.0, min(10.0, x(strategy, col) + rng.gauss(0, 0.55))))
            raw, adjusted = score(s, weights)
            sampled.append((adjusted, raw, strategy))
        sampled.sort(reverse=True, key=lambda item: item[0])
        for rank, (adjusted, raw, strategy) in enumerate(sampled, start=1):
            rows.append({
                "simulation_id": sim,
                "strategy_id": strategy["strategy_id"],
                "strategy": strategy["strategy"],
                "rank": rank,
                "adjusted_resilience_value": round(adjusted, 5),
            })

    summary = []
    for strategy in strategies:
        subset = [r for r in rows if r["strategy_id"] == strategy["strategy_id"]]
        ranks = [int(r["rank"]) for r in subset]
        values = [float(r["adjusted_resilience_value"]) for r in subset]
        summary.append({
            "strategy_id": strategy["strategy_id"],
            "strategy": strategy["strategy"],
            "mean_adjusted_value": round(mean(values), 5),
            "median_adjusted_value": round(median(values), 5),
            "probability_ranked_first": round(100 * sum(1 for r in ranks if r == 1) / n, 2),
            "probability_top_two": round(100 * sum(1 for r in ranks if r <= 2) / n, 2),
            "probability_bottom_two": round(100 * sum(1 for r in ranks if r >= len(strategies) - 1) / n, 2),
        })
    summary.sort(key=lambda r: r["probability_ranked_first"], reverse=True)
    return rows, summary

def main():
    strategies = read_csv(ROOT / "data/raw/future_resilience_strategies.csv")
    scenarios = read_csv(ROOT / "data/raw/future_resilience_priority_scenarios.csv")
    ranked = rankings(strategies, scenarios)

    balanced = next(s for s in scenarios if s["scenario"] == "Balanced")
    simulation, robustness = monte_carlo(strategies, balanced)

    first_place = {}
    for row in ranked:
        if int(row["rank"]) == 1:
            first_place[row["strategy"]] = first_place.get(row["strategy"], 0) + 1
    first_place_rows = [
        {"strategy": k, "times_ranked_first": v}
        for k, v in sorted(first_place.items(), key=lambda item: item[1], reverse=True)
    ]

    write_csv(OUT / "future_resilience_strategy_rankings_standard.csv", ranked)
    write_csv(OUT / "future_resilience_top_rank_summary_standard.csv", first_place_rows)
    write_csv(OUT / "future_resilience_uncertainty_simulation_standard.csv", simulation)
    write_csv(OUT / "future_resilience_robustness_summary_standard.csv", robustness)

    print("Future resilience strategy workflow complete.")
    print(f"Wrote outputs to: {OUT}")
    for row in first_place_rows:
        print(f"  {row['strategy']}: ranked first in {row['times_ranked_first']} priority scenarios")

if __name__ == "__main__":
    main()
