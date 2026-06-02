#!/usr/bin/env python3
# Advanced AI and Resilience Thinking workflow.
# Run: pip install -r requirements-advanced.txt && python python/ai_resilience_thinking_advanced.py

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
OUT_TABLES = ROOT / "outputs/tables"
OUT_FIGURES = ROOT / "outputs/figures"
OUT_MODELS = ROOT / "outputs/models"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)
OUT_MODELS.mkdir(parents=True, exist_ok=True)

FEATURES = [
    "monitoring_value",
    "forecasting_value",
    "scenario_value",
    "decision_support",
    "governance_quality",
    "equity_safeguards",
    "human_oversight",
    "local_knowledge",
    "security_resilience",
    "ai_risk",
    "implementation_burden",
]

def calculate_strategy_profiles(strategies: pd.DataFrame) -> pd.DataFrame:
    out = strategies.copy()
    out["ai_resilience_value"] = (
        0.11 * out["monitoring_value"]
        + 0.10 * out["forecasting_value"]
        + 0.11 * out["scenario_value"]
        + 0.11 * out["decision_support"]
        + 0.12 * out["governance_quality"]
        + 0.12 * out["equity_safeguards"]
        + 0.12 * out["human_oversight"]
        + 0.10 * out["local_knowledge"]
        + 0.10 * out["security_resilience"]
        - 0.05 * out["ai_risk"]
        - 0.04 * out["implementation_burden"]
    )
    out["governance_gap"] = (8.5 - out["governance_quality"]).clip(lower=0)
    out["equity_gap"] = (8.5 - out["equity_safeguards"]).clip(lower=0)
    out["human_gap"] = (8.5 - out["human_oversight"]).clip(lower=0)
    out["local_gap"] = (8.2 - out["local_knowledge"]).clip(lower=0)
    out["security_gap"] = (8.3 - out["security_resilience"]).clip(lower=0)
    out["adjusted_ai_resilience_value"] = (
        out["ai_resilience_value"]
        - 0.07 * out["governance_gap"]
        - 0.08 * out["equity_gap"]
        - 0.08 * out["human_gap"]
        - 0.06 * out["local_gap"]
        - 0.06 * out["security_gap"]
    )
    out["human_and_equity_adjusted_value"] = out["ai_resilience_value"] * (
        0.70 + 0.020 * out["human_oversight"] + 0.020 * out["equity_safeguards"] - 0.010 * out["ai_risk"]
    )
    conditions = [
        out["implementation_burden"] >= 3.8,
        out["ai_risk"] >= 3.2,
        out["equity_safeguards"] < 8.0,
        out["human_oversight"] < 8.1,
        out["local_knowledge"] < 8.0,
        out["governance_quality"] < 8.1,
        out["ai_resilience_value"] >= 7.55,
    ]
    choices = [
        "implementation-burden review needed",
        "AI-risk review needed",
        "equity-safeguards review needed",
        "human-oversight review needed",
        "local-knowledge review needed",
        "governance review needed",
        "strong AI-enabled resilience strategy candidate",
    ]
    out["diagnostic"] = np.select(conditions, choices, default="promising but requires participatory validation")
    return out

def score_strategies(strategies: pd.DataFrame, scenario: pd.Series) -> pd.DataFrame:
    result = strategies.copy()
    result["ai_resilience_value"] = (
        scenario["monitoring_value_weight"] * result["monitoring_value"]
        + scenario["forecasting_value_weight"] * result["forecasting_value"]
        + scenario["scenario_value_weight"] * result["scenario_value"]
        + scenario["decision_support_weight"] * result["decision_support"]
        + scenario["governance_quality_weight"] * result["governance_quality"]
        + scenario["equity_safeguards_weight"] * result["equity_safeguards"]
        + scenario["human_oversight_weight"] * result["human_oversight"]
        + scenario["local_knowledge_weight"] * result["local_knowledge"]
        + scenario["security_resilience_weight"] * result["security_resilience"]
        - scenario["ai_risk_weight"] * result["ai_risk"]
        - scenario["implementation_burden_weight"] * result["implementation_burden"]
    )
    result = result.sort_values("ai_resilience_value", ascending=False).reset_index(drop=True)
    result["rank"] = np.arange(1, len(result) + 1)
    result["scenario"] = scenario["scenario"]
    return result

