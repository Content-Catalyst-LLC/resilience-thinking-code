#!/usr/bin/env python3
"""
Dependency-light adaptive-cycle and panarchy workflow.

Reads synthetic cycle profiles and scenarios, simulates adaptive-cycle phase
dynamics, models release/reorganization, estimates cross-scale revolt/remember
effects, and exports outputs using only the Python standard library.

Run:
    python3 python/adaptive_cycles_panarchy_standard.py
"""

from __future__ import annotations

import csv
import math
import random
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
SYSTEMS_PATH = ROOT / "data" / "raw" / "system_cycle_profiles.csv"
SCALES_PATH = ROOT / "data" / "raw" / "panarchy_scale_profiles.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "cycle_scenarios.csv"
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


def phase_diagnostic(row: dict[str, str]) -> str:
    if row["initial_phase"] == "K" and f(row, "rigidity") >= 0.62 and f(row, "resilience") <= 0.40:
        return "conservation-phase brittleness concern"
    if row["initial_phase"] == "alpha" and f(row, "memory") >= 0.60 and f(row, "novelty") >= 0.30:
        return "strong reorganization potential"
    if row["initial_phase"] == "r" and f(row, "novelty") >= 0.35:
        return "high experimentation and growth potential"
    return "mixed adaptive-cycle profile requiring monitoring"


def update_cycle(
    state: dict[str, object],
    scenario: dict[str, str],
    memory_input: float = 0.0,
    rng: random.Random | None = None,
) -> dict[str, object]:
    if rng is None:
        rng = random.Random(42)

    phase = str(state["phase"])
    potential = float(state["potential"])
    connectedness = float(state["connectedness"])
    resilience = float(state["resilience"])
    rigidity = float(state["rigidity"])
    memory = float(state["memory"])
    novelty = float(state["novelty"])

    growth_rate = float(scenario["growth_rate"])
    connect_rate = float(scenario["connect_rate"])
    disturbance_pressure = float(scenario["disturbance_pressure"])
    rigidity_threshold = float(scenario["rigidity_threshold"])
    resilience_threshold = float(scenario["resilience_threshold"])
    memory_strength = float(scenario["memory_strength"])
    novelty_low = float(scenario["novelty_range_low"])
    novelty_high = float(scenario["novelty_range_high"])

    if phase in ("r", "K"):
        potential = min(1.0, potential + growth_rate * potential * (1.0 - potential))
        connectedness = min(1.0, connectedness + connect_rate * (1.0 - connectedness))
        rigidity = min(1.0, rigidity + 0.050 * connectedness + 0.020 * disturbance_pressure)
        resilience = max(0.0, 1.0 - 0.62 * connectedness - 0.34 * rigidity - 0.12 * disturbance_pressure)
        memory = min(1.0, memory + 0.012 * potential)
        novelty = max(0.02, 0.25 * (1.0 - connectedness))
        phase = "K" if connectedness > 0.55 else "r"

        if rigidity > rigidity_threshold and resilience < resilience_threshold:
            phase = "Omega"

    elif phase == "Omega":
        potential = max(0.05, potential * 0.42)
        connectedness = max(0.08, connectedness * 0.32)
        rigidity = max(0.05, rigidity * 0.38)
        resilience = min(1.0, resilience + 0.30)
        memory = max(0.20, memory * 0.86)
        novelty = rng.uniform(novelty_high, min(0.50, novelty_high + 0.16))
        phase = "alpha"

    elif phase == "alpha":
        novelty = rng.uniform(novelty_low, novelty_high)
        potential = min(1.0, memory_strength * memory + memory_input + novelty)
        connectedness = min(1.0, connectedness + rng.uniform(0.015, 0.045))
        rigidity = max(0.03, rigidity + rng.uniform(-0.020, 0.015))
        resilience = min(1.0, resilience + rng.uniform(0.025, 0.075))
        memory = min(1.0, memory + rng.uniform(-0.015, 0.025))

        if potential > 0.32 and connectedness < 0.50:
            phase = "r"
        else:
            phase = "alpha"

    state.update(
        {
            "phase": phase,
            "potential": potential,
            "connectedness": connectedness,
            "resilience": resilience,
            "rigidity": rigidity,
            "memory": memory,
            "novelty": novelty,
        }
    )
    return state


