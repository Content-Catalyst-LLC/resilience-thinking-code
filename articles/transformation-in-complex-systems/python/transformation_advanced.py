#!/usr/bin/env python3
"""
Advanced transformation pathway workflow.

Uses pandas, numpy, matplotlib, scikit-learn, and joblib.

Run:
    pip install -r requirements-advanced.txt
    python python/transformation_advanced.py
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
PATHWAYS_PATH = ROOT / "data" / "raw" / "transformation_pathways.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "transformation_scenarios.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_FIGURES = ROOT / "outputs" / "figures"
OUT_MODELS = ROOT / "outputs" / "models"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)
OUT_MODELS.mkdir(parents=True, exist_ok=True)

BENEFIT_CRITERIA = [
    "adaptive_support",
    "transformability",
    "governance_readiness",
    "justice_contribution",
    "ecological_viability",
    "legitimacy",
    "resource_feasibility",
]

FEATURES = BENEFIT_CRITERIA + ["structural_risk"]


def calculate_readiness(pathways: pd.DataFrame) -> pd.DataFrame:
    out = pathways.copy()
    out["transformation_readiness"] = (
        0.18 * out["adaptive_support"]
        + 0.20 * out["transformability"]
        + 0.18 * out["governance_readiness"]
        + 0.16 * out["justice_contribution"]
        + 0.14 * out["ecological_viability"]
        + 0.08 * out["legitimacy"]
        + 0.06 * out["resource_feasibility"]
        - 0.10 * out["structural_risk"]
    )

    conditions = [
        (out["transformation_readiness"] >= 7.55) & (out["structural_risk"] <= 4.1),
        out["justice_contribution"] < 7.5,
        out["governance_readiness"] < 7.4,
        out["resource_feasibility"] < 7.0,
    ]
    choices = [
        "high readiness with manageable structural-risk concern",
        "justice contribution needs stronger design",
        "governance readiness constraint",
        "resource feasibility constraint",
    ]
    out["diagnostic"] = np.select(conditions, choices, default="promising but requires participatory validation")
    return out


def score_pathways(pathways: pd.DataFrame, scenario: pd.Series) -> pd.DataFrame:
    result = pathways.copy()
    result["transformation_value"] = (
        scenario["adaptive_support_weight"] * result["adaptive_support"]
        + scenario["transformability_weight"] * result["transformability"]
        + scenario["governance_readiness_weight"] * result["governance_readiness"]
        + scenario["justice_contribution_weight"] * result["justice_contribution"]
        + scenario["ecological_viability_weight"] * result["ecological_viability"]
        + scenario["legitimacy_weight"] * result["legitimacy"]
        + scenario["resource_feasibility_weight"] * result["resource_feasibility"]
        - scenario["structural_risk_weight"] * result["structural_risk"]
    )
    result = result.sort_values("transformation_value", ascending=False).reset_index(drop=True)
    result["rank"] = np.arange(1, len(result) + 1)
    result["scenario"] = scenario["scenario"]
    return result


def scenario_rankings(pathways: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, scenario in scenarios.iterrows():
        rows.append(score_pathways(pathways, scenario))
    return pd.concat(rows, ignore_index=True)


def monte_carlo(pathways: pd.DataFrame, scenario: pd.Series, n: int = 5000) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(42)
    rows = []

    for simulation_id in range(n):
        sampled = pathways.copy()
        for criterion in FEATURES:
            sampled[criterion] = rng.normal(loc=pathways[criterion], scale=0.6)
            sampled[criterion] = sampled[criterion].clip(1, 10)

        scored = score_pathways(sampled, scenario)

        for _, row in scored.iterrows():
            rows.append(
                {
                    "simulation_id": simulation_id,
                    "pathway_id": row["pathway_id"],
                    "pathway": row["pathway"],
                    "rank": int(row["rank"]),
                    "transformation_value": row["transformation_value"],
                    "winner": scored.iloc[0]["pathway"],
                }
            )

    simulation = pd.DataFrame(rows)

    robustness = (
        simulation.groupby(["pathway_id", "pathway"])
        .agg(
            mean_transformation_value=("transformation_value", "mean"),
            median_transformation_value=("transformation_value", "median"),
            probability_ranked_first=("rank", lambda x: (x == 1).mean() * 100),
            probability_top_two=("rank", lambda x: (x <= 2).mean() * 100),
            probability_bottom_two=("rank", lambda x: (x >= len(pathways) - 1).mean() * 100),
        )
        .reset_index()
        .sort_values("probability_ranked_first", ascending=False)
    )

    return simulation, robustness


def expand_training(pathways: pd.DataFrame, n: int = 2600) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []

    for _ in range(n):
        base = pathways.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]
        record = {}

        for feature in FEATURES:
            record[feature] = float(np.clip(float(base[feature]) + rng.normal(0, 0.7), 1, 10))

        readiness = (
            0.18 * record["adaptive_support"]
            + 0.20 * record["transformability"]
            + 0.18 * record["governance_readiness"]
            + 0.16 * record["justice_contribution"]
            + 0.14 * record["ecological_viability"]
            + 0.08 * record["legitimacy"]
            + 0.06 * record["resource_feasibility"]
            - 0.10 * record["structural_risk"]
            + rng.normal(0, 0.20)
        )

        record["transformation_readiness"] = readiness
        record["high_readiness_manageable_risk"] = 1 if readiness >= 7.50 and record["structural_risk"] <= 4.4 else 0
        rows.append(record)

    return pd.DataFrame(rows)


def plot_outputs(profiles: pd.DataFrame, rankings: pd.DataFrame, robustness: pd.DataFrame, importance: pd.DataFrame | None = None) -> None:
    profile_plot = profiles[
        [
            "pathway",
            "transformation_readiness",
            "adaptive_support",
            "transformability",
            "governance_readiness",
            "justice_contribution",
            "ecological_viability",
            "structural_risk",
        ]
    ].melt(id_vars="pathway", var_name="criterion", value_name="value")

    order = profiles.sort_values("transformation_readiness")["pathway"].tolist()

    plt.figure(figsize=(11, 7))
    for criterion, subset in profile_plot.groupby("criterion"):
        y = [order.index(p) for p in subset["pathway"]]
        plt.scatter(subset["value"], y, label=criterion, s=50)
    plt.yticks(range(len(order)), order)
    plt.xlabel("Criterion value")
    plt.title("Transformation Readiness and Pathway Criteria")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "transformation_pathway_profiles.png", dpi=160)
    plt.close()

    pivot = rankings.pivot(index="pathway", columns="scenario", values="transformation_value")
    plt.figure(figsize=(11, 7))
    for scenario in pivot.columns:
        plt.plot(pivot.index, pivot[scenario], marker="o", label=scenario)
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Transformation value")
    plt.title("Transformation Pathway Value Across Strategic Priorities")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "transformation_scenario_rankings.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(robustness["pathway"], robustness["probability_ranked_first"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Probability ranked first (%)")
    plt.title("Transformation Pathway Robustness Under Uncertainty")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "monte_carlo_probability_ranked_first.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(robustness["pathway"], robustness["probability_top_two"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Probability ranked in top two (%)")
    plt.title("Transformation Pathway Top-Two Robustness")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "monte_carlo_probability_top_two.png", dpi=160)
    plt.close()

    if importance is not None:
        plt.figure(figsize=(10, 6))
        plt.barh(importance["feature"], importance["importance"])
        plt.gca().invert_yaxis()
        plt.xlabel("Importance")
        plt.title("Feature Importance for Transformation Readiness Classification")
        plt.tight_layout()
        plt.savefig(OUT_FIGURES / "advanced_feature_importance.png", dpi=160)
        plt.close()


def main() -> None:
    pathways = pd.read_csv(PATHWAYS_PATH)
    scenarios = pd.read_csv(SCENARIOS_PATH)

    profiles = calculate_readiness(pathways)
    rankings = scenario_rankings(pathways, scenarios)
    baseline = scenarios.loc[scenarios["scenario"] == "Balanced"].iloc[0]
    simulation, robustness = monte_carlo(pathways, baseline, n=5000)

    profiles.to_csv(OUT_TABLES / "transformation_pathway_profiles_advanced.csv", index=False)
    rankings.to_csv(OUT_TABLES / "transformation_pathway_rankings_advanced.csv", index=False)
    simulation.to_csv(OUT_TABLES / "transformation_monte_carlo_advanced.csv", index=False)
    robustness.to_csv(OUT_TABLES / "transformation_robustness_summary_advanced.csv", index=False)

    training = expand_training(pathways)
    X = training[FEATURES]
    y = training["high_readiness_manageable_risk"]

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
            "model": "random_forest_transformation_readiness_classifier",
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

    training.to_csv(OUT_TABLES / "synthetic_transformation_readiness_training_data.csv", index=False)
    metrics.to_csv(OUT_TABLES / "advanced_transformation_readiness_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "transformation_readiness_classifier.joblib")

    plot_outputs(profiles, rankings, robustness, importance)

    print("Advanced transformation workflow complete.")
    print(profiles[["pathway", "transformation_readiness", "diagnostic"]].round(4))
    print(metrics.round(4))


if __name__ == "__main__":
    main()
