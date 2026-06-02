#!/usr/bin/env python3
# Advanced Local Knowledge and Resilience Practice workflow.
# Run: pip install -r requirements-advanced.txt && python python/local_knowledge_advanced.py

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
    "participation_access",
    "knowledge_diversity",
    "decision_influence",
    "trust_building",
    "knowledge_protection",
    "reciprocity",
    "implementation_accountability",
    "implementation_burden",
]

def calculate_strategy_profiles(strategies: pd.DataFrame) -> pd.DataFrame:
    out = strategies.copy()
    out["knowledge_integration_value"] = (
        0.14 * out["participation_access"]
        + 0.14 * out["knowledge_diversity"]
        + 0.15 * out["decision_influence"]
        + 0.14 * out["trust_building"]
        + 0.14 * out["knowledge_protection"]
        + 0.14 * out["reciprocity"]
        + 0.15 * out["implementation_accountability"]
        - 0.02 * out["implementation_burden"]
    )
    out["extraction_risk_gap"] = (out["decision_influence"] - out["implementation_accountability"]).clip(lower=0)
    out["protection_gap"] = (8.4 - out["knowledge_protection"]).clip(lower=0)
    out["participation_gap"] = (8.2 - out["participation_access"]).clip(lower=0)
    out["adjusted_knowledge_integration_value"] = (
        out["knowledge_integration_value"]
        - 0.08 * out["extraction_risk_gap"]
        - 0.08 * out["protection_gap"]
        - 0.06 * out["participation_gap"]
    )
    out["equity_adjusted_value"] = out["knowledge_integration_value"] * (0.72 + 0.028 * out["participation_access"])
    conditions = [
        out["implementation_burden"] >= 3.5,
        out["knowledge_protection"] < 8.2,
        out["decision_influence"] < 8.0,
        out["participation_access"] < 8.2,
        out["implementation_accountability"] < 8.2,
        out["knowledge_integration_value"] >= 8.30,
    ]
    choices = [
        "implementation-burden review needed",
        "knowledge-protection safeguards need strengthening",
        "decision-influence review needed",
        "participation-access review needed",
        "implementation-accountability review needed",
        "strong local-knowledge integration strategy candidate",
    ]
    out["diagnostic"] = np.select(conditions, choices, default="promising but requires community validation")
    return out

def score_strategies(strategies: pd.DataFrame, scenario: pd.Series) -> pd.DataFrame:
    result = strategies.copy()
    result["knowledge_integration_value"] = (
        scenario["participation_access_weight"] * result["participation_access"]
        + scenario["knowledge_diversity_weight"] * result["knowledge_diversity"]
        + scenario["decision_influence_weight"] * result["decision_influence"]
        + scenario["trust_building_weight"] * result["trust_building"]
        + scenario["knowledge_protection_weight"] * result["knowledge_protection"]
        + scenario["reciprocity_weight"] * result["reciprocity"]
        + scenario["implementation_accountability_weight"] * result["implementation_accountability"]
        - scenario["implementation_burden_weight"] * result["implementation_burden"]
    )
    result = result.sort_values("knowledge_integration_value", ascending=False).reset_index(drop=True)
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
            sampled[criterion] = rng.normal(loc=strategies[criterion], scale=0.6).clip(1, 10)
        scored = score_strategies(sampled, scenario)
        for _, row in scored.iterrows():
            rows.append({
                "simulation_id": simulation_id,
                "strategy_id": row["strategy_id"],
                "strategy": row["strategy"],
                "rank": int(row["rank"]),
                "knowledge_integration_value": row["knowledge_integration_value"],
                "winner": scored.iloc[0]["strategy"],
            })
    simulation = pd.DataFrame(rows)
    robustness = (
        simulation.groupby(["strategy_id", "strategy"])
        .agg(
            mean_knowledge_integration_value=("knowledge_integration_value", "mean"),
            median_knowledge_integration_value=("knowledge_integration_value", "median"),
            probability_ranked_first=("rank", lambda x: (x == 1).mean() * 100),
            probability_top_two=("rank", lambda x: (x <= 2).mean() * 100),
            probability_bottom_two=("rank", lambda x: (x >= len(strategies) - 1).mean() * 100),
        )
        .reset_index()
        .sort_values("probability_ranked_first", ascending=False)
    )
    return simulation, robustness

