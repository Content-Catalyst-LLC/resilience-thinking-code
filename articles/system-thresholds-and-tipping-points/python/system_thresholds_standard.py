#!/usr/bin/env python3
"""
Dependency-light threshold and tipping-point workflow.

Reads synthetic system profiles and threshold scenarios, calculates threshold-risk
profiles, simulates nonlinear threshold/hysteresis paths, computes rolling early
warning indicators, and exports outputs using only the Python standard library.

Run:
    python3 python/system_thresholds_standard.py
"""

from __future__ import annotations

import csv
import math
import random
from pathlib import Path
from statistics import mean, variance


ROOT = Path(__file__).resolve().parents[1]
PROFILES_PATH = ROOT / "data" / "raw" / "threshold_system_profiles.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "threshold_scenarios.csv"
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


def threshold_risk_score(row: dict[str, str]) -> float:
    return (
        0.24 * f(row, "pressure")
        + 0.22 * f(row, "feedback_strength")
        + 0.18 * f(row, "disturbance_load")
        + 0.14 * f(row, "exposure")
        - 0.10 * f(row, "adaptive_capacity")
        - 0.07 * f(row, "system_memory")
        - 0.05 * f(row, "recovery_speed")
    )


def diagnostic(row: dict[str, str], risk: float) -> str:
    if risk >= 0.55:
        return "high threshold-risk concern"
    if f(row, "recovery_speed") < 0.38 or f(row, "adaptive_capacity") < 0.46:
        return "low recovery or adaptive-capacity concern"
    if f(row, "feedback_strength") >= 0.72:
        return "feedback amplification concern"
    return "mixed threshold profile requiring monitoring"


def update_state(x: float, pressure: float, r: float = 1.2, dt: float = 0.05) -> float:
    return x + dt * (r * x - x**3 + pressure)


def lag1_autocorr(values: list[float]) -> float | None:
    if len(values) < 3:
        return None
    xs = values[:-1]
    ys = values[1:]
    mean_x = mean(xs)
    mean_y = mean(ys)
    denom_x = sum((x - mean_x) ** 2 for x in xs)
    denom_y = sum((y - mean_y) ** 2 for y in ys)
    if denom_x == 0 or denom_y == 0:
        return None
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    return num / math.sqrt(denom_x * denom_y)


def rolling_indicators(rows: list[dict[str, object]], window: int = 16) -> list[dict[str, object]]:
    output = []
    states = [float(r["state"]) for r in rows]

    for i, row in enumerate(rows):
        segment = states[max(0, i - window + 1): i + 1]
        row_out = dict(row)

        if len(segment) >= window:
            var_value = variance(segment)
            ac_value = lag1_autocorr(segment)
            row_out["rolling_variance"] = round(var_value, 6)
            row_out["rolling_autocorr"] = round(ac_value, 6) if ac_value is not None else ""
            row_out["recovery_speed_proxy"] = round(1.0 - ac_value, 6) if ac_value is not None else ""
        else:
            row_out["rolling_variance"] = ""
            row_out["rolling_autocorr"] = ""
            row_out["recovery_speed_proxy"] = ""

        output.append(row_out)

    return output


def simulate_hysteresis(scenario: dict[str, str], seed: int = 42) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rng = random.Random(seed)
    steps = int(float(scenario["steps"]))
    start = float(scenario["pressure_start"])
    end = float(scenario["pressure_end"])
    noise_level = float(scenario["noise_level"])

    pressures_forward = [start + (end - start) * i / (steps - 1) for i in range(steps)]
    pressures_backward = [end + (start - end) * i / (steps - 1) for i in range(steps)]

    rows: list[dict[str, object]] = []

    x = -0.90
    for step, pressure in enumerate(pressures_forward, start=1):
        x = update_state(x, pressure) + rng.gauss(0.0, noise_level)
        rows.append(
            {
                "scenario_id": scenario["scenario_id"],
                "scenario_name": scenario["scenario_name"],
                "step": step,
                "pressure": round(pressure, 6),
                "state": round(x, 6),
                "direction": "Increasing Pressure",
                "regime": "upper regime" if x >= 0 else "lower regime",
            }
        )

    x_backward = x
    for step, pressure in enumerate(pressures_backward, start=1):
        x_backward = update_state(x_backward, pressure) + rng.gauss(0.0, noise_level)
        rows.append(
            {
                "scenario_id": scenario["scenario_id"],
                "scenario_name": scenario["scenario_name"],
                "step": step,
                "pressure": round(pressure, 6),
                "state": round(x_backward, 6),
                "direction": "Decreasing Pressure",
                "regime": "upper regime" if x_backward >= 0 else "lower regime",
            }
        )

    forward_rows = [r for r in rows if r["direction"] == "Increasing Pressure"]
    early_warning = rolling_indicators(forward_rows, window=16)

    return rows, early_warning


def main() -> None:
    systems = read_csv(PROFILES_PATH)
    scenarios = read_csv(SCENARIOS_PATH)

    profile_rows = []
    for row in systems:
        risk = threshold_risk_score(row)
        profile_rows.append(
            {
                "system_id": row["system_id"],
                "system_name": row["system_name"],
                "system_type": row["system_type"],
                "critical_function": row["critical_function"],
                "threshold_risk_score": round(risk, 4),
                "pressure": row["pressure"],
                "feedback_strength": row["feedback_strength"],
                "disturbance_load": row["disturbance_load"],
                "adaptive_capacity": row["adaptive_capacity"],
                "system_memory": row["system_memory"],
                "recovery_speed": row["recovery_speed"],
                "diagnostic": diagnostic(row, risk),
            }
        )

    threshold_rows = []
    warning_rows = []
    for scenario in scenarios:
        sim_rows, ew_rows = simulate_hysteresis(scenario)
        threshold_rows.extend(sim_rows)
        warning_rows.extend(ew_rows)

    scenario_summary = []
    for scenario in scenarios:
        sid = scenario["scenario_id"]
        subset = [r for r in threshold_rows if r["scenario_id"] == sid]
        forward = [r for r in subset if r["direction"] == "Increasing Pressure"]
        backward = [r for r in subset if r["direction"] == "Decreasing Pressure"]
        first_upper = next((r for r in forward if r["regime"] == "upper regime"), None)
        last_lower_back = next((r for r in backward if r["regime"] == "lower regime"), None)

        scenario_summary.append(
            {
                "scenario_id": sid,
                "scenario_name": scenario["scenario_name"],
                "forward_transition_pressure": first_upper["pressure"] if first_upper else "",
                "return_transition_pressure": last_lower_back["pressure"] if last_lower_back else "",
                "maximum_state": round(max(float(r["state"]) for r in subset), 4),
                "minimum_state": round(min(float(r["state"]) for r in subset), 4),
            }
        )

    write_csv(OUT_TABLES / "threshold_system_profiles_standard.csv", profile_rows)
    write_csv(OUT_TABLES / "threshold_hysteresis_simulation_standard.csv", threshold_rows)
    write_csv(OUT_TABLES / "threshold_early_warning_signals_standard.csv", warning_rows)
    write_csv(OUT_TABLES / "threshold_scenario_summary_standard.csv", scenario_summary)
    write_csv(DATA_PROCESSED / "threshold_system_profiles_standard.csv", profile_rows)

    print("System thresholds workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    for row in profile_rows:
        print(
            f"  {row['system_name']}: risk={row['threshold_risk_score']} "
            f"diagnostic={row['diagnostic']}"
        )


if __name__ == "__main__":
    main()
