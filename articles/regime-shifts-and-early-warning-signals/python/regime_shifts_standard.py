#!/usr/bin/env python3
"""
Dependency-light regime-shift and early-warning workflow.

Reads synthetic regime profiles and scenarios, calculates regime-shift risk,
simulates nonlinear transition paths, computes rolling variance, lag-1
autocorrelation, recovery-speed proxies, and threshold-proximity scores.

Run:
    python3 python/regime_shifts_standard.py
"""

from __future__ import annotations

import csv
import math
import random
from pathlib import Path
from statistics import mean, variance


ROOT = Path(__file__).resolve().parents[1]
PROFILES_PATH = ROOT / "data" / "raw" / "regime_system_profiles.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "regime_scenarios.csv"
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


def regime_risk_score(row: dict[str, str]) -> float:
    return max(0.0, min(1.0,
        0.18 * f(row, "pressure")
        + 0.17 * f(row, "feedback_strength")
        + 0.15 * f(row, "variance_signal")
        + 0.15 * f(row, "autocorr_signal")
        + 0.12 * f(row, "exposure")
        - 0.08 * f(row, "recovery_speed")
        - 0.06 * f(row, "adaptive_capacity")
        - 0.04 * f(row, "system_memory")
        - 0.03 * f(row, "monitoring_quality")
        - 0.02 * f(row, "justice_visibility")
    ))


def threshold_protection_score(row: dict[str, str]) -> float:
    return max(0.0, min(1.0,
        0.22 * f(row, "recovery_speed")
        + 0.20 * f(row, "adaptive_capacity")
        + 0.18 * f(row, "system_memory")
        + 0.16 * f(row, "monitoring_quality")
        + 0.12 * f(row, "justice_visibility")
        + 0.12 * (1.0 - f(row, "feedback_strength"))
    ))


def diagnostic(row: dict[str, str], risk: float) -> str:
    if risk >= 0.55:
        return "high regime-shift risk concern"
    if f(row, "recovery_speed") < 0.38:
        return "critical slowing and weak recovery concern"
    if f(row, "monitoring_quality") < 0.50:
        return "monitoring quality concern"
    if f(row, "justice_visibility") < 0.45:
        return "unequal warning and justice visibility concern"
    return "mixed regime profile requiring monitoring"


def update_state(x: float, pressure: float, r: float = 1.2, dt: float = 0.05) -> float:
    return x + dt * (r * x - x**3 + pressure)


def lag1_autocorr(values: list[float]) -> float | None:
    if len(values) < 3:
        return None
    xs = values[:-1]
    ys = values[1:]
    mx = mean(xs)
    my = mean(ys)
    denom_x = sum((x - mx) ** 2 for x in xs)
    denom_y = sum((y - my) ** 2 for y in ys)
    if denom_x == 0 or denom_y == 0:
        return None
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return num / math.sqrt(denom_x * denom_y)


def percentile_ranks(values: list[float | None]) -> list[float | None]:
    clean = sorted(v for v in values if v is not None)
    if not clean:
        return [None for _ in values]
    ranks = []
    for v in values:
        if v is None:
            ranks.append(None)
        else:
            count = sum(1 for x in clean if x <= v)
            ranks.append(count / len(clean))
    return ranks


def rolling_indicators(rows: list[dict[str, object]], window: int = 18) -> list[dict[str, object]]:
    states = [float(r["state"]) for r in rows]
    variances: list[float | None] = []
    autocorrs: list[float | None] = []

    for i in range(len(states)):
        segment = states[max(0, i - window + 1): i + 1]
        if len(segment) >= window:
            variances.append(variance(segment))
            autocorrs.append(lag1_autocorr(segment))
        else:
            variances.append(None)
            autocorrs.append(None)

    variance_ranks = percentile_ranks(variances)
    autocorr_ranks = percentile_ranks(autocorrs)

    output = []
    for i, row in enumerate(rows):
        out = dict(row)
        rv = variances[i]
        ac = autocorrs[i]
        vr = variance_ranks[i]
        ar = autocorr_ranks[i]
        out["rolling_variance"] = round(rv, 6) if rv is not None else ""
        out["rolling_autocorr"] = round(ac, 6) if ac is not None else ""
        out["recovery_speed_proxy"] = round(1.0 - ac, 6) if ac is not None else ""
        out["threshold_proximity_score"] = round((vr + ar) / 2, 6) if vr is not None and ar is not None else ""
        output.append(out)

    return output


