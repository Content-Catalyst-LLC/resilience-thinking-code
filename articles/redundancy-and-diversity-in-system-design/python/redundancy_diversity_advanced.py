#!/usr/bin/env python3
"""
Advanced redundancy and diversity workflow.

Uses pandas, numpy, matplotlib, scikit-learn, and joblib.

Run:
    pip install -r requirements-advanced.txt
    python python/redundancy_diversity_advanced.py
"""

from __future__ import annotations

from pathlib import Path

try:
    import joblib
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, brier_score_loss, f1_score, precision_score, recall_score, roc_auc_score
    from sklearn.model_selection import train_test_split
except ImportError as exc:
    raise SystemExit("Missing advanced dependency. Run: pip install -r requirements-advanced.txt") from exc


ROOT = Path(__file__).resolve().parents[1]
STRATEGIES_PATH = ROOT / "data" / "raw" / "redundancy_diversity_strategies.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "redundancy_diversity_scenarios.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_FIGURES = ROOT / "outputs" / "figures"
OUT_MODELS = ROOT / "outputs" / "models"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)
OUT_MODELS.mkdir(parents=True, exist_ok=True)

BENEFIT_CRITERIA = [
    "redundancy",
    "diversity",
    "response_diversity",
    "coordination_capacity",
    "justice_contribution",
    "maintenance_reliability",
]

FEATURES = BENEFIT_CRITERIA + ["common_mode_risk"]


def calculate_base_profiles(strategies: pd.DataFrame) -> pd.DataFrame:
    out = strategies.copy()
    out["base_resilience_value"] = (
        0.22 * out["redundancy"]
        + 0.18 * out["diversity"]
        + 0.22 * out["response_diversity"]
        + 0.13 * out["coordination_capacity"]
        + 0.10 * out["justice_contribution"]
        + 0.07 * out["maintenance_reliability"]
        - 0.08 * out["common_mode_risk"]
    )

    conditions = [
        (out["base_resilience_value"] >= 7.25) & (out["common_mode_risk"] <= 3.7),
        out["common_mode_risk"] >= 4.0,
        out["coordination_capacity"] < 7.5,
        out["justice_contribution"] < 7.6,
        out["maintenance_reliability"] < 7.4,
    ]
    choices = [
        "strong diverse-redundancy profile with manageable common-mode risk",
        "common-mode failure review needed",
        "coordination and interoperability constraint",
        "justice contribution needs stronger design",
        "maintenance reliability needs stronger evidence",
    ]
    out["diagnostic"] = np.select(conditions, choices, default="promising but requires stress testing and validation")
    return out


def score_strategies(strategies: pd.DataFrame, scenario: pd.Series) -> pd.DataFrame:
    result = strategies.copy()
    result["resilience_value"] = (
        scenario["redundancy_weight"] * result["redundancy"]
        + scenario["diversity_weight"] * result["diversity"]
        + scenario["response_diversity_weight"] * result["response_diversity"]
        + scenario["coordination_capacity_weight"] * result["coordination_capacity"]
        + scenario["justice_contribution_weight"] * result["justice_contribution"]
        + scenario["maintenance_reliability_weight"] * result["maintenance_reliability"]
        - scenario["common_mode_risk_weight"] * result["common_mode_risk"]
    )
    result = result.sort_values("resilience_value", ascending=False).reset_index(drop=True)
    result["rank"] = np.arange(1, len(result) + 1)
    result["scenario"] = scenario["scenario"]
    return result


def scenario_rankings(strategies: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, scenario in scenarios.iterrows():
        rows.append(score_strategies(strategies, scenario))
    return pd.concat(rows, ignore_index=True)


def monte_carlo(strategies: pd.DataFrame, scenario: pd.Series, n: int = 5000) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(42)
    rows = []

    for simulation_id in range(n):
        sampled = strategies.copy()
        for criterion in FEATURES:
            sampled[criterion] = rng.normal(loc=strategies[criterion], scale=0.6)
            sampled[criterion] = sampled[criterion].clip(1, 10)

        scored = score_strategies(sampled, scenario)

        for _, row in scored.iterrows():
            rows.append(
                {
                    "simulation_id": simulation_id,
                    "strategy_id": row["strategy_id"],
                    "strategy": row["strategy"],
                    "rank": int(row["rank"]),
                    "resilience_value": row["resilience_value"],
                    "winner": scored.iloc[0]["strategy"],
                }
            )

    simulation = pd.DataFrame(rows)

    robustness = (
        simulation.groupby(["strategy_id", "strategy"])
        .agg(
            mean_resilience_value=("resilience_value", "mean"),
            median_resilience_value=("resilience_value", "median"),
            probability_ranked_first=("rank", lambda x: (x == 1).mean() * 100),
            probability_top_two=("rank", lambda x: (x <= 2).mean() * 100),
            probability_bottom_two=("rank", lambda x: (x >= len(strategies) - 1).mean() * 100),
        )
        .reset_index()
        .sort_values("probability_ranked_first", ascending=False)
    )

    return simulation, robustness


def expand_training(strategies: pd.DataFrame, n: int = 2600) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []

    for _ in range(n):
        base = strategies.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]
        record = {}

        for feature in FEATURES:
            record[feature] = float(np.clip(float(base[feature]) + rng.normal(0, 0.7), 1, 10))

        value = (
            0.22 * record["redundancy"]
            + 0.18 * record["diversity"]
            + 0.22 * record["response_diversity"]
            + 0.13 * record["coordination_capacity"]
            + 0.10 * record["justice_contribution"]
            + 0.07 * record["maintenance_reliability"]
            - 0.08 * record["common_mode_risk"]
            + rng.normal(0, 0.18)
        )

        record["resilience_value"] = value
        record["high_resilience_manageable_common_mode"] = 1 if value >= 7.20 and record["common_mode_risk"] <= 3.9 else 0
        rows.append(record)

    return pd.DataFrame(rows)


