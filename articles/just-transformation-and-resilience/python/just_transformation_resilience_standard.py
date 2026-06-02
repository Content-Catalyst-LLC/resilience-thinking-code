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
    "resilience_capacity",
    "transformation_capacity",
    "equity",
    "ecological_repair",
    "governance_legitimacy",
    "livelihood_protection",
    "exposure_reduction",
]
PENALTIES = ["burden_shift", "lock_in_risk", "implementation_burden"]

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

    justice_gap = (
        0.24 * max(0.0, 8.5 - x(row, "equity"))
        + 0.22 * max(0.0, 8.5 - x(row, "governance_legitimacy"))
        + 0.20 * max(0.0, 8.5 - x(row, "livelihood_protection"))
        + 0.18 * x(row, "burden_shift")
        + 0.16 * x(row, "lock_in_risk")
    )
    adjusted = value - justice_gap
    return value, adjusted, justice_gap

def diagnostic(row, justice_gap):
    if justice_gap >= 3.0:
        return "high justice-gap review needed"
    if x(row, "burden_shift") >= 5.5:
        return "burden-shifting review needed"
    if x(row, "equity") < 7.0:
        return "equity gap"
    if x(row, "governance_legitimacy") < 7.0:
        return "governance legitimacy gap"
    if x(row, "livelihood_protection") < 7.0:
        return "livelihood protection gap"
    return "just transformation candidate"

def rankings(pathways, scenarios):
    rows = []
    for scenario in scenarios:
        scored = []
        for pathway in pathways:
            raw, adjusted, gap = score(pathway, scenario)
            scored.append((adjusted, raw, gap, pathway))
        scored.sort(reverse=True, key=lambda item: item[0])
        for rank, (adjusted, raw, gap, pathway) in enumerate(scored, start=1):
            rows.append({
                "scenario": scenario["scenario"],
                "pathway_id": pathway["pathway_id"],
                "pathway": pathway["pathway"],
                "rank": rank,
                "just_transformation_value": round(raw, 5),
                "justice_gap": round(gap, 5),
                "adjusted_value": round(adjusted, 5),
                "diagnostic": diagnostic(pathway, gap),
                "critical_function": pathway["critical_function"],
            })
    return rows

def simulate_pathway(row, steps=72):
    rng = random.Random(200 + int(row["dynamic_id"].replace("JTD", "")))
    exposure = x(row, "initial_exposure")
    capacity = x(row, "institutional_capacity")
    transformation = x(row, "transformation_investment")
    protection = x(row, "social_protection")
    ecology = x(row, "ecological_repair")
    legitimacy = x(row, "governance_legitimacy")
    burden = x(row, "burden_shift")
    lock_in = x(row, "lock_in_risk")
    trust = 0.50

    rows = []
    shocks = {12: 0.28, 25: 0.31, 39: 0.34, 56: 0.30}

    for t in range(steps):
        shock = shocks.get(t, 0.03 + rng.random() * 0.02)
        climate_pressure = 0.18 + 0.006 * t + 0.25 * shock

        exposure = max(0.0, min(1.0, exposure + 0.04 * climate_pressure + 0.03 * lock_in - 0.07 * transformation - 0.05 * ecology - 0.04 * capacity))
        capacity = max(0.0, min(1.0, capacity + 0.04 * legitimacy + 0.03 * transformation - 0.03 * shock))
        protection = max(0.0, min(1.0, protection + 0.04 * capacity + 0.03 * legitimacy - 0.04 * burden - 0.02 * shock))
        trust = max(0.0, min(1.0, trust + 0.05 * legitimacy + 0.04 * protection - 0.06 * burden - 0.03 * shock))
        lock_in = max(0.0, min(1.0, lock_in + 0.025 * shock + 0.025 * burden - 0.060 * transformation - 0.035 * capacity))
        ecology = max(0.0, min(1.0, ecology + 0.035 * transformation + 0.025 * capacity - 0.025 * climate_pressure))

        transformation_capacity = max(0.0, min(1.0, 0.26 * transformation + 0.20 * capacity + 0.18 * legitimacy + 0.15 * protection + 0.12 * ecology + 0.09 * trust))
        justice_gap = max(0.0, min(1.0, 0.30 * burden + 0.24 * lock_in + 0.20 * exposure - 0.18 * protection - 0.16 * legitimacy))
        justice_adjusted_resilience = max(0.0, min(1.0, 0.24 * transformation_capacity + 0.18 * protection + 0.18 * ecology + 0.16 * trust + 0.14 * (1 - exposure) + 0.10 * (1 - lock_in) - 0.20 * justice_gap))

        rows.append({
            "dynamic_id": row["dynamic_id"],
            "pathway": row["pathway"],
            "time": t,
            "shock": round(shock, 5),
            "climate_pressure": round(climate_pressure, 5),
            "exposure": round(exposure, 5),
            "institutional_capacity": round(capacity, 5),
            "social_protection": round(protection, 5),
            "ecological_repair": round(ecology, 5),
            "governance_legitimacy": round(legitimacy, 5),
            "trust": round(trust, 5),
            "burden_shift": round(burden, 5),
            "lock_in_risk": round(lock_in, 5),
            "transformation_capacity": round(transformation_capacity, 5),
            "justice_gap": round(justice_gap, 5),
            "justice_adjusted_resilience": round(justice_adjusted_resilience, 5),
        })
    return rows