def scenario_rankings(strategies: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    return pd.concat([score_strategies(strategies, scenario) for _, scenario in scenarios.iterrows()], ignore_index=True)

def strategy_monte_carlo(strategies: pd.DataFrame, scenario: pd.Series, n: int = 5000):
    rng = np.random.default_rng(42)
    rows = []
    for simulation_id in range(n):
        sampled = strategies.copy()
        for criterion in FEATURES:
            sampled[criterion] = rng.normal(loc=strategies[criterion], scale=0.55).clip(1, 10)
        scored = score_strategies(sampled, scenario)
        for _, row in scored.iterrows():
            rows.append({
                "simulation_id": simulation_id,
                "strategy_id": row["strategy_id"],
                "strategy": row["strategy"],
                "rank": int(row["rank"]),
                "ai_resilience_value": row["ai_resilience_value"],
                "winner": scored.iloc[0]["strategy"],
            })
    simulation = pd.DataFrame(rows)
    robustness = (
        simulation.groupby(["strategy_id", "strategy"])
        .agg(
            mean_ai_resilience_value=("ai_resilience_value", "mean"),
            median_ai_resilience_value=("ai_resilience_value", "median"),
            probability_ranked_first=("rank", lambda x: (x == 1).mean() * 100),
            probability_top_two=("rank", lambda x: (x <= 2).mean() * 100),
            probability_bottom_two=("rank", lambda x: (x >= len(strategies) - 1).mean() * 100),
        )
        .reset_index()
        .sort_values("probability_ranked_first", ascending=False)
    )
    return simulation, robustness

def expand_training(strategies: pd.DataFrame, n: int = 3400) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []
    for _ in range(n):
        base = strategies.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]
        record = {}
        for feature in FEATURES:
            record[feature] = float(np.clip(float(base[feature]) + rng.normal(0, 0.65), 1, 10))
        value = (
            0.11 * record["monitoring_value"]
            + 0.10 * record["forecasting_value"]
            + 0.11 * record["scenario_value"]
            + 0.11 * record["decision_support"]
            + 0.12 * record["governance_quality"]
            + 0.12 * record["equity_safeguards"]
            + 0.12 * record["human_oversight"]
            + 0.10 * record["local_knowledge"]
            + 0.10 * record["security_resilience"]
            - 0.05 * record["ai_risk"]
            - 0.04 * record["implementation_burden"]
            + rng.normal(0, 0.15)
        )
        review_gap = (
            max(0, 8.5 - record["governance_quality"])
            + max(0, 8.5 - record["equity_safeguards"])
            + max(0, 8.5 - record["human_oversight"])
            + max(0, 8.2 - record["local_knowledge"])
            + max(0, 8.3 - record["security_resilience"])
            + max(0, record["ai_risk"] - 3.2)
            + max(0, record["implementation_burden"] - 3.7)
        )
        record["ai_resilience_value"] = value
        record["review_gap"] = review_gap
        record["high_value_feasible"] = 1 if value >= 7.15 and record["ai_risk"] <= 3.2 and record["implementation_burden"] <= 3.7 and review_gap <= 1.6 else 0
        rows.append(record)
    return pd.DataFrame(rows)

def main() -> None:
    strategies = pd.read_csv(ROOT / "data/raw/ai_resilience_strategies.csv")
    scenarios = pd.read_csv(ROOT / "data/raw/ai_resilience_scenarios.csv")
    profiles = calculate_strategy_profiles(strategies)
    rankings = scenario_rankings(strategies, scenarios)
    baseline = scenarios.loc[scenarios["scenario"] == "Balanced"].iloc[0]
    simulation, robustness = strategy_monte_carlo(strategies, baseline)

    profiles.to_csv(OUT_TABLES / "ai_resilience_strategy_profiles_advanced.csv", index=False)
    rankings.to_csv(OUT_TABLES / "ai_resilience_strategy_rankings_advanced.csv", index=False)
    simulation.to_csv(OUT_TABLES / "ai_resilience_monte_carlo_advanced.csv", index=False)
    robustness.to_csv(OUT_TABLES / "ai_resilience_robustness_summary_advanced.csv", index=False)

    training = expand_training(strategies)
    X = training[FEATURES + ["review_gap"]]
    y = training["high_value_feasible"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=450, min_samples_leaf=6, class_weight="balanced", random_state=42)
    model.fit(X_train, y_train)
    prob = model.predict_proba(X_test)[:, 1]
    pred = (prob >= 0.50).astype(int)

    metrics = pd.DataFrame([{
        "model": "random_forest_ai_resilience_classifier",
        "accuracy": accuracy_score(y_test, pred),
        "precision": precision_score(y_test, pred, zero_division=0),
        "recall": recall_score(y_test, pred, zero_division=0),
        "f1": f1_score(y_test, pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, prob),
        "brier_score": brier_score_loss(y_test, prob),
    }])
    importance = pd.DataFrame({"feature": FEATURES + ["review_gap"], "importance": model.feature_importances_}).sort_values("importance", ascending=False)

    metrics.to_csv(OUT_TABLES / "advanced_ai_resilience_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "ai_resilience_classifier.joblib")

    plt.figure(figsize=(10, 6))
    plt.bar(robustness["strategy"], robustness["probability_ranked_first"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Probability ranked first (%)")
    plt.title("Robustness of AI Resilience Strategies")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "monte_carlo_probability_ranked_first.png", dpi=160)
    plt.close()

    print("Advanced AI resilience workflow complete.")
    print(profiles[["strategy", "ai_resilience_value", "adjusted_ai_resilience_value", "diagnostic"]].round(4))
    print(metrics.round(4))

if __name__ == "__main__":
    main()
