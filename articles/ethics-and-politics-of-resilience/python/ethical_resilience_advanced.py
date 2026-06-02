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
    "protection_effectiveness",
    "equity",
    "governance_legitimacy",
    "recognition",
    "accountability",
]
PENALTIES = ["burden_shift", "implementation_burden"]

def compute(df, weights):
    result = df.copy()
    value = np.zeros(len(result))
    for col in BENEFITS:
        value += float(weights[f"{col}_weight"]) * result[col]
    for col in PENALTIES:
        value -= float(weights[f"{col}_weight"]) * result[col]

    result["ethical_resilience_value"] = value
    result["equity_gap"] = np.maximum(0, 8.5 - result["equity"])
    result["governance_gap"] = np.maximum(0, 8.5 - result["governance_legitimacy"])
    result["recognition_gap"] = np.maximum(0, 8.5 - result["recognition"])

    result["adjusted_ethical_resilience_value"] = (
        result["ethical_resilience_value"]
        - 0.06 * result["equity_gap"]
        - 0.06 * result["governance_gap"]
        - 0.05 * result["recognition_gap"]
    )
    return result.sort_values("adjusted_ethical_resilience_value", ascending=False)

def main():
    strategies = pd.read_csv(ROOT / "data/raw/ethical_resilience_strategies.csv")
    scenarios = pd.read_csv(ROOT / "data/raw/ethical_resilience_priority_scenarios.csv")
    balanced = scenarios.loc[scenarios["scenario"] == "Balanced"].iloc[0]

    baseline = compute(strategies, balanced)
    baseline.to_csv(OUT_TABLES / "ethical_resilience_baseline_advanced.csv", index=False)

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
                "adjusted_ethical_resilience_value": row["adjusted_ethical_resilience_value"],
            })

    simulation = pd.DataFrame(rows)
    robustness = (
        simulation.groupby(["strategy_id", "strategy"])
        .agg(
            mean_adjusted_value=("adjusted_ethical_resilience_value", "mean"),
            median_adjusted_value=("adjusted_ethical_resilience_value", "median"),
            probability_ranked_first=("rank", lambda x: (x == 1).mean() * 100),
            probability_top_two=("rank", lambda x: (x <= 2).mean() * 100),
            probability_bottom_two=("rank", lambda x: (x >= len(strategies) - 1).mean() * 100),
        )
        .reset_index()
        .sort_values("probability_ranked_first", ascending=False)
    )

    simulation.to_csv(OUT_TABLES / "ethical_resilience_uncertainty_simulation_advanced.csv", index=False)
    robustness.to_csv(OUT_TABLES / "ethical_resilience_robustness_summary_advanced.csv", index=False)

    plt.figure(figsize=(10, 6))
    plt.bar(robustness["strategy"], robustness["probability_ranked_first"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Probability ranked first (%)")
    plt.title("Robustness of Justice-Sensitive Resilience Choices Under Uncertainty")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "ethical_resilience_probability_ranked_first.png", dpi=160)
    plt.close()

    print("Advanced ethical resilience workflow complete.")
    print(robustness.round(4))

if __name__ == "__main__":
    main()
