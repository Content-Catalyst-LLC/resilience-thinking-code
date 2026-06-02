#!/usr/bin/env python3
# Advanced Intelligent Infrastructure and Resilience workflow.
# Run: pip install -r requirements-advanced.txt && python python/intelligent_infrastructure_resilience_advanced.py

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
    "predictive_maintenance",
    "cyber_physical_security",
    "digital_twin_capacity",
    "redundancy_and_fallback",
    "climate_adaptation",
    "governance_quality",
    "equity_performance",
    "ecological_integration",
    "fragility_risk",
    "implementation_burden",
]

def calculate_strategy_profiles(strategies: pd.DataFrame) -> pd.DataFrame:
    out = strategies.copy()
    out["infrastructure_resilience_value"] = (
        0.10 * out["monitoring_value"]
        + 0.11 * out["predictive_maintenance"]
        + 0.11 * out["cyber_physical_security"]
        + 0.10 * out["digital_twin_capacity"]
        + 0.11 * out["redundancy_and_fallback"]
        + 0.11 * out["climate_adaptation"]
        + 0.12 * out["governance_quality"]
        + 0.12 * out["equity_performance"]
        + 0.10 * out["ecological_integration"]
        - 0.04 * out["fragility_risk"]
        - 0.04 * out["implementation_burden"]
    )
    out["governance_gap"] = (8.5 - out["governance_quality"]).clip(lower=0)
    out["equity_gap"] = (8.5 - out["equity_performance"]).clip(lower=0)
    out["redundancy_gap"] = (8.5 - out["redundancy_and_fallback"]).clip(lower=0)
    out["maintenance_gap"] = (8.4 - out["predictive_maintenance"]).clip(lower=0)
    out["adjusted_infrastructure_resilience_value"] = (
        out["infrastructure_resilience_value"]
        - 0.07 * out["governance_gap"]
        - 0.08 * out["equity_gap"]
        - 0.07 * out["redundancy_gap"]
        - 0.06 * out["maintenance_gap"]
    )
    out["equity_and_governance_adjusted_value"] = out["infrastructure_resilience_value"] * (
        0.70 + 0.018 * out["equity_performance"] + 0.018 * out["governance_quality"] - 0.010 * out["fragility_risk"]
    )
    conditions = [
        out["implementation_burden"] >= 3.9,
        out["fragility_risk"] >= 3.1,
        out["equity_performance"] < 8.1,
        out["governance_quality"] < 8.3,
        out["cyber_physical_security"] < 8.1,
        out["predictive_maintenance"] < 8.1,
        out["infrastructure_resilience_value"] >= 7.65,
    ]
    choices = [
        "implementation-burden review needed",
        "hidden-fragility review needed",
        "equity-performance review needed",
        "governance review needed",
        "cyber-physical security review needed",
        "maintenance-capacity review needed",
        "strong intelligent infrastructure resilience strategy candidate",
    ]
    out["diagnostic"] = np.select(conditions, choices, default="promising but requires field validation")
    return out

def score_strategies(strategies: pd.DataFrame, scenario: pd.Series) -> pd.DataFrame:
    result = strategies.copy()
    result["infrastructure_resilience_value"] = (
        scenario["monitoring_value_weight"] * result["monitoring_value"]
        + scenario["predictive_maintenance_weight"] * result["predictive_maintenance"]
        + scenario["cyber_physical_security_weight"] * result["cyber_physical_security"]
        + scenario["digital_twin_capacity_weight"] * result["digital_twin_capacity"]
        + scenario["redundancy_and_fallback_weight"] * result["redundancy_and_fallback"]
        + scenario["climate_adaptation_weight"] * result["climate_adaptation"]
        + scenario["governance_quality_weight"] * result["governance_quality"]
        + scenario["equity_performance_weight"] * result["equity_performance"]
        + scenario["ecological_integration_weight"] * result["ecological_integration"]
        - scenario["fragility_risk_weight"] * result["fragility_risk"]
        - scenario["implementation_burden_weight"] * result["implementation_burden"]
    )
    result = result.sort_values("infrastructure_resilience_value", ascending=False).reset_index(drop=True)
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
                "infrastructure_resilience_value": row["infrastructure_resilience_value"],
                "winner": scored.iloc[0]["strategy"],
            })
    simulation = pd.DataFrame(rows)
    robustness = (
        simulation.groupby(["strategy_id", "strategy"])
        .agg(
            mean_infrastructure_resilience_value=("infrastructure_resilience_value", "mean"),
            median_infrastructure_resilience_value=("infrastructure_resilience_value", "median"),
            probability_ranked_first=("rank", lambda x: (x == 1).mean() * 100),
            probability_top_two=("rank", lambda x: (x <= 2).mean() * 100),
            probability_bottom_two=("rank", lambda x: (x >= len(strategies) - 1).mean() * 100),
        )
        .reset_index()
        .sort_values("probability_ranked_first", ascending=False)
    )
    return simulation, robustness

