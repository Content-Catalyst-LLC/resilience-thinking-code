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
    "persistence_capacity",
    "harm_reduction",
    "lock_in_reduction",
    "equity",
    "transformation_capacity",
    "ecological_integrity",
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

    maladaptive_risk = (
        0.28 * max(0.0, 8.0 - x(row, "harm_reduction"))
        + 0.24 * max(0.0, 8.0 - x(row, "lock_in_reduction"))
        + 0.20 * max(0.0, 8.0 - x(row, "transformation_capacity"))
        + 0.16 * x(row, "burden_shift")
        + 0.12 * max(0.0, 8.0 - x(row, "equity"))
    )
    adjusted = value - maladaptive_risk
    return value, adjusted, maladaptive_risk

def diagnostic(row, maladaptive_risk):
    if maladaptive_risk >= 3.0:
        return "high maladaptive-resilience risk"
    if x(row, "burden_shift") >= 5.5:
        return "burden-shifting review needed"
    if x(row, "harm_reduction") < 6.0:
        return "harm-reduction gap"
    if x(row, "lock_in_reduction") < 6.0:
        return "lock-in reduction gap"
    if x(row, "transformation_capacity") < 6.0:
        return "transformation gap"
    return "adaptive resilience candidate"

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
                "adaptive_resilience_value": round(raw, 5),
                "maladaptive_risk": round(risk, 5),
                "adjusted_value": round(adjusted, 5),
                "diagnostic": diagnostic(strategy, risk),
                "critical_function": strategy["critical_function"],
            })
    return rows

def simulate_pathway(row, steps=70):
    rng = random.Random(100 + int(row["pathway_id"].replace("MP", "")))
    persistence = x(row, "initial_persistence")
    harm = x(row, "initial_harm")
    lock_in = x(row, "initial_lock_in")
    burden = x(row, "burden_shift")
    transformation = x(row, "transformation_capacity")
    ecology = x(row, "ecological_integrity")
    equity = x(row, "equity")

    rows = []
    shocks = {12: 0.28, 25: 0.32, 40: 0.34, 55: 0.30}

    for t in range(steps):
        shock = shocks.get(t, 0.03 + rng.random() * 0.02)

        persistence = max(0.0, min(1.0, persistence + 0.04 * shock + 0.02 * lock_in - 0.03 * transformation))
        harm = max(0.0, min(1.0, harm + 0.035 * persistence + 0.030 * burden + 0.025 * shock - 0.060 * transformation - 0.030 * ecology))
        lock_in = max(0.0, min(1.0, lock_in + 0.030 * persistence + 0.020 * shock - 0.055 * transformation))
        ecology = max(0.0, min(1.0, ecology - 0.025 * harm + 0.040 * transformation))
        equity = max(0.0, min(1.0, equity - 0.030 * burden - 0.020 * harm + 0.045 * transformation))

        maladaptive_risk = max(0.0, min(1.0, 0.30 * persistence + 0.28 * harm + 0.22 * lock_in + 0.15 * burden - 0.20 * transformation - 0.10 * equity))
        adaptive_resilience = max(0.0, min(1.0, 0.24 * transformation + 0.20 * ecology + 0.20 * equity + 0.16 * (1 - harm) + 0.12 * (1 - lock_in) + 0.08 * persistence - 0.16 * maladaptive_risk))

        rows.append({
            "pathway_id": row["pathway_id"],
            "pathway": row["pathway"],
            "time": t,
            "shock": round(shock, 5),
            "persistence": round(persistence, 5),
            "harm": round(harm, 5),
            "lock_in": round(lock_in, 5),
            "burden_shift": round(burden, 5),
            "transformation_capacity": round(transformation, 5),
            "ecological_integrity": round(ecology, 5),
            "equity": round(equity, 5),
            "maladaptive_risk": round(maladaptive_risk, 5),
            "adaptive_resilience": round(adaptive_resilience, 5),
        })
    return rows

def summarize_simulation(rows):
    summary = []
    for pathway in sorted({r["pathway"] for r in rows}):
        subset = [r for r in rows if r["pathway"] == pathway]
        risk = [float(r["maladaptive_risk"]) for r in subset]
        adaptive = [float(r["adaptive_resilience"]) for r in subset]
        harm = [float(r["harm"]) for r in subset]
        lock = [float(r["lock_in"]) for r in subset]
        equity = [float(r["equity"]) for r in subset]
        summary.append({
            "pathway": pathway,
            "mean_maladaptive_risk": round(mean(risk), 5),
            "max_maladaptive_risk": round(max(risk), 5),
            "final_maladaptive_risk": round(risk[-1], 5),
            "mean_adaptive_resilience": round(mean(adaptive), 5),
            "final_adaptive_resilience": round(adaptive[-1], 5),
            "final_harm": round(harm[-1], 5),
            "final_lock_in": round(lock[-1], 5),
            "final_equity": round(equity[-1], 5),
        })
    summary.sort(key=lambda r: r["final_adaptive_resilience"], reverse=True)
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
                "maladaptive_risk": round(risk, 5),
            })

    summary = []
    for strategy in strategies:
        subset = [r for r in rows if r["strategy_id"] == strategy["strategy_id"]]
        ranks = [int(r["rank"]) for r in subset]
        values = [float(r["adjusted_value"]) for r in subset]
        risks = [float(r["maladaptive_risk"]) for r in subset]
        summary.append({
            "strategy_id": strategy["strategy_id"],
            "strategy": strategy["strategy"],
            "mean_adjusted_value": round(mean(values), 5),
            "median_adjusted_value": round(median(values), 5),
            "mean_maladaptive_risk": round(mean(risks), 5),
            "probability_ranked_first": round(100 * sum(1 for r in ranks if r == 1) / n, 2),
            "probability_top_two": round(100 * sum(1 for r in ranks if r <= 2) / n, 2),
            "probability_bottom_two": round(100 * sum(1 for r in ranks if r >= len(strategies) - 1) / n, 2),
        })
    summary.sort(key=lambda r: r["probability_ranked_first"], reverse=True)
    return rows, summary

def main():
    strategies = read_csv(ROOT / "data/raw/maladaptive_resilience_strategies.csv")
    scenarios = read_csv(ROOT / "data/raw/maladaptive_priority_scenarios.csv")
    ranked = rankings(strategies, scenarios)

    pathways = read_csv(ROOT / "data/raw/maladaptive_pathways.csv")
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

    write_csv(OUT / "maladaptive_resilience_strategy_rankings_standard.csv", ranked)
    write_csv(OUT / "maladaptive_resilience_top_rank_summary_standard.csv", first_place_rows)
    write_csv(OUT / "maladaptive_resilience_pathway_simulation_standard.csv", simulation)
    write_csv(OUT / "maladaptive_resilience_pathway_summary_standard.csv", pathway_summary)
    write_csv(OUT / "maladaptive_resilience_monte_carlo_standard.csv", mc_rows)
    write_csv(OUT / "maladaptive_resilience_robustness_summary_standard.csv", mc_summary)

    print("Maladaptive Resilience workflow complete.")
    print(f"Wrote outputs to: {OUT}")
    for row in first_place_rows:
        print(f"  {row['strategy']}: ranked first in {row['times_ranked_first']} priority scenarios")

if __name__ == "__main__":
    main()
