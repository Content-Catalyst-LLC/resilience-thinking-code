#!/usr/bin/env python3
"""
Dependency-light feedback-loop workflow.

Reads synthetic feedback profiles and scenarios, calculates feedback-risk
profiles, simulates reinforcing/balancing/delayed behavior, delay sensitivity,
and simple policy-resistance examples using only the Python standard library.

Run:
    python3 python/feedback_loops_standard.py
"""

from __future__ import annotations

import csv
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
PROFILES_PATH = ROOT / "data" / "raw" / "feedback_system_profiles.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "feedback_scenarios.csv"
LINKS_PATH = ROOT / "data" / "raw" / "causal_links.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
DATA_PROCESSED = ROOT / "data" / "processed"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

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

def feedback_risk_score(row: dict[str, str]) -> float:
    return (
        0.24 * f(row, "reinforcing_gain")
        + 0.20 * f(row, "disturbance_load")
        + 0.18 * (f(row, "delay_steps") / 10.0)
        - 0.16 * f(row, "balancing_strength")
        - 0.10 * f(row, "adaptive_capacity")
        - 0.07 * f(row, "signal_quality")
        - 0.03 * f(row, "system_memory")
        - 0.02 * f(row, "justice_visibility")
    )

def diagnostic(row: dict[str, str], risk: float) -> str:
    if risk >= 0.12:
        return "high feedback-risk concern"
    if f(row, "delay_steps") >= 7:
        return "delay and overshoot concern"
    if f(row, "balancing_strength") < 0.10:
        return "weak balancing feedback concern"
    if f(row, "signal_quality") < 0.48:
        return "feedback blindness or signal-quality concern"
    return "mixed feedback profile requiring monitoring"

def loop_type_from_links(loop_links: list[dict[str, str]]) -> str:
    negative_count = sum(1 for link in loop_links if link["polarity"].strip() == "-")
    return "reinforcing" if negative_count % 2 == 0 else "balancing"

def simulate_scenario(scenario: dict[str, str], steps: int = 80) -> list[dict[str, object]]:
    gain = float(scenario["reinforcing_gain"])
    balancing = float(scenario["balancing_strength"])
    delay = int(float(scenario["delay_steps"]))
    target = float(scenario["target"])
    shock = float(scenario["disturbance_shock"])
    adaptive_response = float(scenario["adaptive_response"])

    x = [20.0 for _ in range(max(steps, delay + 2))]
    rows = []

    for t in range(1, steps):
        delayed_index = max(0, t - delay)
        disturbance = shock if t == 12 else 0.0
        effective_balancing = balancing + adaptive_response * min(1.0, t / steps)

        x[t] = (
            x[t - 1]
            + gain * x[t - 1]
            - effective_balancing * (x[delayed_index] - target)
            + disturbance
        )

        overshoot = max(0.0, x[t] - target)
        rows.append(
            {
                "scenario_id": scenario["scenario_id"],
                "scenario_name": scenario["scenario_name"],
                "time_step": t,
                "value": round(x[t], 5),
                "target": target,
                "reinforcing_gain": gain,
                "effective_balancing": round(effective_balancing, 5),
                "delay_steps": delay,
                "disturbance": disturbance,
                "overshoot": round(overshoot, 5),
            }
        )
    return rows

def simulate_delay_sensitivity(base: dict[str, str], delays: list[int] | None = None, steps: int = 80) -> list[dict[str, object]]:
    if delays is None:
        delays = [1, 3, 5, 8, 12]
    rows = []
    for delay in delays:
        scenario = dict(base)
        scenario["delay_steps"] = str(delay)
        sim = simulate_scenario(scenario, steps=steps)
        for row in sim:
            row["delay_experiment"] = delay
        rows.extend(sim)
    return rows

