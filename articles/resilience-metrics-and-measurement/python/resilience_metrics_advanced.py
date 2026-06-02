#!/usr/bin/env python3
"""
Advanced resilience metrics and measurement workflow.

Uses pandas, numpy, matplotlib, scikit-learn, and joblib.

Run:
    pip install -r requirements-advanced.txt
    python python/resilience_metrics_advanced.py
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
FRAMEWORKS_PATH = ROOT / "data" / "raw" / "resilience_measurement_frameworks.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "resilience_measurement_scenarios.csv"
EVENTS_PATH = ROOT / "data" / "raw" / "synthetic_system_events.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_FIGURES = ROOT / "outputs" / "figures"
OUT_MODELS = ROOT / "outputs" / "models"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)
OUT_MODELS.mkdir(parents=True, exist_ok=True)

BENEFIT_CRITERIA = [
    "resistance_coverage",
    "recovery_insight",
    "adaptive_capacity_visibility",
    "buffer_visibility",
    "justice_visibility",
    "data_quality_transparency",
]

FEATURES = BENEFIT_CRITERIA + ["threshold_blindness"]


def calculate_base_profiles(frameworks: pd.DataFrame) -> pd.DataFrame:
    out = frameworks.copy()
    out["base_metric_value"] = (
        0.16 * out["resistance_coverage"]
        + 0.16 * out["recovery_insight"]
        + 0.16 * out["adaptive_capacity_visibility"]
        + 0.15 * out["buffer_visibility"]
        + 0.13 * out["justice_visibility"]
        + 0.10 * out["data_quality_transparency"]
        - 0.14 * out["threshold_blindness"]
    )

    conditions = [
        (out["base_metric_value"] >= 5.95) & (out["threshold_blindness"] <= 3.4),
        out["threshold_blindness"] >= 4.8,
        out["justice_visibility"] < 7.2,
        out["data_quality_transparency"] < 7.3,
    ]
    choices = [
        "strong hybrid measurement profile with low threshold blindness",
        "threshold blindness review needed",
        "justice visibility needs strengthening",
        "data-quality transparency constraint",
    ]
    out["diagnostic"] = np.select(conditions, choices, default="promising but requires system-specific validation")
    return out


def event_metrics(events: pd.DataFrame) -> pd.DataFrame:
    out = events.copy()
    out["performance_loss"] = (out["baseline_function"] - out["min_function"]).clip(lower=0)
    out["resistance_score"] = (1 - out["performance_loss"] / out["shock_intensity"].clip(lower=0.01)).clip(0, 1)
    out["recovery_completeness"] = (
        (out["recovered_function"] - out["min_function"])
        / (out["baseline_function"] - out["min_function"]).clip(lower=0.01)
    ).clip(0, 1)
    out["recovery_speed"] = 1 / (1 + out["recovery_days"] / 30)
    out["justice_adjusted_recovery"] = (
        out["recovery_completeness"]
        * (0.70 + 0.30 * out["justice_visibility"])
        * (1 - 0.20 * out["affected_population_share"])
    ).clip(0, 1)

    conditions = [
        out["justice_adjusted_recovery"] < 0.55,
        out["resistance_score"] < 0.45,
        out["recovery_speed"] < 0.30,
    ]
    choices = [
        "recovery may hide distributional or long-duration vulnerability",
        "low resistance to disturbance",
        "slow recovery requires capacity review",
    ]
    out["diagnostic"] = np.select(conditions, choices, default="moderate to strong event-level resilience signal")
    return out


def score_frameworks(frameworks: pd.DataFrame, scenario: pd.Series) -> pd.DataFrame:
    result = frameworks.copy()
    result["metric_value"] = (
        scenario["resistance_coverage_weight"] * result["resistance_coverage"]
        + scenario["recovery_insight_weight"] * result["recovery_insight"]
        + scenario["adaptive_capacity_visibility_weight"] * result["adaptive_capacity_visibility"]
        + scenario["buffer_visibility_weight"] * result["buffer_visibility"]
        + scenario["justice_visibility_weight"] * result["justice_visibility"]
        + scenario["data_quality_transparency_weight"] * result["data_quality_transparency"]
        - scenario["threshold_blindness_weight"] * result["threshold_blindness"]
    )
    result = result.sort_values("metric_value", ascending=False).reset_index(drop=True)
    result["rank"] = np.arange(1, len(result) + 1)
    result["scenario"] = scenario["scenario"]
    return result


def scenario_rankings(frameworks: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, scenario in scenarios.iterrows():
        rows.append(score_frameworks(frameworks, scenario))
    return pd.concat(rows, ignore_index=True)


def monte_carlo(frameworks: pd.DataFrame, scenario: pd.Series, n: int = 5000) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(42)
    rows = []

    for simulation_id in range(n):
        sampled = frameworks.copy()
        for criterion in FEATURES:
            sampled[criterion] = rng.normal(loc=frameworks[criterion], scale=0.6)
            sampled[criterion] = sampled[criterion].clip(1, 10)

        scored = score_frameworks(sampled, scenario)

        for _, row in scored.iterrows():
            rows.append(
                {
                    "simulation_id": simulation_id,
                    "framework_id": row["framework_id"],
                    "framework": row["framework"],
                    "rank": int(row["rank"]),
                    "metric_value": row["metric_value"],
                    "winner": scored.iloc[0]["framework"],
                }
            )

    simulation = pd.DataFrame(rows)

    robustness = (
        simulation.groupby(["framework_id", "framework"])
        .agg(
            mean_metric_value=("metric_value", "mean"),
            median_metric_value=("metric_value", "median"),
            probability_ranked_first=("rank", lambda x: (x == 1).mean() * 100),
            probability_top_two=("rank", lambda x: (x <= 2).mean() * 100),
            probability_bottom_two=("rank", lambda x: (x >= len(frameworks) - 1).mean() * 100),
        )
        .reset_index()
        .sort_values("probability_ranked_first", ascending=False)
    )

    return simulation, robustness


def expand_training(frameworks: pd.DataFrame, n: int = 2600) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []

    for _ in range(n):
        base = frameworks.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]
        record = {}

        for feature in FEATURES:
            record[feature] = float(np.clip(float(base[feature]) + rng.normal(0, 0.7), 1, 10))

        value = (
            0.16 * record["resistance_coverage"]
            + 0.16 * record["recovery_insight"]
            + 0.16 * record["adaptive_capacity_visibility"]
            + 0.15 * record["buffer_visibility"]
            + 0.13 * record["justice_visibility"]
            + 0.10 * record["data_quality_transparency"]
            - 0.14 * record["threshold_blindness"]
            + rng.normal(0, 0.18)
        )

        record["metric_value"] = value
        record["high_value_low_threshold_blindness"] = 1 if value >= 5.9 and record["threshold_blindness"] <= 3.9 else 0
        rows.append(record)

    return pd.DataFrame(rows)


def plot_outputs(profiles: pd.DataFrame, event_df: pd.DataFrame, rankings: pd.DataFrame, robustness: pd.DataFrame, importance: pd.DataFrame | None = None) -> None:
    profile_plot = profiles[
        [
            "framework",
            "base_metric_value",
            "resistance_coverage",
            "recovery_insight",
            "adaptive_capacity_visibility",
            "buffer_visibility",
            "justice_visibility",
            "data_quality_transparency",
            "threshold_blindness",
        ]
    ].melt(id_vars="framework", var_name="criterion", value_name="value")

    order = profiles.sort_values("base_metric_value")["framework"].tolist()

    plt.figure(figsize=(11, 7))
    for criterion, subset in profile_plot.groupby("criterion"):
        y = [order.index(p) for p in subset["framework"]]
        plt.scatter(subset["value"], y, label=criterion, s=50)
    plt.yticks(range(len(order)), order)
    plt.xlabel("Criterion value")
    plt.title("Resilience Measurement Framework Profiles")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "resilience_measurement_framework_profiles.png", dpi=160)
    plt.close()

    pivot = rankings.pivot(index="framework", columns="scenario", values="metric_value")
    plt.figure(figsize=(11, 7))
    for scenario in pivot.columns:
        plt.plot(pivot.index, pivot[scenario], marker="o", label=scenario)
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Metric value")
    plt.title("Framework Value Across Measurement Priorities")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "resilience_measurement_scenario_rankings.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(robustness["framework"], robustness["probability_ranked_first"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Probability ranked first (%)")
    plt.title("Robustness of Resilience Measurement Choices")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "monte_carlo_probability_ranked_first.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(event_df["system_name"], event_df["justice_adjusted_recovery"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Justice-adjusted recovery")
    plt.title("Event-Level Justice-Adjusted Recovery")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "event_justice_adjusted_recovery.png", dpi=160)
    plt.close()

    if importance is not None:
        plt.figure(figsize=(10, 6))
        plt.barh(importance["feature"], importance["importance"])
        plt.gca().invert_yaxis()
        plt.xlabel("Importance")
        plt.title("Feature Importance for Measurement-Framework Classification")
        plt.tight_layout()
        plt.savefig(OUT_FIGURES / "advanced_feature_importance.png", dpi=160)
        plt.close()


def main() -> None:
    frameworks = pd.read_csv(FRAMEWORKS_PATH)
    scenarios = pd.read_csv(SCENARIOS_PATH)
    events = pd.read_csv(EVENTS_PATH)

    profiles = calculate_base_profiles(frameworks)
    event_df = event_metrics(events)
    rankings = scenario_rankings(frameworks, scenarios)
    baseline = scenarios.loc[scenarios["scenario"] == "Balanced"].iloc[0]
    simulation, robustness = monte_carlo(frameworks, baseline, n=5000)

    profiles.to_csv(OUT_TABLES / "resilience_metric_framework_profiles_advanced.csv", index=False)
    event_df.to_csv(OUT_TABLES / "resilience_event_performance_metrics_advanced.csv", index=False)
    rankings.to_csv(OUT_TABLES / "resilience_metric_framework_rankings_advanced.csv", index=False)
    simulation.to_csv(OUT_TABLES / "resilience_measurement_monte_carlo_advanced.csv", index=False)
    robustness.to_csv(OUT_TABLES / "resilience_measurement_robustness_summary_advanced.csv", index=False)

    training = expand_training(frameworks)
    X = training[FEATURES]
    y = training["high_value_low_threshold_blindness"]

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
            "model": "random_forest_measurement_framework_classifier",
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

    training.to_csv(OUT_TABLES / "synthetic_measurement_framework_training_data.csv", index=False)
    metrics.to_csv(OUT_TABLES / "advanced_measurement_framework_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "measurement_framework_classifier.joblib")

    plot_outputs(profiles, event_df, rankings, robustness, importance)

    print("Advanced resilience metrics workflow complete.")
    print(profiles[["framework", "base_metric_value", "diagnostic"]].round(4))
    print(metrics.round(4))


if __name__ == "__main__":
    main()
