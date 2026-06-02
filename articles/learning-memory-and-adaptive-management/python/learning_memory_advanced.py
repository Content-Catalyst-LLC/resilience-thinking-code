#!/usr/bin/env python3
"""
Advanced learning, memory, and adaptive management workflow.

Uses pandas, numpy, matplotlib, scikit-learn, and joblib.

Run:
    pip install -r requirements-advanced.txt
    python python/learning_memory_advanced.py
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
STRATEGIES_PATH = ROOT / "data" / "raw" / "adaptive_management_strategies.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "adaptive_management_scenarios.csv"
PROFILES_PATH = ROOT / "data" / "raw" / "adaptive_management_profiles.csv"
EVENTS_PATH = ROOT / "data" / "raw" / "learning_memory_events.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_FIGURES = ROOT / "outputs" / "figures"
OUT_MODELS = ROOT / "outputs" / "models"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)
OUT_MODELS.mkdir(parents=True, exist_ok=True)

BENEFIT_CRITERIA = [
    "monitoring_quality",
    "memory_retention",
    "feedback_use",
    "governance_flexibility",
    "community_knowledge",
    "justice_protection",
    "implementation_reliability",
]

FEATURES = BENEFIT_CRITERIA + ["forgetting_pressure"]


def calculate_strategy_profiles(strategies: pd.DataFrame) -> pd.DataFrame:
    out = strategies.copy()
    out["base_adaptive_learning_value"] = (
        0.15 * out["monitoring_quality"]
        + 0.15 * out["memory_retention"]
        + 0.17 * out["feedback_use"]
        + 0.14 * out["governance_flexibility"]
        + 0.12 * out["community_knowledge"]
        + 0.11 * out["justice_protection"]
        + 0.09 * out["implementation_reliability"]
        - 0.07 * out["forgetting_pressure"]
    )

    conditions = [
        (out["base_adaptive_learning_value"] >= 7.2) & (out["forgetting_pressure"] <= 3.1),
        out["forgetting_pressure"] >= 3.5,
        out["feedback_use"] < 8.0,
        out["justice_protection"] < 7.5,
    ]
    choices = [
        "strong adaptive-learning profile with manageable forgetting pressure",
        "forgetting-pressure review needed",
        "feedback-use constraint",
        "justice protection needs strengthening",
    ]
    out["diagnostic"] = np.select(conditions, choices, default="promising but requires implementation and governance validation")
    return out


def event_diagnostics(events: pd.DataFrame) -> pd.DataFrame:
    out = events.copy()
    out["lesson_score"] = (
        0.20 * out["monitoring_signal"]
        + 0.22 * out["lesson_capture"]
        + 0.20 * out["implementation_followthrough"]
        + 0.18 * out["community_input"]
        + 0.14 * out["justice_visibility"]
        - 0.06 * out["memory_loss_risk"]
    )
    out["justice_weighted_learning"] = out["lesson_score"] * (0.70 + 0.30 * out["justice_visibility"])

    conditions = [
        out["implementation_followthrough"] < 0.58,
        out["community_input"] < 0.55,
        out["memory_loss_risk"] > 0.44,
    ]
    choices = [
        "lesson capture may not become institutional change",
        "community knowledge integration is weak",
        "memory-loss risk threatens learning continuity",
    ]
    out["diagnostic"] = np.select(conditions, choices, default="moderate to strong learning signal")
    return out


def simulate_profile(row: pd.Series, seed: int = 42, time_steps: int = 80) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    function_level = 0.88
    memory = row["memory_retention"]
    adaptive_capacity = 0.55

    disturbance = np.full(time_steps, 0.04)
    disturbance[[15, 32, 50, 67]] = [0.35, 0.22, 0.40, 0.28]

    rows = []

    for t in range(time_steps):
        shock = disturbance[t]

        monitoring_signal = np.clip(
            row["monitoring_quality"] * shock + rng.normal(0, 0.015),
            0,
            1,
        )

        learning = (
            row["learning_rate"]
            * monitoring_signal
            * row["feedback_use"]
            * row["governance_capacity"]
        )

        memory = (
            row["memory_retention"] * memory
            + learning
            - 0.05 * row["forgetting_pressure"]
        )
        memory = np.clip(memory, 0, 1)

        adaptive_capacity = (
            0.82 * adaptive_capacity
            + 0.12 * memory
            + 0.10 * row["governance_capacity"]
            - 0.06 * row["forgetting_pressure"]
        )
        adaptive_capacity = np.clip(adaptive_capacity, 0, 1)

        function_level = (
            function_level
            - 0.42 * shock
            + 0.24 * adaptive_capacity
            + 0.10 * memory
            - 0.05 * row["forgetting_pressure"]
        )
        function_level = np.clip(function_level, 0, 1)

        justice_adjusted_function = function_level * (0.75 + 0.25 * row["justice_sensitivity"])

        rows.append(
            {
                "profile_id": row["profile_id"],
                "profile": row["profile"],
                "time": t,
                "disturbance": shock,
                "monitoring_signal": monitoring_signal,
                "learning": learning,
                "memory": memory,
                "adaptive_capacity": adaptive_capacity,
                "function_level": function_level,
                "justice_adjusted_function": justice_adjusted_function,
            }
        )

    return pd.DataFrame(rows)


def run_dynamic_simulations(profiles: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    simulation = pd.concat(
        [simulate_profile(row, seed=42 + i) for i, row in profiles.iterrows()],
        ignore_index=True,
    )

    summary = (
        simulation.groupby("profile")
        .agg(
            mean_function=("function_level", "mean"),
            min_function=("function_level", "min"),
            final_function=("function_level", "last"),
            mean_memory=("memory", "mean"),
            final_memory=("memory", "last"),
            mean_adaptive_capacity=("adaptive_capacity", "mean"),
            mean_justice_adjusted_function=("justice_adjusted_function", "mean"),
        )
        .reset_index()
        .sort_values("mean_justice_adjusted_function", ascending=False)
    )

    return simulation, summary


def score_strategies(strategies: pd.DataFrame, scenario: pd.Series) -> pd.DataFrame:
    result = strategies.copy()
    result["adaptive_learning_value"] = (
        scenario["monitoring_quality_weight"] * result["monitoring_quality"]
        + scenario["memory_retention_weight"] * result["memory_retention"]
        + scenario["feedback_use_weight"] * result["feedback_use"]
        + scenario["governance_flexibility_weight"] * result["governance_flexibility"]
        + scenario["community_knowledge_weight"] * result["community_knowledge"]
        + scenario["justice_protection_weight"] * result["justice_protection"]
        + scenario["implementation_reliability_weight"] * result["implementation_reliability"]
        - scenario["forgetting_pressure_weight"] * result["forgetting_pressure"]
    )
    result = result.sort_values("adaptive_learning_value", ascending=False).reset_index(drop=True)
    result["rank"] = np.arange(1, len(result) + 1)
    result["scenario"] = scenario["scenario"]
    return result


def scenario_rankings(strategies: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, scenario in scenarios.iterrows():
        rows.append(score_strategies(strategies, scenario))
    return pd.concat(rows, ignore_index=True)


def strategy_monte_carlo(strategies: pd.DataFrame, scenario: pd.Series, n: int = 5000) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(42)
    rows = []

    for simulation_id in range(n):
        sampled = strategies.copy()
        for criterion in FEATURES:
            sampled[criterion] = rng.normal(loc=strategies[criterion], scale=0.6).clip(1, 10)

        scored = score_strategies(sampled, scenario)

        for _, row in scored.iterrows():
            rows.append(
                {
                    "simulation_id": simulation_id,
                    "strategy_id": row["strategy_id"],
                    "strategy": row["strategy"],
                    "rank": int(row["rank"]),
                    "adaptive_learning_value": row["adaptive_learning_value"],
                    "winner": scored.iloc[0]["strategy"],
                }
            )

    simulation = pd.DataFrame(rows)

    robustness = (
        simulation.groupby(["strategy_id", "strategy"])
        .agg(
            mean_adaptive_learning_value=("adaptive_learning_value", "mean"),
            median_adaptive_learning_value=("adaptive_learning_value", "median"),
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
            0.15 * record["monitoring_quality"]
            + 0.15 * record["memory_retention"]
            + 0.17 * record["feedback_use"]
            + 0.14 * record["governance_flexibility"]
            + 0.12 * record["community_knowledge"]
            + 0.11 * record["justice_protection"]
            + 0.09 * record["implementation_reliability"]
            - 0.07 * record["forgetting_pressure"]
            + rng.normal(0, 0.18)
        )

        record["adaptive_learning_value"] = value
        record["high_adaptive_learning_low_forgetting"] = 1 if value >= 7.15 and record["forgetting_pressure"] <= 3.4 else 0
        rows.append(record)

    return pd.DataFrame(rows)


def plot_outputs(
    strategy_profiles: pd.DataFrame,
    dynamic_simulation: pd.DataFrame,
    dynamic_summary: pd.DataFrame,
    rankings: pd.DataFrame,
    robustness: pd.DataFrame,
    importance: pd.DataFrame | None = None,
) -> None:
    profile_plot = strategy_profiles[
        [
            "strategy",
            "base_adaptive_learning_value",
            "monitoring_quality",
            "memory_retention",
            "feedback_use",
            "governance_flexibility",
            "community_knowledge",
            "justice_protection",
            "implementation_reliability",
            "forgetting_pressure",
        ]
    ].melt(id_vars="strategy", var_name="criterion", value_name="value")

    order = strategy_profiles.sort_values("base_adaptive_learning_value")["strategy"].tolist()

    plt.figure(figsize=(11, 7))
    for criterion, subset in profile_plot.groupby("criterion"):
        y = [order.index(p) for p in subset["strategy"]]
        plt.scatter(subset["value"], y, label=criterion, s=50)
    plt.yticks(range(len(order)), order)
    plt.xlabel("Criterion value")
    plt.title("Adaptive Management Strategy Profiles")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "adaptive_management_strategy_profiles.png", dpi=160)
    plt.close()

    pivot = rankings.pivot(index="strategy", columns="scenario", values="adaptive_learning_value")
    plt.figure(figsize=(11, 7))
    for scenario in pivot.columns:
        plt.plot(pivot.index, pivot[scenario], marker="o", label=scenario)
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Adaptive learning value")
    plt.title("Adaptive Management Strategy Value Across Priorities")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "adaptive_management_scenario_rankings.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    for profile, subset in dynamic_simulation.groupby("profile"):
        plt.plot(subset["time"], subset["function_level"], label=profile)
    plt.xlabel("Time")
    plt.ylabel("System function")
    plt.title("System Function Under Repeated Disturbance")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "system_function_under_disturbance.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    for profile, subset in dynamic_simulation.groupby("profile"):
        plt.plot(subset["time"], subset["memory"], label=profile)
    plt.xlabel("Time")
    plt.ylabel("System memory")
    plt.title("Memory Retention and Learning Under Disturbance")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "memory_retention_under_disturbance.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(dynamic_summary["profile"], dynamic_summary["mean_justice_adjusted_function"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Mean justice-adjusted function")
    plt.title("Justice-Adjusted Adaptive Response by Profile")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "justice_adjusted_adaptive_response.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(robustness["strategy"], robustness["probability_ranked_first"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Probability ranked first (%)")
    plt.title("Robustness of Adaptive Management Strategies")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "monte_carlo_probability_ranked_first.png", dpi=160)
    plt.close()

    if importance is not None:
        plt.figure(figsize=(10, 6))
        plt.barh(importance["feature"], importance["importance"])
        plt.gca().invert_yaxis()
        plt.xlabel("Importance")
        plt.title("Feature Importance for Adaptive-Learning Classification")
        plt.tight_layout()
        plt.savefig(OUT_FIGURES / "advanced_feature_importance.png", dpi=160)
        plt.close()


def main() -> None:
    strategies = pd.read_csv(STRATEGIES_PATH)
    scenarios = pd.read_csv(SCENARIOS_PATH)
    profiles = pd.read_csv(PROFILES_PATH)
    events = pd.read_csv(EVENTS_PATH)

    strategy_profiles = calculate_strategy_profiles(strategies)
    event_df = event_diagnostics(events)
    dynamic_simulation, dynamic_summary = run_dynamic_simulations(profiles)
    rankings = scenario_rankings(strategies, scenarios)
    baseline = scenarios.loc[scenarios["scenario"] == "Balanced"].iloc[0]
    strategy_simulation, robustness = strategy_monte_carlo(strategies, baseline, n=5000)

    strategy_profiles.to_csv(OUT_TABLES / "adaptive_management_strategy_profiles_advanced.csv", index=False)
    event_df.to_csv(OUT_TABLES / "learning_memory_event_diagnostics_advanced.csv", index=False)
    dynamic_simulation.to_csv(OUT_TABLES / "learning_memory_dynamic_simulation_advanced.csv", index=False)
    dynamic_summary.to_csv(OUT_TABLES / "learning_memory_dynamic_summary_advanced.csv", index=False)
    rankings.to_csv(OUT_TABLES / "adaptive_management_strategy_rankings_advanced.csv", index=False)
    strategy_simulation.to_csv(OUT_TABLES / "adaptive_management_monte_carlo_advanced.csv", index=False)
    robustness.to_csv(OUT_TABLES / "adaptive_management_robustness_summary_advanced.csv", index=False)

    training = expand_training(strategies)
    X = training[FEATURES]
    y = training["high_adaptive_learning_low_forgetting"]

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
            "model": "random_forest_adaptive_learning_classifier",
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

    training.to_csv(OUT_TABLES / "synthetic_adaptive_learning_training_data.csv", index=False)
    metrics.to_csv(OUT_TABLES / "advanced_adaptive_learning_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "adaptive_learning_classifier.joblib")

    plot_outputs(strategy_profiles, dynamic_simulation, dynamic_summary, rankings, robustness, importance)

    print("Advanced learning, memory, and adaptive management workflow complete.")
    print("Dynamic profile summary:")
    print(dynamic_summary[["profile", "mean_function", "final_memory", "mean_justice_adjusted_function"]].round(4))
    print("Model metrics:")
    print(metrics.round(4))


if __name__ == "__main__":
    main()
