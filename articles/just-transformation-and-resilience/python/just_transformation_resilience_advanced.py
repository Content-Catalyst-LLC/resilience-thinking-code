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
    "resilience_capacity",
    "transformation_capacity",
    "equity",
    "ecological_repair",
    "governance_legitimacy",
    "livelihood_protection",
    "exposure_reduction",
]
PENALTIES = ["burden_shift", "lock_in_risk", "implementation_burden"]

def compute(df, weights):
    result = df.copy()
    value = np.zeros(len(result))
    for col in BENEFITS:
        value += float(weights[f"{col}_weight"]) * result[col]
    for col in PENALTIES:
        value -= float(weights[f"{col}_weight"]) * result[col]

    result["just_transformation_value"] = value
    result["justice_gap"] = (
        0.24 * np.maximum(0, 8.5 - result["equity"])
        + 0.22 * np.maximum(0, 8.5 - result["governance_legitimacy"])
        + 0.20 * np.maximum(0, 8.5 - result["livelihood_protection"])
        + 0.18 * result["burden_shift"]
        + 0.16 * result["lock_in_risk"]
    )
    result["adjusted_value"] = result["just_transformation_value"] - result["justice_gap"]
    return result.sort_values("adjusted_value", ascending=False)

def main():
    pathways = pd.read_csv(ROOT / "data/raw/just_transformation_pathways.csv")
    scenarios = pd.read_csv(ROOT / "data/raw/just_transformation_priority_scenarios.csv")
    balanced = scenarios.loc[scenarios["scenario"] == "Balanced"].iloc[0]

    baseline = compute(pathways, balanced)
    baseline.to_csv(OUT_TABLES / "just_transformation_baseline_advanced.csv", index=False)

    rng = np.random.default_rng(42)
    rows = []
    n_simulations = 5000
    for sim in range(n_simulations):
        sampled = pathways.copy()
        for col in BENEFITS + PENALTIES:
            sampled[col] = rng.normal(pathways[col], 0.60).clip(1, 10)
        scored = compute(sampled, balanced).reset_index(drop=True)
        for rank, row in scored.iterrows():
            rows.append({
                "simulation_id": sim,
                "pathway_id": row["pathway_id"],
                "pathway": row["pathway"],
                "rank": rank + 1,
                "adjusted_value": row["adjusted_value"],
                "justice_gap": row["justice_gap"],
            })

    simulation = pd.DataFrame(rows)
    robustness = (
        simulation.groupby(["pathway_id", "pathway"])
        .agg(
            mean_adjusted_value=("adjusted_value", "mean"),
            median_adjusted_value=("adjusted_value", "median"),
            mean_justice_gap=("justice_gap", "mean"),
            probability_ranked_first=("rank", lambda x: (x == 1).mean() * 100),
            probability_top_two=("rank", lambda x: (x <= 2).mean() * 100),
            probability_bottom_two=("rank", lambda x: (x >= len(pathways) - 1).mean() * 100),
        )
        .reset_index()
        .sort_values("probability_ranked_first", ascending=False)
    )

    simulation.to_csv(OUT_TABLES / "just_transformation_uncertainty_simulation_advanced.csv", index=False)
    robustness.to_csv(OUT_TABLES / "just_transformation_robustness_summary_advanced.csv", index=False)

    plt.figure(figsize=(10, 6))
    plt.bar(robustness["pathway"], robustness["probability_ranked_first"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Probability ranked first (%)")
    plt.title("Robustness of Just Transformation Pathways Under Uncertainty")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "just_transformation_probability_ranked_first.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(robustness["pathway"], robustness["mean_justice_gap"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Mean justice gap")
    plt.title("Mean Justice Gap by Transformation Pathway")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "just_transformation_mean_justice_gap.png", dpi=160)
    plt.close()

    print("Advanced Just Transformation and Resilience workflow complete.")
    print(robustness.round(4))

if __name__ == "__main__":
    main()
