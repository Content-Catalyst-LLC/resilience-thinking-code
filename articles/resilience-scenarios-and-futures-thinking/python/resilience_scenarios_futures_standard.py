#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "tables"
OUT.mkdir(parents=True, exist_ok=True)

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

def scenario_value(row):
    return (
        0.10 * x(row, "horizon_scanning")
        + 0.10 * x(row, "weak_signal_detection")
        + 0.11 * x(row, "stress_testing")
        + 0.12 * x(row, "adaptive_pathways")
        + 0.11 * x(row, "participation")
        + 0.10 * x(row, "data_modeling")
        + 0.12 * x(row, "governance_integration")
        + 0.12 * x(row, "equity_sensitivity")
        + 0.12 * x(row, "transformation_potential")
        - 0.04 * x(row, "scenario_design_risk")
        - 0.04 * x(row, "implementation_burden")
    )

def diagnostic(row, value):
    if x(row, "implementation_burden") >= 3.9:
        return "implementation-burden review needed"
    if x(row, "scenario_design_risk") >= 3.0:
        return "scenario-design risk review needed"
    if x(row, "participation") < 8.2:
        return "participation review needed"
    if x(row, "equity_sensitivity") < 8.2:
        return "equity review needed"
    if x(row, "governance_integration") < 8.4:
        return "governance integration review needed"
    if value >= 7.70:
        return "strong resilience scenario strategy candidate"
    return "promising but requires iterative revision"

def simulate_pathway(row, steps=60):
    function = x(row, "initial_function")
    vulnerability = x(row, "initial_vulnerability")
    trust = x(row, "initial_trust")
    learning = 0.40
    climate = 0.30
    infrastructure = 0.34

    governance = x(row, "governance_capacity")
    adaptive = x(row, "adaptive_capacity")
    participation = x(row, "participation")
    equity = x(row, "equity_focus")
    transformation = x(row, "transformation_investment")
    redundancy = x(row, "redundancy_and_slack")

    shocks = {10: 0.66, 22: 0.74, 34: 0.78, 46: 0.68, 56: 0.90}
    rows = []

    for t in range(steps):
        shock = shocks.get(t, 0.05)
        climate = max(0.0, min(1.0, climate + x(row, "climate_stress_growth") + 0.08 * shock - 0.020 * transformation))
        infrastructure = max(0.0, min(1.0, infrastructure + x(row, "infrastructure_stress_growth") + 0.07 * shock - 0.018 * adaptive))
        vulnerability = max(0.0, min(1.0, vulnerability + x(row, "social_vulnerability_growth") + 0.045 * climate + 0.040 * infrastructure - 0.080 * equity - 0.045 * participation - 0.030 * transformation))
        learning = max(0.0, min(1.0, learning + 0.055 * governance + 0.045 * participation + 0.040 * adaptive + 0.030 * transformation - 0.035 * shock))
        trust = max(0.0, min(1.0, trust + 0.050 * participation + 0.050 * equity + 0.035 * learning + 0.025 * governance - 0.070 * vulnerability - 0.035 * shock))

        adaptive_buffer = max(0.0, min(1.0, 0.20 * adaptive + 0.17 * governance + 0.17 * redundancy + 0.14 * learning + 0.12 * trust + 0.10 * transformation + 0.10 * participation))
        transformation_effect = max(0.0, min(1.0, 0.28 * transformation + 0.22 * equity + 0.18 * participation + 0.15 * governance + 0.10 * learning + 0.07 * adaptive))
        fragility_gap = max(0.0, 0.30 * climate + 0.26 * infrastructure + 0.25 * vulnerability + 0.16 * shock - adaptive_buffer)

        function = max(0.0, min(1.0, function - 0.20 * climate - 0.17 * infrastructure - 0.17 * vulnerability - 0.13 * shock - 0.10 * fragility_gap + 0.20 * adaptive_buffer + 0.15 * transformation_effect + 0.08 * trust))
        equity_adjusted = max(0.0, min(1.0, function * (0.70 + 0.30 * equity) - 0.11 * vulnerability + 0.08 * trust))
        resilience_score = max(0.0, min(1.0, 0.18 * function + 0.17 * adaptive_buffer + 0.15 * transformation_effect + 0.13 * trust + 0.12 * learning + 0.10 * (1.0 - vulnerability) + 0.08 * redundancy + 0.07 * governance))

        rows.append({
            "scenario": row["scenario"],
            "time": t,
            "shock": round(shock, 5),
            "climate_stress": round(climate, 5),
            "infrastructure_stress": round(infrastructure, 5),
            "vulnerability": round(vulnerability, 5),
            "institutional_learning": round(learning, 5),
            "social_trust": round(trust, 5),
            "adaptive_buffer": round(adaptive_buffer, 5),
            "transformation_effect": round(transformation_effect, 5),
            "fragility_gap": round(fragility_gap, 5),
            "function": round(function, 5),
            "equity_adjusted_resilience": round(equity_adjusted, 5),
            "robust_resilience_score": round(resilience_score, 5),
        })
    return rows

def main():
    strategies = read_csv(ROOT / "data/raw/resilience_scenario_strategies.csv")
    profiles = []
    for row in strategies:
        value = scenario_value(row)
        profiles.append({
            "strategy_id": row["strategy_id"],
            "strategy": row["strategy"],
            "scenario_resilience_value": round(value, 5),
            "diagnostic": diagnostic(row, value),
        })
    profiles.sort(key=lambda r: r["scenario_resilience_value"], reverse=True)

    pathways = read_csv(ROOT / "data/raw/resilience_future_pathways.csv")
    simulation = []
    for p in pathways:
        simulation.extend(simulate_pathway(p))

    summary = []
    for scenario in sorted({r["scenario"] for r in simulation}):
        subset = [r for r in simulation if r["scenario"] == scenario]
        summary.append({
            "scenario": scenario,
            "mean_function": round(mean(float(r["function"]) for r in subset), 5),
            "minimum_function": min(float(r["function"]) for r in subset),
            "final_function": subset[-1]["function"],
            "final_vulnerability": subset[-1]["vulnerability"],
            "final_social_trust": subset[-1]["social_trust"],
            "final_equity_adjusted_resilience": subset[-1]["equity_adjusted_resilience"],
            "final_robust_resilience_score": subset[-1]["robust_resilience_score"],
        })
    summary.sort(key=lambda r: r["final_robust_resilience_score"], reverse=True)

    write_csv(OUT / "resilience_scenario_strategy_profiles_standard.csv", profiles)
    write_csv(OUT / "resilience_future_pathway_simulation_standard.csv", simulation)
    write_csv(OUT / "resilience_future_pathway_summary_standard.csv", summary)

    print("Resilience scenarios and futures thinking workflow complete.")
    print(f"Wrote outputs to: {OUT}")
    for row in profiles:
        print(f"  {row['strategy']}: value={row['scenario_resilience_value']} diagnostic={row['diagnostic']}")

if __name__ == "__main__":
    main()