def simulate_scenario(scenario: dict[str, str], seed: int = 42) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rng = random.Random(seed + int(scenario["scenario_id"][-1]))
    steps = int(float(scenario["steps"]))
    start = float(scenario["pressure_start"])
    end = float(scenario["pressure_end"])
    noise_level = float(scenario["noise_level"])
    intervention = float(scenario["adaptive_intervention"])

    rows = []
    x = -0.90

    for step in range(1, steps + 1):
        base_pressure = start + (end - start) * (step - 1) / (steps - 1)
        intervention_effect = intervention * min(1.0, step / steps)
        pressure = base_pressure - 0.18 * intervention_effect

        if step > 1:
            x = update_state(x, pressure) + rng.gauss(0.0, noise_level)

        rows.append(
            {
                "scenario_id": scenario["scenario_id"],
                "scenario_name": scenario["scenario_name"],
                "time_step": step,
                "pressure": round(pressure, 6),
                "state": round(x, 6),
                "regime": "upper regime" if x >= 0 else "lower regime",
                "monitoring_quality": scenario["monitoring_quality"],
            }
        )

    warning_rows = rolling_indicators(rows, window=18)
    return rows, warning_rows


def main() -> None:
    profiles = read_csv(PROFILES_PATH)
    scenarios = read_csv(SCENARIOS_PATH)

    profile_rows = []
    for row in profiles:
        risk = regime_risk_score(row)
        protection = threshold_protection_score(row)
        profile_rows.append(
            {
                "system_id": row["system_id"],
                "system_name": row["system_name"],
                "system_type": row["system_type"],
                "critical_function": row["critical_function"],
                "regime_risk_score": round(risk, 5),
                "threshold_protection_score": round(protection, 5),
                "pressure": row["pressure"],
                "feedback_strength": row["feedback_strength"],
                "variance_signal": row["variance_signal"],
                "autocorr_signal": row["autocorr_signal"],
                "recovery_speed": row["recovery_speed"],
                "adaptive_capacity": row["adaptive_capacity"],
                "system_memory": row["system_memory"],
                "monitoring_quality": row["monitoring_quality"],
                "justice_visibility": row["justice_visibility"],
                "exposure": row["exposure"],
                "diagnostic": diagnostic(row, risk),
            }
        )

    regime_rows = []
    warning_rows = []
    for scenario in scenarios:
        sim, ew = simulate_scenario(scenario)
        regime_rows.extend(sim)
        warning_rows.extend(ew)

    scenario_summary = []
    for sid in sorted({r["scenario_id"] for r in warning_rows}):
        subset = [r for r in warning_rows if r["scenario_id"] == sid]
        upper = [r for r in subset if r["regime"] == "upper regime"]
        prox = [float(r["threshold_proximity_score"]) for r in subset if r["threshold_proximity_score"] != ""]
        autoc = [float(r["rolling_autocorr"]) for r in subset if r["rolling_autocorr"] != ""]
        vars_ = [float(r["rolling_variance"]) for r in subset if r["rolling_variance"] != ""]
        rec = [float(r["recovery_speed_proxy"]) for r in subset if r["recovery_speed_proxy"] != ""]
        scenario_summary.append(
            {
                "scenario_id": sid,
                "scenario_name": subset[0]["scenario_name"],
                "transition_time": upper[0]["time_step"] if upper else "",
                "max_threshold_proximity_score": round(max(prox), 5) if prox else "",
                "max_rolling_autocorr": round(max(autoc), 5) if autoc else "",
                "max_rolling_variance": round(max(vars_), 5) if vars_ else "",
                "min_recovery_speed_proxy": round(min(rec), 5) if rec else "",
            }
        )

    write_csv(OUT_TABLES / "regime_system_profiles_standard.csv", profile_rows)
    write_csv(OUT_TABLES / "regime_shift_simulation_standard.csv", regime_rows)
    write_csv(OUT_TABLES / "early_warning_indicators_standard.csv", warning_rows)
    write_csv(OUT_TABLES / "regime_shift_scenario_summary_standard.csv", scenario_summary)
    write_csv(DATA_PROCESSED / "regime_system_profiles_standard.csv", profile_rows)

    print("Regime shifts workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    for row in profile_rows:
        print(
            f"  {row['system_name']}: risk={row['regime_risk_score']} "
            f"protection={row['threshold_protection_score']} diagnostic={row['diagnostic']}"
        )


if __name__ == "__main__":
    main()
