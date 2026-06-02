#!/usr/bin/env python3
"""
Advanced resilience indicators and dashboard-risk workflow.

Uses pandas, numpy, matplotlib, scikit-learn, and joblib.

Run:
    pip install -r requirements-advanced.txt
    python python/resilience_dashboard_advanced.py
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
DESIGNS_PATH = ROOT / "data" / "raw" / "dashboard_designs.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "dashboard_scenarios.csv"
SYSTEMS_PATH = ROOT / "data" / "raw" / "synthetic_resilience_dashboard_systems.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_FIGURES = ROOT / "outputs" / "figures"
OUT_MODELS = ROOT / "outputs" / "models"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)
OUT_MODELS.mkdir(parents=True, exist_ok=True)

DESIGN_FEATURES = [
    "indicator_coverage",
    "threshold_sensitivity",
    "justice_visibility",
    "uncertainty_transparency",
    "decision_trigger_clarity",
    "learning_integration",
    "dashboard_risk",
]

SYSTEM_FEATURES = [
    "exposure_reduction",
    "recovery_capacity",
    "adaptive_capacity",
    "buffer_capacity",
    "justice_visibility",
    "threshold_risk",
    "missingness",
]


def calculate_dashboard_profiles(designs: pd.DataFrame) -> pd.DataFrame:
    out = designs.copy()
    out["base_dashboard_value"] = (
        0.15 * out["indicator_coverage"]
        + 0.17 * out["threshold_sensitivity"]
        + 0.16 * out["justice_visibility"]
        + 0.14 * out["uncertainty_transparency"]
        + 0.16 * out["decision_trigger_clarity"]
        + 0.14 * out["learning_integration"]
        - 0.08 * out["dashboard_risk"]
    )

    conditions = [
        (out["base_dashboard_value"] >= 6.8) & (out["dashboard_risk"] <= 4.1),
        out["dashboard_risk"] >= 7.0,
        out["justice_visibility"] < 7.0,
        out["decision_trigger_clarity"] < 7.0,
    ]
    choices = [
        "strong responsible-dashboard profile",
        "high false-precision and dashboard-risk exposure",
        "justice visibility needs strengthening",
        "decision-trigger clarity constraint",
    ]
    out["diagnostic"] = np.select(conditions, choices, default="promising but requires governance and uncertainty validation")
    return out


def score_systems(systems: pd.DataFrame) -> pd.DataFrame:
    out = systems.copy()

    out["naive_score"] = (
        0.17 * out["exposure_reduction"]
        + 0.18 * out["recovery_capacity"]
        + 0.19 * out["adaptive_capacity"]
        + 0.16 * out["buffer_capacity"]
        + 0.16 * out["justice_visibility"]
    )
    out["threshold_adjusted_score"] = out["naive_score"] - 0.09 * out["threshold_risk"]
    out["uncertainty_adjusted_score"] = out["threshold_adjusted_score"] - 0.05 * out["missingness"]

    red_flags = []
    for _, row in out.iterrows():
        flags = []
        if row["threshold_risk"] >= 0.50:
            flags.append("threshold risk")
        if row["justice_visibility"] <= 0.52:
            flags.append("low justice visibility")
        if row["missingness"] >= 0.24:
            flags.append("high missingness")
        if row["buffer_capacity"] <= 0.55:
            flags.append("low buffer capacity")
        if row["adaptive_capacity"] <= 0.58:
            flags.append("low adaptive capacity")
        red_flags.append("; ".join(flags) if flags else "none")

    out["red_flags"] = red_flags
    out["red_flag_count"] = out["red_flags"].apply(lambda x: 0 if x == "none" else len(x.split("; ")))

    return out.sort_values("uncertainty_adjusted_score", ascending=False)


def score_designs(designs: pd.DataFrame, scenario: pd.Series) -> pd.DataFrame:
    result = designs.copy()
    result["dashboard_value"] = (
        scenario["indicator_coverage_weight"] * result["indicator_coverage"]
        + scenario["threshold_sensitivity_weight"] * result["threshold_sensitivity"]
        + scenario["justice_visibility_weight"] * result["justice_visibility"]
        + scenario["uncertainty_transparency_weight"] * result["uncertainty_transparency"]
        + scenario["decision_trigger_clarity_weight"] * result["decision_trigger_clarity"]
        + scenario["learning_integration_weight"] * result["learning_integration"]
        - scenario["dashboard_risk_weight"] * result["dashboard_risk"]
    )
    result = result.sort_values("dashboard_value", ascending=False).reset_index(drop=True)
    result["rank"] = np.arange(1, len(result) + 1)
    result["scenario"] = scenario["scenario"]
    return result


def scenario_rankings(designs: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    return pd.concat([score_designs(designs, scenario) for _, scenario in scenarios.iterrows()], ignore_index=True)


def design_monte_carlo(designs: pd.DataFrame, scenario: pd.Series, n: int = 5000) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(42)
    rows = []

    for simulation_id in range(n):
        sampled = designs.copy()
        for criterion in DESIGN_FEATURES:
            sampled[criterion] = rng.normal(loc=designs[criterion], scale=0.6).clip(1, 10)

        scored = score_designs(sampled, scenario)

        for _, row in scored.iterrows():
            rows.append(
                {
                    "simulation_id": simulation_id,
                    "dashboard_id": row["dashboard_id"],
                    "dashboard": row["dashboard"],
                    "rank": int(row["rank"]),
                    "dashboard_value": row["dashboard_value"],
                    "winner": scored.iloc[0]["dashboard"],
                }
            )

    simulation = pd.DataFrame(rows)
    robustness = (
        simulation.groupby(["dashboard_id", "dashboard"])
        .agg(
            mean_dashboard_value=("dashboard_value", "mean"),
            median_dashboard_value=("dashboard_value", "median"),
            probability_ranked_first=("rank", lambda x: (x == 1).mean() * 100),
            probability_top_two=("rank", lambda x: (x <= 2).mean() * 100),
            probability_bottom_two=("rank", lambda x: (x >= len(designs) - 1).mean() * 100),
        )
        .reset_index()
        .sort_values("probability_ranked_first", ascending=False)
    )
    return simulation, robustness


def system_monte_carlo(systems: pd.DataFrame, n: int = 5000) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(100)
    rows = []

    for simulation_id in range(n):
        sampled = systems.copy()
        for criterion in SYSTEM_FEATURES:
            sampled[criterion] = rng.normal(loc=systems[criterion], scale=0.06).clip(0, 1)

        scored = score_systems(sampled)

        for rank, (_, row) in enumerate(scored.iterrows(), start=1):
            rows.append(
                {
                    "simulation_id": simulation_id,
                    "system_id": row["system_id"],
                    "system": row["system"],
                    "rank": rank,
                    "naive_score": row["naive_score"],
                    "threshold_adjusted_score": row["threshold_adjusted_score"],
                    "uncertainty_adjusted_score": row["uncertainty_adjusted_score"],
                    "red_flag_count": row["red_flag_count"],
                    "red_flags": row["red_flags"],
                    "winner": scored.iloc[0]["system"],
                }
            )

    simulation = pd.DataFrame(rows)
    summary = (
        simulation.groupby(["system_id", "system"])
        .agg(
            mean_naive_score=("naive_score", "mean"),
            mean_threshold_adjusted_score=("threshold_adjusted_score", "mean"),
            mean_uncertainty_adjusted_score=("uncertainty_adjusted_score", "mean"),
            probability_ranked_first=("rank", lambda x: (x == 1).mean() * 100),
            probability_top_two=("rank", lambda x: (x <= 2).mean() * 100),
            probability_any_red_flag=("red_flag_count", lambda x: (x > 0).mean() * 100),
            mean_red_flag_count=("red_flag_count", "mean"),
        )
        .reset_index()
        .sort_values("mean_uncertainty_adjusted_score", ascending=False)
    )
    return simulation, summary


def expand_training(designs: pd.DataFrame, n: int = 2600) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []

    for _ in range(n):
        base = designs.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]
        record = {}

        for feature in DESIGN_FEATURES:
            record[feature] = float(np.clip(float(base[feature]) + rng.normal(0, 0.7), 1, 10))

        value = (
            0.15 * record["indicator_coverage"]
            + 0.17 * record["threshold_sensitivity"]
            + 0.16 * record["justice_visibility"]
            + 0.14 * record["uncertainty_transparency"]
            + 0.16 * record["decision_trigger_clarity"]
            + 0.14 * record["learning_integration"]
            - 0.08 * record["dashboard_risk"]
            + rng.normal(0, 0.18)
        )

        record["dashboard_value"] = value
        record["high_value_low_dashboard_risk"] = 1 if value >= 6.8 and record["dashboard_risk"] <= 4.5 else 0
        rows.append(record)

    return pd.DataFrame(rows)


def plot_outputs(
    profiles: pd.DataFrame,
    system_scores: pd.DataFrame,
    rankings: pd.DataFrame,
    design_robustness: pd.DataFrame,
    system_summary: pd.DataFrame,
    importance: pd.DataFrame | None = None,
) -> None:
    profile_plot = profiles[
        [
            "dashboard",
            "base_dashboard_value",
            "indicator_coverage",
            "threshold_sensitivity",
            "justice_visibility",
            "uncertainty_transparency",
            "decision_trigger_clarity",
            "learning_integration",
            "dashboard_risk",
        ]
    ].melt(id_vars="dashboard", var_name="criterion", value_name="value")

    order = profiles.sort_values("base_dashboard_value")["dashboard"].tolist()

    plt.figure(figsize=(11, 7))
    for criterion, subset in profile_plot.groupby("criterion"):
        y = [order.index(p) for p in subset["dashboard"]]
        plt.scatter(subset["value"], y, label=criterion, s=50)
    plt.yticks(range(len(order)), order)
    plt.xlabel("Criterion value")
    plt.title("Resilience Dashboard Design Profiles")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "dashboard_design_profiles.png", dpi=160)
    plt.close()

    pivot = rankings.pivot(index="dashboard", columns="scenario", values="dashboard_value")
    plt.figure(figsize=(11, 7))
    for scenario in pivot.columns:
        plt.plot(pivot.index, pivot[scenario], marker="o", label=scenario)
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Dashboard value")
    plt.title("Dashboard Design Value Across Priorities")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "dashboard_design_scenario_rankings.png", dpi=160)
    plt.close()

    x = np.arange(len(system_scores))
    width = 0.28
    plt.figure(figsize=(11, 7))
    plt.bar(x - width, system_scores["naive_score"], width, label="Naive")
    plt.bar(x, system_scores["threshold_adjusted_score"], width, label="Threshold-adjusted")
    plt.bar(x + width, system_scores["uncertainty_adjusted_score"], width, label="Uncertainty-adjusted")
    plt.xticks(x, system_scores["system"], rotation=25, ha="right")
    plt.ylabel("Dashboard score")
    plt.title("Dashboard Scores Before and After Risk Adjustment")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "dashboard_score_adjustments.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(system_summary["system"], system_summary["probability_any_red_flag"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Probability of any red flag (%)")
    plt.title("Red-Flag Rate Under Simulated Uncertainty")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "system_red_flag_rates.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(design_robustness["dashboard"], design_robustness["probability_ranked_first"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Probability ranked first (%)")
    plt.title("Robustness of Dashboard Designs Under Uncertainty")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "dashboard_design_probability_ranked_first.png", dpi=160)
    plt.close()

    if importance is not None:
        plt.figure(figsize=(10, 6))
        plt.barh(importance["feature"], importance["importance"])
        plt.gca().invert_yaxis()
        plt.xlabel("Importance")
        plt.title("Feature Importance for Responsible Dashboard Classification")
        plt.tight_layout()
        plt.savefig(OUT_FIGURES / "advanced_feature_importance.png", dpi=160)
        plt.close()


def main() -> None:
    designs = pd.read_csv(DESIGNS_PATH)
    scenarios = pd.read_csv(SCENARIOS_PATH)
    systems = pd.read_csv(SYSTEMS_PATH)

    profiles = calculate_dashboard_profiles(designs)
    system_scores = score_systems(systems)
    rankings = scenario_rankings(designs, scenarios)

    baseline = scenarios.loc[scenarios["scenario"] == "Balanced"].iloc[0]
    design_simulation, design_robustness = design_monte_carlo(designs, baseline, n=5000)
    system_simulation, system_summary = system_monte_carlo(systems, n=5000)

    profiles.to_csv(OUT_TABLES / "dashboard_design_profiles_advanced.csv", index=False)
    system_scores.to_csv(OUT_TABLES / "resilience_dashboard_system_scores_advanced.csv", index=False)
    rankings.to_csv(OUT_TABLES / "dashboard_design_rankings_advanced.csv", index=False)
    design_simulation.to_csv(OUT_TABLES / "dashboard_design_monte_carlo_advanced.csv", index=False)
    design_robustness.to_csv(OUT_TABLES / "dashboard_design_robustness_summary_advanced.csv", index=False)
    system_simulation.to_csv(OUT_TABLES / "resilience_dashboard_system_monte_carlo_advanced.csv", index=False)
    system_summary.to_csv(OUT_TABLES / "resilience_dashboard_system_uncertainty_summary_advanced.csv", index=False)

    training = expand_training(designs)
    X = training[DESIGN_FEATURES]
    y = training["high_value_low_dashboard_risk"]

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
            "model": "random_forest_responsible_dashboard_classifier",
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
            "feature": DESIGN_FEATURES,
            "importance": model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)

    training.to_csv(OUT_TABLES / "synthetic_dashboard_design_training_data.csv", index=False)
    metrics.to_csv(OUT_TABLES / "advanced_dashboard_design_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "responsible_dashboard_classifier.joblib")

    plot_outputs(profiles, system_scores, rankings, design_robustness, system_summary, importance)

    print("Advanced resilience dashboard workflow complete.")
    print("System dashboard scores:")
    print(system_scores[["system", "naive_score", "threshold_adjusted_score", "uncertainty_adjusted_score", "red_flags"]].round(4))
    print("Model metrics:")
    print(metrics.round(4))


if __name__ == "__main__":
    main()