def plot_outputs(profiles: pd.DataFrame, rankings: pd.DataFrame, robustness: pd.DataFrame, importance: pd.DataFrame | None = None) -> None:
    profile_plot = profiles[
        [
            "strategy",
            "base_resilience_value",
            "redundancy",
            "diversity",
            "response_diversity",
            "coordination_capacity",
            "justice_contribution",
            "maintenance_reliability",
            "common_mode_risk",
        ]
    ].melt(id_vars="strategy", var_name="criterion", value_name="value")

    order = profiles.sort_values("base_resilience_value")["strategy"].tolist()

    plt.figure(figsize=(11, 7))
    for criterion, subset in profile_plot.groupby("criterion"):
        y = [order.index(p) for p in subset["strategy"]]
        plt.scatter(subset["value"], y, label=criterion, s=50)
    plt.yticks(range(len(order)), order)
    plt.xlabel("Criterion value")
    plt.title("Redundancy, Diversity, and Common-Mode Risk Profiles")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "redundancy_diversity_strategy_profiles.png", dpi=160)
    plt.close()

    pivot = rankings.pivot(index="strategy", columns="scenario", values="resilience_value")
    plt.figure(figsize=(11, 7))
    for scenario in pivot.columns:
        plt.plot(pivot.index, pivot[scenario], marker="o", label=scenario)
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Resilience value")
    plt.title("Strategy Value Across Redundancy and Diversity Priorities")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "redundancy_diversity_scenario_rankings.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(robustness["strategy"], robustness["probability_ranked_first"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Probability ranked first (%)")
    plt.title("Robustness of Redundancy and Diversity Choices")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "monte_carlo_probability_ranked_first.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(robustness["strategy"], robustness["probability_top_two"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Probability ranked in top two (%)")
    plt.title("Top-Two Robustness of Redundancy and Diversity Choices")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "monte_carlo_probability_top_two.png", dpi=160)
    plt.close()

    if importance is not None:
        plt.figure(figsize=(10, 6))
        plt.barh(importance["feature"], importance["importance"])
        plt.gca().invert_yaxis()
        plt.xlabel("Importance")
        plt.title("Feature Importance for Resilience-Design Classification")
        plt.tight_layout()
        plt.savefig(OUT_FIGURES / "advanced_feature_importance.png", dpi=160)
        plt.close()


def main() -> None:
    strategies = pd.read_csv(STRATEGIES_PATH)
    scenarios = pd.read_csv(SCENARIOS_PATH)

    profiles = calculate_base_profiles(strategies)
    rankings = scenario_rankings(strategies, scenarios)
    baseline = scenarios.loc[scenarios["scenario"] == "Balanced"].iloc[0]
    simulation, robustness = monte_carlo(strategies, baseline, n=5000)

    profiles.to_csv(OUT_TABLES / "redundancy_diversity_profiles_advanced.csv", index=False)
    rankings.to_csv(OUT_TABLES / "redundancy_diversity_rankings_advanced.csv", index=False)
    simulation.to_csv(OUT_TABLES / "redundancy_diversity_monte_carlo_advanced.csv", index=False)
    robustness.to_csv(OUT_TABLES / "redundancy_diversity_robustness_summary_advanced.csv", index=False)

    training = expand_training(strategies)
    X = training[FEATURES]
    y = training["high_resilience_manageable_common_mode"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=450,
        min_samples_leaf=6,
        class_weight="balanced",
        random_state=42,
    )
    model.fit(X_train, y_train)

    prob = model.predict_proba(X_test)[:, 1]
    pred = (prob >= 0.50).astype(int)

    metrics = pd.DataFrame(
        [{
            "model": "random_forest_resilience_design_classifier",
            "accuracy": accuracy_score(y_test, pred),
            "precision": precision_score(y_test, pred, zero_division=0),
            "recall": recall_score(y_test, pred, zero_division=0),
            "f1": f1_score(y_test, pred, zero_division=0),
            "roc_auc": roc_auc_score(y_test, prob),
            "brier_score": brier_score_loss(y_test, prob),
        }]
    )

    importance = pd.DataFrame(
        {
            "feature": FEATURES,
            "importance": model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)

    training.to_csv(OUT_TABLES / "synthetic_resilience_design_training_data.csv", index=False)
    metrics.to_csv(OUT_TABLES / "advanced_resilience_design_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "resilience_design_classifier.joblib")

    plot_outputs(profiles, rankings, robustness, importance)

    print("Advanced redundancy and diversity workflow complete.")
    print(profiles[["strategy", "base_resilience_value", "diagnostic"]].round(4))
    print(metrics.round(4))


if __name__ == "__main__":
    main()