def summarize_simulation(rows):
    summary = []
    for pathway in sorted({r["pathway"] for r in rows}):
        subset = [r for r in rows if r["pathway"] == pathway]
        resilience = [float(r["justice_adjusted_resilience"]) for r in subset]
        gap = [float(r["justice_gap"]) for r in subset]
        exposure = [float(r["exposure"]) for r in subset]
        protection = [float(r["social_protection"]) for r in subset]
        ecology = [float(r["ecological_repair"]) for r in subset]
        trust = [float(r["trust"]) for r in subset]
        lock = [float(r["lock_in_risk"]) for r in subset]
        summary.append({
            "pathway": pathway,
            "mean_justice_adjusted_resilience": round(mean(resilience), 5),
            "final_justice_adjusted_resilience": round(resilience[-1], 5),
            "mean_justice_gap": round(mean(gap), 5),
            "final_justice_gap": round(gap[-1], 5),
            "final_exposure": round(exposure[-1], 5),
            "final_social_protection": round(protection[-1], 5),
            "final_ecological_repair": round(ecology[-1], 5),
            "final_trust": round(trust[-1], 5),
            "final_lock_in_risk": round(lock[-1], 5),
        })
    summary.sort(key=lambda r: r["final_justice_adjusted_resilience"], reverse=True)
    return summary

def monte_carlo(pathways, weights, n=2500):
    rng = random.Random(42)
    rows = []
    for sim in range(n):
        sampled = []
        for pathway in pathways:
            s = dict(pathway)
            for col in BENEFITS + PENALTIES:
                s[col] = str(max(1.0, min(10.0, x(pathway, col) + rng.gauss(0, 0.60))))
            raw, adjusted, gap = score(s, weights)
            sampled.append((adjusted, raw, gap, pathway))
        sampled.sort(reverse=True, key=lambda item: item[0])
        for rank, (adjusted, raw, gap, pathway) in enumerate(sampled, start=1):
            rows.append({
                "simulation_id": sim,
                "pathway_id": pathway["pathway_id"],
                "pathway": pathway["pathway"],
                "rank": rank,
                "adjusted_value": round(adjusted, 5),
                "justice_gap": round(gap, 5),
            })

    summary = []
    for pathway in pathways:
        subset = [r for r in rows if r["pathway_id"] == pathway["pathway_id"]]
        ranks = [int(r["rank"]) for r in subset]
        values = [float(r["adjusted_value"]) for r in subset]
        gaps = [float(r["justice_gap"]) for r in subset]
        summary.append({
            "pathway_id": pathway["pathway_id"],
            "pathway": pathway["pathway"],
            "mean_adjusted_value": round(mean(values), 5),
            "median_adjusted_value": round(median(values), 5),
            "mean_justice_gap": round(mean(gaps), 5),
            "probability_ranked_first": round(100 * sum(1 for r in ranks if r == 1) / n, 2),
            "probability_top_two": round(100 * sum(1 for r in ranks if r <= 2) / n, 2),
            "probability_bottom_two": round(100 * sum(1 for r in ranks if r >= len(pathways) - 1) / n, 2),
        })
    summary.sort(key=lambda r: r["probability_ranked_first"], reverse=True)
    return rows, summary

def main():
    pathways = read_csv(ROOT / "data/raw/just_transformation_pathways.csv")
    scenarios = read_csv(ROOT / "data/raw/just_transformation_priority_scenarios.csv")
    ranked = rankings(pathways, scenarios)

    dynamic_pathways = read_csv(ROOT / "data/raw/just_transformation_dynamic_pathways.csv")
    simulation = []
    for pathway in dynamic_pathways:
        simulation.extend(simulate_pathway(pathway))
    simulation_summary = summarize_simulation(simulation)

    balanced = next(s for s in scenarios if s["scenario"] == "Balanced")
    mc_rows, mc_summary = monte_carlo(pathways, balanced)

    first_place = {}
    for row in ranked:
        if int(row["rank"]) == 1:
            first_place[row["pathway"]] = first_place.get(row["pathway"], 0) + 1
    first_place_rows = [
        {"pathway": k, "times_ranked_first": v}
        for k, v in sorted(first_place.items(), key=lambda item: item[1], reverse=True)
    ]

    write_csv(OUT / "just_transformation_pathway_rankings_standard.csv", ranked)
    write_csv(OUT / "just_transformation_top_rank_summary_standard.csv", first_place_rows)
    write_csv(OUT / "just_transformation_dynamic_simulation_standard.csv", simulation)
    write_csv(OUT / "just_transformation_dynamic_summary_standard.csv", simulation_summary)
    write_csv(OUT / "just_transformation_monte_carlo_standard.csv", mc_rows)
    write_csv(OUT / "just_transformation_robustness_summary_standard.csv", mc_summary)

    print("Just Transformation and Resilience workflow complete.")
    print(f"Wrote outputs to: {OUT}")
    for row in first_place_rows:
        print(f"  {row['pathway']}: ranked first in {row['times_ranked_first']} priority scenarios")

if __name__ == "__main__":
    main()