def expand_training(strategies: pd.DataFrame, n: int = 3600) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []
    for _ in range(n):
        base = strategies.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]
        record = {}
        for feature in FEATURES:
            record[feature] = float(np.clip(float(base[feature]) + rng.normal(0, 0.65), 1, 10))
        value = (
            0.10 * record["monitoring_value"]
            + 0.11 * record["predictive_maintenance"]
            + 0.11 * record["cyber_physical_security"]
            + 0.10 * record["digital_twin_capacity"]
            + 0.11 * record["redundancy_and_fallback"]
            + 0.11 * record["climate_adaptation"]
            + 0.12 * record["governance_quality"]
            + 0.12 * record["equity_performance"]
            + 0.10 * record["ecological_integration"]
            - 0.04 * record["fragility_risk"]
            - 0.04 * record["implementation_burden"]
            + rng.normal(0, 0.15)
        )
        review_gap = (
            max(0, 8.5 - record["governance_quality"])
            + max(0, 8.5 - record["equity_performance"])
            + max(0, 8.5 - record["redundancy_and_fallback"])
            + max(0, 8.4 - record["predictive_maintenance"])
            + max(0, 8.2 - record["ecological_integration"])
            + max(0, record["fragility_risk"] - 3.1)
            + max(0, record["implementation_burden"] - 3.8)
        )
        record["infrastructure_resilience_value"] = value
        record["review_gap"] = review_gap
        record["high_value_feasible"] = 1 if value >= 7.25 and record["fragility_risk"] <= 3.1 and record["implementation_burden"] <= 3.8 and review_gap <= 1.6 else 0
        rows.append(record)
    return pd.DataFrame(rows)

def main() -> None:
    strategies = pd.read_csv(ROOT / "data/raw/intelligent_infrastructure_strategies.csv")
    scenarios = pd.read_csv(ROOT / "data/raw/intelligent_infrastructure_scenarios.csv")
    profiles = calculate_strategy_profiles(strategies)
    rankings = scenario_rankings(strategies, scenarios)
    baseline = scenarios.loc[scenarios["scenario"] == "Balanced"].iloc[0]
    simulation, robustness = strategy_monte_carlo(strategies, baseline)

    profiles.to_csv(OUT_TABLES / "intelligent_infrastructure_strategy_profiles_advanced.csv", index=False)
    rankings.to_csv(OUT_TABLES / "intelligent_infrastructure_strategy_rankings_advanced.csv", index=False)
    simulation.to_csv(OUT_TABLES / "intelligent_infrastructure_monte_carlo_advanced.csv", index=False)
    robustness.to_csv(OUT_TABLES / "intelligent_infrastructure_robustness_summary_advanced.csv", index=False)

    training = expand_training(strategies)
    X = training[FEATURES + ["review_gap"]]
    y = training["high_value_feasible"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=450, min_samples_leaf=6, class_weight="balanced", random_state=42)
    model.fit(X_train, y_train)
    prob = model.predict_proba(X_test)[:, 1]
    pred = (prob >= 0.50).astype(int)

    metrics = pd.DataFrame([{
        "model": "random_forest_intelligent_infrastructure_resilience_classifier",
        "accuracy": accuracy_score(y_test, pred),
        "precision": precision_score(y_test, pred, zero_division=0),
        "recall": recall_score(y_test, pred, zero_division=0),
        "f1": f1_score(y_test, pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, prob),
        "brier_score": brier_score_loss(y_test, prob),
    }])
    importance = pd.DataFrame({"feature": FEATURES + ["review_gap"], "importance": model.feature_importances_}).sort_values("importance", ascending=False)

    metrics.to_csv(OUT_TABLES / "advanced_intelligent_infrastructure_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "intelligent_infrastructure_resilience_classifier.joblib")

    plt.figure(figsize=(10, 6))
    plt.bar(robustness["strategy"], robustness["probability_ranked_first"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Probability ranked first (%)")
    plt.title("Robustness of Intelligent Infrastructure Resilience Strategies")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "monte_carlo_probability_ranked_first.png", dpi=160)
    plt.close()

    print("Advanced intelligent infrastructure resilience workflow complete.")
    print(profiles[["strategy", "infrastructure_resilience_value", "adjusted_infrastructure_resilience_value", "diagnostic"]].round(4))
    print(metrics.round(4))

if __name__ == "__main__":
    main()