def simulate_system(system: dict[str, str], scenario: dict[str, str], steps: int = 120) -> list[dict[str, object]]:
    rng = random.Random(42)
    state: dict[str, object] = {
        "phase": system["initial_phase"],
        "potential": f(system, "potential"),
        "connectedness": f(system, "connectedness"),
        "resilience": f(system, "resilience"),
        "rigidity": f(system, "rigidity"),
        "memory": f(system, "memory"),
        "novelty": f(system, "novelty"),
    }

    rows = []

    for t in range(1, steps + 1):
        previous_phase = str(state["phase"])
        state = update_cycle(state, scenario, memory_input=0.0, rng=rng)
        release_flag = 1 if state["phase"] == "Omega" else 0

        rows.append(
            {
                "system_id": system["system_id"],
                "system_name": system["system_name"],
                "system_type": system["system_type"],
                "scenario_id": scenario["scenario_id"],
                "scenario_name": scenario["scenario_name"],
                "time_step": t,
                "phase": state["phase"],
                "phase_changed": state["phase"] != previous_phase,
                "potential": round(float(state["potential"]), 5),
                "connectedness": round(float(state["connectedness"]), 5),
                "resilience": round(float(state["resilience"]), 5),
                "rigidity": round(float(state["rigidity"]), 5),
                "memory": round(float(state["memory"]), 5),
                "novelty": round(float(state["novelty"]), 5),
                "release_flag": release_flag,
            }
        )

    return rows


def simulate_two_scale_panarchy(scales: list[dict[str, str]], scenario: dict[str, str], steps: int = 120) -> list[dict[str, object]]:
    rng = random.Random(42)
    fast_rows = [r for r in scales if r["scale_speed"] == "fast"]
    slow_rows = [r for r in scales if r["scale_speed"] == "slow"]

    rows = []
    pairs = list(zip(fast_rows, slow_rows))

    for fast_row, slow_row in pairs:
        fast_state: dict[str, object] = {
            "phase": "r" if f(fast_row, "connectedness") < 0.55 else "K",
            "potential": f(fast_row, "potential"),
            "connectedness": f(fast_row, "connectedness"),
            "resilience": f(fast_row, "resilience"),
            "rigidity": f(fast_row, "rigidity"),
            "memory": f(fast_row, "memory"),
            "novelty": f(fast_row, "innovation_capacity"),
        }
        slow_state: dict[str, object] = {
            "phase": "K",
            "potential": f(slow_row, "potential"),
            "connectedness": f(slow_row, "connectedness"),
            "resilience": f(slow_row, "resilience"),
            "rigidity": f(slow_row, "rigidity"),
            "memory": f(slow_row, "memory"),
            "novelty": f(slow_row, "innovation_capacity"),
        }

        for t in range(1, steps + 1):
            previous_fast_phase = str(fast_state["phase"])
            previous_slow_phase = str(slow_state["phase"])

            remember_effect = float(scenario["remember_strength"]) * float(slow_state["memory"]) if fast_state["phase"] == "alpha" else 0.0
            fast_state = update_cycle(fast_state, scenario, memory_input=remember_effect, rng=rng)

            revolt_effect = 0.0
            if fast_state["phase"] == "Omega" and float(slow_state["connectedness"]) > 0.72 and float(slow_state["resilience"]) < 0.42:
                revolt_effect = float(scenario["revolt_strength"])

            slow_state["rigidity"] = min(1.0, float(slow_state["rigidity"]) + revolt_effect)
            slow_state = update_cycle(slow_state, scenario, memory_input=0.0, rng=rng)

            rows.append(
                {
                    "system_id": fast_row["system_id"],
                    "fast_scale": fast_row["scale_name"],
                    "slow_scale": slow_row["scale_name"],
                    "scenario_id": scenario["scenario_id"],
                    "scenario_name": scenario["scenario_name"],
                    "time_step": t,
                    "fast_phase": fast_state["phase"],
                    "slow_phase": slow_state["phase"],
                    "fast_potential": round(float(fast_state["potential"]), 5),
                    "fast_connectedness": round(float(fast_state["connectedness"]), 5),
                    "fast_resilience": round(float(fast_state["resilience"]), 5),
                    "fast_rigidity": round(float(fast_state["rigidity"]), 5),
                    "fast_memory": round(float(fast_state["memory"]), 5),
                    "slow_potential": round(float(slow_state["potential"]), 5),
                    "slow_connectedness": round(float(slow_state["connectedness"]), 5),
                    "slow_resilience": round(float(slow_state["resilience"]), 5),
                    "slow_rigidity": round(float(slow_state["rigidity"]), 5),
                    "slow_memory": round(float(slow_state["memory"]), 5),
                    "revolt_effect": round(revolt_effect, 5),
                    "remember_effect": round(remember_effect, 5),
                    "fast_phase_changed": fast_state["phase"] != previous_fast_phase,
                    "slow_phase_changed": slow_state["phase"] != previous_slow_phase,
                }
            )

    return rows