def simulate_policy_resistance(steps: int = 80) -> list[dict[str, object]]:
    rows = []
    fuel = 35.0
    visible_fire_damage = 20.0
    suppression = 0.70

    for t in range(1, steps + 1):
        fuel += 1.2 * suppression - 0.18 * visible_fire_damage
        fuel = max(0.0, fuel)

        if t % 15 == 0:
            visible_fire_damage = 0.22 * fuel * (1.0 + suppression)
        else:
            visible_fire_damage = max(0.0, visible_fire_damage * 0.72)

        suppression = min(1.0, suppression + 0.012 * visible_fire_damage / 20.0)

        rows.append(
            {
                "time_step": t,
                "fuel_load": round(fuel, 5),
                "visible_fire_damage": round(visible_fire_damage, 5),
                "suppression_pressure": round(suppression, 5),
                "policy_resistance_note": "short-term suppression can increase long-term fuel accumulation",
            }
        )
    return rows

def main() -> None:
    profiles = read_csv(PROFILES_PATH)
    scenarios = read_csv(SCENARIOS_PATH)
    links = read_csv(LINKS_PATH)

    profile_rows = []
    for row in profiles:
        risk = feedback_risk_score(row)
        profile_rows.append(
            {
                "system_id": row["system_id"],
                "system_name": row["system_name"],
                "system_type": row["system_type"],
                "critical_function": row["critical_function"],
                "feedback_risk_score": round(risk, 5),
                "reinforcing_gain": row["reinforcing_gain"],
                "balancing_strength": row["balancing_strength"],
                "delay_steps": row["delay_steps"],
                "disturbance_load": row["disturbance_load"],
                "adaptive_capacity": row["adaptive_capacity"],
                "signal_quality": row["signal_quality"],
                "system_memory": row["system_memory"],
                "justice_visibility": row["justice_visibility"],
                "diagnostic": diagnostic(row, risk),
            }
        )

    loop_rows = []
    for loop_id in sorted({link["loop_id"] for link in links}):
        loop_links = [link for link in links if link["loop_id"] == loop_id]
        loop_rows.append(
            {
                "loop_id": loop_id,
                "loop_name": loop_links[0]["loop_name"],
                "link_count": len(loop_links),
                "negative_link_count": sum(1 for link in loop_links if link["polarity"].strip() == "-"),
                "loop_type": loop_type_from_links(loop_links),
            }
        )

    simulation_rows = []
    for scenario in scenarios:
        simulation_rows.extend(simulate_scenario(scenario))

    delay_rows = simulate_delay_sensitivity(scenarios[0])
    policy_rows = simulate_policy_resistance()

    scenario_summary = []
    for sid in sorted({r["scenario_id"] for r in simulation_rows}):
        subset = [r for r in simulation_rows if r["scenario_id"] == sid]
        scenario_summary.append(
            {
                "scenario_id": sid,
                "scenario_name": subset[0]["scenario_name"],
                "final_value": round(float(subset[-1]["value"]), 4),
                "maximum_value": round(max(float(r["value"]) for r in subset), 4),
                "maximum_overshoot": round(max(float(r["overshoot"]) for r in subset), 4),
                "average_effective_balancing": round(mean(float(r["effective_balancing"]) for r in subset), 4),
            }
        )

    write_csv(OUT_TABLES / "feedback_system_profiles_standard.csv", profile_rows)
    write_csv(OUT_TABLES / "feedback_loop_polarity_diagnostics_standard.csv", loop_rows)
    write_csv(OUT_TABLES / "feedback_loop_simulation_standard.csv", simulation_rows)
    write_csv(OUT_TABLES / "feedback_delay_sensitivity_standard.csv", delay_rows)
    write_csv(OUT_TABLES / "policy_resistance_fire_suppression_standard.csv", policy_rows)
    write_csv(OUT_TABLES / "feedback_scenario_summary_standard.csv", scenario_summary)
    write_csv(DATA_PROCESSED / "feedback_system_profiles_standard.csv", profile_rows)

    print("Feedback loops workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    for row in profile_rows:
        print(f"  {row['system_name']}: risk={row['feedback_risk_score']} diagnostic={row['diagnostic']}")

if __name__ == "__main__":
    main()
