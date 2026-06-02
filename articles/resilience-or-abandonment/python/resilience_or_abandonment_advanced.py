#!/usr/bin/env python3
from pathlib import Path

try:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError as exc:
    raise SystemExit("Missing dependency. Run: pip install -r requirements-advanced.txt") from exc

ROOT = Path(__file__).resolve().parents[1]
OUT_TABLES = ROOT / "outputs/tables"
OUT_FIGURES = ROOT / "outputs/figures"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)

BENEFITS = [
    "protective_effectiveness",
    "material_support",
    "accessible_recovery",
    "governance_inclusion",
    "transformation_potential",
    "exposure_reduction",
]
PENALTIES = ["burden_shift", "implementation_burden"]

def compute(df, weights):
    result = df.copy()
    value = np.zeros(len(result))
    for col in BENEFITS:
        value += float(weights[f"{col}_weight"]) * result[col]
    for col in PENALTIES:
        value -= float(weights[f"{col}_weight"]) * result[col]

    support_gap = np.maximum(0, 8.0 - result["material_support"])
    recovery_gap = np.maximum(0, 8.0 - result["accessible_recovery"])
    governance_gap = np.maximum(0, 8.0 - result["governance_inclusion"])
    exposure_gap = np.maximum(0, 8.0 - result["exposure_reduction"])

    result["support_resilience_value"] = value
    result["abandonment_risk"] = (
        0.32 * support_gap
        + 0.24 * recovery_gap
        + 0.22 * governance_gap
        + 0.14 * result["burden_shift"]
        + 0.08 * exposure_gap
    )
    result["adjusted_value"] = result["support_resilience_value"] - result["abandonment_risk"]
    return result.sort_values("adjusted_value", ascending=False)

def main():
    strategies = pd.read_csv(ROOT / "data/raw/resilience_or_abandonment_strategies.csv")
    scenarios = pd.read_csv(ROOT / "data/raw/abandonment_priority_scenarios.csv")
    balanced = scenarios.loc[scenarios["scenario"] == "Balanced"].iloc[0]

    baseline = compute(strategies, balanced)
    baseline.to_csv(OUT_TABLES / "resilience_or_abandonment_baseline_advanced.csv", index=False)

    rng = np.random.default_rng(42)
    rows = []
    n_simulations = 5000
    for sim in range(n_simulations):
        sampled = strategies.copy()
        for col in BENEFITS + PENALTIES:
            sampled[col] = rng.normal(strategies[col], 0.60).clip(1, 10)
        scored = compute(sampled, balanced).reset_index(drop=True)
        for rank, row in scored.iterrows():
            rows.append({
                "simulation_id": sim,
                "strategy_id": row["strategy_id"],
                "strategy": row["strategy"],
                "rank": rank + 1,
                "adjusted_value": row["adjusted_value"],
                "abandonment_risk": row["abandonment_risk"],
            })

    simulation = pd.DataFrame(rows)
    robustness = (
        simulation.groupby(["strategy_id", "strategy"])
        .agg(
            mean_adjusted_value=("adjusted_value", "mean"),
            median_adjusted_value=("adjusted_value", "median"),
            mean_abandonment_risk=("abandonment_risk", "mean"),
            probability_ranked_first=("rank", lambda x: (x == 1).mean() * 100),
            probability_top_two=("rank", lambda x: (x <= 2).mean() * 100),
            probability_bottom_two=("rank", lambda x: (x >= len(strategies) - 1).mean() * 100),
        )
        .reset_index()
        .sort_values("probability_ranked_first", ascending=False)
    )

    simulation.to_csv(OUT_TABLES / "resilience_or_abandonment_uncertainty_simulation_advanced.csv", index=False)
    robustness.to_csv(OUT_TABLES / "resilience_or_abandonment_robustness_summary_advanced.csv", index=False)

    plt.figure(figsize=(10, 6))
    plt.bar(robustness["strategy"], robustness["probability_ranked_first"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Probability ranked first (%)")
    plt.title("Robustness of Support-Oriented Resilience Under Uncertainty")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "resilience_or_abandonment_probability_ranked_first.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(robustness["strategy"], robustness["mean_abandonment_risk"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Mean abandonment risk")
    plt.title("Mean Abandonment Risk by Strategy")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "resilience_or_abandonment_mean_risk.png", dpi=160)
    plt.close()

    print("Advanced Resilience or Abandonment workflow complete.")
    print(robustness.round(4))

if __name__ == "__main__":
    main()
