#!/usr/bin/env python3
# Advanced Financial System Resilience workflow.
# Run: pip install -r requirements-advanced.txt && python python/financial_system_resilience_advanced.py

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
    "capital_strength",
    "liquidity_resilience",
    "infrastructure_robustness",
    "governance_capacity",
    "inclusive_resilience",
    "systemic_exposure",
    "implementation_burden",
]

def calculate_strategy_profiles(strategies: pd.DataFrame) -> pd.DataFrame:
    out = strategies.copy()
    out["financial_resilience_value"] = (
        0.16 * out["capital_strength"]
        + 0.16 * out["liquidity_resilience"]
        + 0.16 * out["infrastructure_robustness"]
        + 0.16 * out["governance_capacity"]
        + 0.16 * out["inclusive_resilience"]
        - 0.12 * out["systemic_exposure"]
        - 0.08 * out["implementation_burden"]
    )
    out["inclusion_gap"] = (8.0 - out["inclusive_resilience"]).clip(lower=0)
    out["infrastructure_gap"] = (8.0 - out["infrastructure_robustness"]).clip(lower=0)
    out["liquidity_gap"] = (8.0 - out["liquidity_resilience"]).clip(lower=0)
    out["adjusted_financial_resilience_value"] = (
        out["financial_resilience_value"]
        - 0.07 * out["inclusion_gap"]
        - 0.06 * out["infrastructure_gap"]
        - 0.05 * out["liquidity_gap"]
    )
    out["inclusion_adjusted_value"] = out["financial_resilience_value"] * (0.72 + 0.028 * out["inclusive_resilience"])
    conditions = [
        out["implementation_burden"] >= 3.7,
        out["inclusive_resilience"] < 7.5,
        out["infrastructure_robustness"] < 7.6,
        out["systemic_exposure"] >= 4.4,
        out["liquidity_resilience"] < 7.5,
        out["financial_resilience_value"] >= 4.80,
    ]
    choices = [
        "implementation-burden review needed",
        "financial-inclusion review needed",
        "infrastructure-resilience review needed",
        "systemic-exposure review needed",
        "liquidity-resilience review needed",
        "strong financial resilience strategy candidate",
    ]
    out["diagnostic"] = np.select(conditions, choices, default="promising but requires stress testing")
    return out

def score_strategies(strategies: pd.DataFrame, scenario: pd.Series) -> pd.DataFrame:
    result = strategies.copy()
    result["financial_resilience_value"] = (
        scenario["capital_strength_weight"] * result["capital_strength"]
        + scenario["liquidity_resilience_weight"] * result["liquidity_resilience"]
        + scenario["infrastructure_robustness_weight"] * result["infrastructure_robustness"]
        + scenario["governance_capacity_weight"] * result["governance_capacity"]
        + scenario["inclusive_resilience_weight"] * result["inclusive_resilience"]
        - scenario["systemic_exposure_weight"] * result["systemic_exposure"]
        - scenario["implementation_burden_weight"] * result["implementation_burden"]
    )
    result = result.sort_values("financial_resilience_value", ascending=False).reset_index(drop=True)
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
                "financial_resilience_value": row["financial_resilience_value"],
                "winner": scored.iloc[0]["strategy"],
            })
    simulation = pd.DataFrame(rows)
    robustness = (
        simulation.groupby(["strategy_id", "strategy"])
        .agg(
            mean_financial_resilience_value=("financial_resilience_value", "mean"),
            median_financial_resilience_value=("financial_resilience_value", "median"),
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
            0.16 * record["capital_strength"]
            + 0.16 * record["liquidity_resilience"]
            + 0.16 * record["infrastructure_robustness"]
            + 0.16 * record["governance_capacity"]
            + 0.16 * record["inclusive_resilience"]
            - 0.12 * record["systemic_exposure"]
            - 0.08 * record["implementation_burden"]
            + rng.normal(0, 0.18)
        )
        review_gap = (
            max(0, 8.0 - record["inclusive_resilience"])
            + max(0, 8.0 - record["liquidity_resilience"])
            + max(0, 8.0 - record["infrastructure_robustness"])
            + max(0, record["systemic_exposure"] - 4.1)
        )
        record["financial_resilience_value"] = value
        record["review_gap"] = review_gap
        record["high_value_feasible"] = 1 if value >= 4.65 and record["implementation_burden"] <= 3.5 and review_gap <= 1.1 else 0
        rows.append(record)
    return pd.DataFrame(rows)

def main() -> None:
    strategies = pd.read_csv(ROOT / "data/raw/financial_resilience_strategies.csv")
    scenarios = pd.read_csv(ROOT / "data/raw/financial_resilience_scenarios.csv")
    profiles = calculate_strategy_profiles(strategies)
    rankings = scenario_rankings(strategies, scenarios)
    baseline = scenarios.loc[scenarios["scenario"] == "Balanced"].iloc[0]
    simulation, robustness = strategy_monte_carlo(strategies, baseline)

    profiles.to_csv(OUT_TABLES / "financial_resilience_strategy_profiles_advanced.csv", index=False)
    rankings.to_csv(OUT_TABLES / "financial_resilience_strategy_rankings_advanced.csv", index=False)
    simulation.to_csv(OUT_TABLES / "financial_resilience_monte_carlo_advanced.csv", index=False)
    robustness.to_csv(OUT_TABLES / "financial_resilience_robustness_summary_advanced.csv", index=False)

    training = expand_training(strategies)
    X = training[FEATURES + ["review_gap"]]
    y = training["high_value_feasible"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=450, min_samples_leaf=6, class_weight="balanced", random_state=42)
    model.fit(X_train, y_train)
    prob = model.predict_proba(X_test)[:, 1]
    pred = (prob >= 0.50).astype(int)

    metrics = pd.DataFrame([{
        "model": "random_forest_financial_system_resilience_classifier",
        "accuracy": accuracy_score(y_test, pred),
        "precision": precision_score(y_test, pred, zero_division=0),
        "recall": recall_score(y_test, pred, zero_division=0),
        "f1": f1_score(y_test, pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, prob),
        "brier_score": brier_score_loss(y_test, prob),
    }])
    importance = pd.DataFrame({"feature": FEATURES + ["review_gap"], "importance": model.feature_importances_}).sort_values("importance", ascending=False)

    metrics.to_csv(OUT_TABLES / "advanced_financial_resilience_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "financial_system_resilience_classifier.joblib")

    plt.figure(figsize=(10, 6))
    plt.bar(robustness["strategy"], robustness["probability_ranked_first"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Probability ranked first (%)")
    plt.title("Robustness of Financial System Resilience Strategies")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "monte_carlo_probability_ranked_first.png", dpi=160)
    plt.close()

    print("Advanced financial system resilience workflow complete.")
    print(profiles[["strategy", "financial_resilience_value", "adjusted_financial_resilience_value", "diagnostic"]].round(4))
    print(metrics.round(4))

if __name__ == "__main__":
    main()