def expand_training(strategies: pd.DataFrame, n: int = 2800) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []
    for _ in range(n):
        base = strategies.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]
        record = {}
        for feature in FEATURES:
            record[feature] = float(np.clip(float(base[feature]) + rng.normal(0, 0.7), 1, 10))
        value = (
            0.14 * record["participation_access"]
            + 0.14 * record["knowledge_diversity"]
            + 0.15 * record["decision_influence"]
            + 0.14 * record["trust_building"]
            + 0.14 * record["knowledge_protection"]
            + 0.14 * record["reciprocity"]
            + 0.15 * record["implementation_accountability"]
            - 0.02 * record["implementation_burden"]
            + rng.normal(0, 0.18)
        )
        review_gap = (
            max(0, 8.2 - record["participation_access"])
            + max(0, 8.4 - record["knowledge_protection"])
            + max(0, record["decision_influence"] - record["implementation_accountability"])
        )
        record["knowledge_integration_value"] = value
        record["review_gap"] = review_gap
        record["high_value_feasible"] = 1 if value >= 8.10 and record["implementation_burden"] <= 3.4 and review_gap <= 0.8 else 0
        rows.append(record)
    return pd.DataFrame(rows)

def main() -> None:
    strategies = pd.read_csv(ROOT / "data/raw/local_knowledge_strategies.csv")
    scenarios = pd.read_csv(ROOT / "data/raw/local_knowledge_scenarios.csv")
    profiles = calculate_strategy_profiles(strategies)
    rankings = scenario_rankings(strategies, scenarios)
    baseline = scenarios.loc[scenarios["scenario"] == "Balanced"].iloc[0]
    simulation, robustness = strategy_monte_carlo(strategies, baseline)

    profiles.to_csv(OUT_TABLES / "local_knowledge_strategy_profiles_advanced.csv", index=False)
    rankings.to_csv(OUT_TABLES / "local_knowledge_strategy_rankings_advanced.csv", index=False)
    simulation.to_csv(OUT_TABLES / "local_knowledge_monte_carlo_advanced.csv", index=False)
    robustness.to_csv(OUT_TABLES / "local_knowledge_robustness_summary_advanced.csv", index=False)

    training = expand_training(strategies)
    X = training[FEATURES + ["review_gap"]]
    y = training["high_value_feasible"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=450, min_samples_leaf=6, class_weight="balanced", random_state=42)
    model.fit(X_train, y_train)
    prob = model.predict_proba(X_test)[:, 1]
    pred = (prob >= 0.50).astype(int)

    metrics = pd.DataFrame([{
        "model": "random_forest_local_knowledge_classifier",
        "accuracy": accuracy_score(y_test, pred),
        "precision": precision_score(y_test, pred, zero_division=0),
        "recall": recall_score(y_test, pred, zero_division=0),
        "f1": f1_score(y_test, pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, prob),
        "brier_score": brier_score_loss(y_test, prob),
    }])
    importance = pd.DataFrame({"feature": FEATURES + ["review_gap"], "importance": model.feature_importances_}).sort_values("importance", ascending=False)

    metrics.to_csv(OUT_TABLES / "advanced_local_knowledge_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "local_knowledge_classifier.joblib")

    plt.figure(figsize=(10, 6))
    plt.bar(robustness["strategy"], robustness["probability_ranked_first"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Probability ranked first (%)")
    plt.title("Robustness of Local-Knowledge Integration Strategies")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "monte_carlo_probability_ranked_first.png", dpi=160)
    plt.close()

    print("Advanced local knowledge workflow complete.")
    print(profiles[["strategy", "knowledge_integration_value", "adjusted_knowledge_integration_value", "diagnostic"]].round(4))
    print(metrics.round(4))

if __name__ == "__main__":
    main()