def main() -> None:
    systems = read_csv(SYSTEMS_PATH)
    scales = read_csv(SCALES_PATH)
    scenarios = read_csv(SCENARIOS_PATH)

    profile_rows = []
    for system in systems:
        profile_rows.append(
            {
                "system_id": system["system_id"],
                "system_name": system["system_name"],
                "system_type": system["system_type"],
                "initial_phase": system["initial_phase"],
                "potential": system["potential"],
                "connectedness": system["connectedness"],
                "resilience": system["resilience"],
                "rigidity": system["rigidity"],
                "memory": system["memory"],
                "novelty": system["novelty"],
                "diagnostic": phase_diagnostic(system),
            }
        )

    simulation_rows = []
    panarchy_rows = []

    for scenario in scenarios:
        for system in systems:
            simulation_rows.extend(simulate_system(system, scenario))
        panarchy_rows.extend(simulate_two_scale_panarchy(scales, scenario))

    summary_rows = []
    for sid in sorted({r["system_id"] for r in simulation_rows}):
        subset = [r for r in simulation_rows if r["system_id"] == sid]
        summary_rows.append(
            {
                "system_id": sid,
                "system_name": subset[0]["system_name"],
                "release_events": sum(1 for r in subset if r["phase"] == "Omega"),
                "alpha_steps": sum(1 for r in subset if r["phase"] == "alpha"),
                "minimum_resilience": round(min(float(r["resilience"]) for r in subset), 4),
                "maximum_rigidity": round(max(float(r["rigidity"]) for r in subset), 4),
                "average_memory": round(mean(float(r["memory"]) for r in subset), 4),
            }
        )

    write_csv(OUT_TABLES / "adaptive_cycle_profiles_standard.csv", profile_rows)
    write_csv(OUT_TABLES / "adaptive_cycle_phase_simulation_standard.csv", simulation_rows)
    write_csv(OUT_TABLES / "adaptive_cycle_summary_standard.csv", summary_rows)
    write_csv(OUT_TABLES / "panarchy_cross_scale_simulation_standard.csv", panarchy_rows)
    write_csv(DATA_PROCESSED / "adaptive_cycle_profiles_standard.csv", profile_rows)

    print("Adaptive cycles and panarchy workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    for row in profile_rows:
        print(f"  {row['system_name']}: phase={row['initial_phase']} diagnostic={row['diagnostic']}")


if __name__ == "__main__":
    main()
