#!/usr/bin/env python3
"""
Advanced Python resilience diagnostics.

Uses pandas/numpy/matplotlib when available. If dependencies are missing,
install with:

    pip install -r requirements-advanced.txt

Run:
    python python/resilience_diagnostics_advanced.py
"""

from __future__ import annotations

from pathlib import Path

try:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError as exc:
    raise SystemExit(
        "Missing advanced dependency. Run: pip install -r requirements-advanced.txt"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw" / "synthetic_resilience_systems.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_FIGURES = ROOT / "outputs" / "figures"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)


def build_profiles(systems: pd.DataFrame) -> pd.DataFrame:
    systems = systems.copy()
    systems["resilience_profile"] = (
        0.24 * systems["adaptive_capacity"]
        + 0.20 * systems["threshold_distance"]
        + 0.18 * systems["learning_capacity"]
        + 0.14 * systems["modularity"]
        + 0.14 * systems["redundancy"]
        - 0.05 * systems["exposure"]
        - 0.05 * systems["sensitivity"]
    )
    systems["risk_pressure"] = 0.55 * systems["exposure"] + 0.45 * systems["sensitivity"]
    systems["viability_margin"] = (
        systems["resilience_profile"] + systems["threshold_distance"] - systems["risk_pressure"]
    )
    systems["vulnerability_flag"] = np.select(
        [
            systems["viability_margin"] < 0.15,
            systems["viability_margin"] < 0.30,
        ],
        [
            "high threshold risk",
            "moderate threshold risk",
        ],
        default="lower threshold risk",
    )
    return systems


def simulate(systems: pd.DataFrame, steps: int = 72) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    time_steps = np.arange(1, steps + 1)
    baseline = rng.uniform(0.035, 0.095, steps)
    shocks = np.zeros(steps)
    shocks[[11, 23, 36, 47, 60]] = [0.20, 0.28, 0.23, 0.31, 0.18]
    disturbance = baseline + shocks

    rows = []
    for _, row in systems.iterrows():
        viability = 1.0
        learning_memory = 0.0

        for time_step, d in zip(time_steps, disturbance):
            disturbance_load = d * (0.65 + row.exposure) * (0.55 + row.sensitivity)
            protective_structure = 0.35 * row.redundancy + 0.25 * row.modularity
            adaptive_response = (
                0.028 * row.adaptive_capacity
                + 0.012 * row.learning_capacity * (1 + learning_memory)
            )

            net_impact = disturbance_load * (1 - 0.45 * protective_structure)
            viability = float(np.clip(viability - net_impact + adaptive_response, 0.0, 1.25))
            learning_memory += 0.01 * row.learning_capacity

            margin = viability + row.threshold_distance - row.risk_pressure

            rows.append(
                {
                    "system_id": row.system_id,
                    "system_type": row.system_type,
                    "time_step": int(time_step),
                    "disturbance": float(d),
                    "viability": viability,
                    "viability_margin": margin,
                    "threshold_flag": "threshold risk" if margin < 0.20 else "viable margin",
                }
            )

    return pd.DataFrame(rows)


def plot_viability(simulation: pd.DataFrame) -> None:
    plt.figure(figsize=(10, 6))
    for name, subset in simulation.groupby("system_type"):
        plt.plot(subset["time_step"], subset["viability"], label=name)
    plt.axhline(0.30, linestyle="--", linewidth=1, label="Low viability reference")
    plt.xlabel("Time step")
    plt.ylabel("Viability")
    plt.title("Stylized Viability Under Repeated Disturbance")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "viability_under_repeated_disturbance.png", dpi=160)
    plt.close()


def plot_margin(simulation: pd.DataFrame) -> None:
    plt.figure(figsize=(10, 6))
    for name, subset in simulation.groupby("system_type"):
        plt.plot(subset["time_step"], subset["viability_margin"], label=name)
    plt.axhline(0.20, linestyle="--", linewidth=1, label="Threshold-risk reference")
    plt.xlabel("Time step")
    plt.ylabel("Viability margin")
    plt.title("Threshold Margin Under Repeated Disturbance")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "threshold_margin_under_disturbance.png", dpi=160)
    plt.close()


def main() -> None:
    systems = pd.read_csv(DATA)
    profiles = build_profiles(systems)
    simulation = simulate(profiles)

    summary = (
        simulation.groupby(["system_id", "system_type"], as_index=False)
        .agg(
            minimum_viability=("viability", "min"),
            average_viability=("viability", "mean"),
            minimum_margin=("viability_margin", "min"),
            threshold_risk_steps=("threshold_flag", lambda s: int((s == "threshold risk").sum())),
        )
        .sort_values("minimum_margin")
    )

    profiles.to_csv(OUT_TABLES / "resilience_profiles_advanced.csv", index=False)
    simulation.to_csv(OUT_TABLES / "resilience_simulation_advanced.csv", index=False)
    summary.to_csv(OUT_TABLES / "resilience_summary_advanced.csv", index=False)

    plot_viability(simulation)
    plot_margin(simulation)

    print(summary.round(3))
    print(f"\nWrote outputs to {OUT_TABLES} and {OUT_FIGURES}")


if __name__ == "__main__":
    main()
