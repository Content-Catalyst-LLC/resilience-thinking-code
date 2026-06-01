#!/usr/bin/env python3
"""
Advanced historical resilience-theory workflow.

Uses pandas, numpy, and matplotlib.

Run:
    pip install -r requirements-advanced.txt
    python python/history_resilience_theory_advanced.py
"""

from __future__ import annotations

from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
except ImportError as exc:
    raise SystemExit(
        "Missing advanced dependency. Run: pip install -r requirements-advanced.txt"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw" / "resilience_theory_historical_phases.csv"
CONCEPTS = ROOT / "data" / "raw" / "resilience_theory_key_concepts.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_FIGURES = ROOT / "outputs" / "figures"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)


def build_phase_scores(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["influence_score"] = (
        0.35 * out["conceptual_scope"]
        + 0.25 * out["governance_relevance"]
        + 0.25 * out["system_complexity"]
        + 0.15 * out["justice_relevance"]
    )
    out["conceptual_delta"] = out["conceptual_scope"].diff().fillna(0)
    out["governance_delta"] = out["governance_relevance"].diff().fillna(0)
    out["justice_delta"] = out["justice_relevance"].diff().fillna(0)
    return out


def simulate_models(steps: int = 160) -> pd.DataFrame:
    time = np.arange(1, steps + 1)

    x_star = 0.0
    a = 0.10
    equilibrium = np.zeros(steps)
    equilibrium[0] = 1.0

    for t in range(1, steps):
        equilibrium[t] = equilibrium[t - 1] - a * (equilibrium[t - 1] - x_star)

    threshold_state = np.zeros(steps)
    threshold_state[0] = -0.9
    pressure = np.linspace(-0.45, 0.85, steps)
    r = 1.1
    dt = 0.05

    for t in range(1, steps):
        threshold_state[t] = threshold_state[t - 1] + dt * (
            r * threshold_state[t - 1] - threshold_state[t - 1] ** 3 + pressure[t]
        )

    basin_width = np.linspace(0.85, 0.45, steps)
    disturbance_load = np.linspace(0.10, 0.70, steps)
    adaptive_capacity = 0.35 + 0.20 * np.sin(time / 18)
    resilience_margin = basin_width - disturbance_load + adaptive_capacity

    return pd.DataFrame(
        {
            "time": time,
            "equilibrium_state": equilibrium,
            "threshold_state": threshold_state,
            "pressure": pressure,
            "basin_width": basin_width,
            "disturbance_load": disturbance_load,
            "adaptive_capacity": adaptive_capacity,
            "resilience_margin": resilience_margin,
        }
    )


def plot_history(history: pd.DataFrame) -> None:
    long = history.melt(
        id_vars=["period", "start_year"],
        value_vars=[
            "conceptual_scope",
            "governance_relevance",
            "system_complexity",
            "justice_relevance",
        ],
        var_name="dimension",
        value_name="value",
    )

    plt.figure(figsize=(10, 6))
    for dimension, subset in long.groupby("dimension"):
        plt.plot(subset["start_year"], subset["value"], marker="o", label=dimension)
    plt.xlabel("Year")
    plt.ylabel("Relative emphasis")
    plt.title("Stylized Historical Expansion of Resilience Theory")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "historical_expansion_dimensions.png", dpi=160)
    plt.close()

    ranked = history.sort_values("influence_score", ascending=True)
    plt.figure(figsize=(10, 7))
    plt.barh(ranked["period"], ranked["influence_score"])
    plt.xlabel("Influence score")
    plt.title("Stylized Influence Score Across Historical Phases")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "historical_phase_influence_scores.png", dpi=160)
    plt.close()


def plot_models(models: pd.DataFrame) -> None:
    plt.figure(figsize=(10, 6))
    plt.plot(models["time"], models["equilibrium_state"], label="Equilibrium return")
    plt.plot(models["time"], models["threshold_state"], label="Threshold dynamics")
    plt.xlabel("Time step")
    plt.ylabel("System state")
    plt.title("From Stability Logic to Resilience Logic")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "equilibrium_vs_threshold_dynamics.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(models["time"], models["resilience_margin"])
    plt.axhline(0, linestyle="--", linewidth=1)
    plt.xlabel("Time step")
    plt.ylabel("Resilience margin")
    plt.title("Stylized Resilience Margin Over Time")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "resilience_margin_over_time.png", dpi=160)
    plt.close()


def main() -> None:
    history = pd.read_csv(DATA)
    concepts = pd.read_csv(CONCEPTS)

    history = build_phase_scores(history)
    models = simulate_models()

    history.to_csv(OUT_TABLES / "history_phase_scores_advanced.csv", index=False)
    concepts.to_csv(OUT_TABLES / "history_key_concepts_advanced.csv", index=False)
    models.to_csv(OUT_TABLES / "equilibrium_vs_threshold_advanced.csv", index=False)

    plot_history(history)
    plot_models(models)

    print("Advanced historical resilience-theory workflow complete.")
    print(history[["period", "start_year", "influence_score"]].round(3))


if __name__ == "__main__":
    main()
