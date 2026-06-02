#!/usr/bin/env python3
# Advanced Public Health System Resilience workflow.
# Run: pip install -r requirements-advanced.txt && python python/public_health_resilience_advanced.py

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
    "prevention",
    "detection",
    "service_continuity",
    "workforce_capacity",
    "adaptive_governance",
    "trust",
    "equity_protection",
    "implementation_burden",
]

def calculate_strategy_profiles(strategies: pd.DataFrame) -> pd.DataFrame:
    out = strategies.copy()
    out["base_resilience_value"] = (
        0.14 * out["prevention"]
        + 0.15 * out["detection"]
        + 0.15 * out["service_continuity"]
        + 0.14 * out["workforce_capacity"]
        + 0.14 * out["adaptive_governance"]
        + 0.13 * out["trust"]
        + 0.13 * out["equity_protection"]
        - 0.02 * out["implementation_burden"]
    )
    out["equity_adjusted_value"] = out["base_resilience_value"] * (0.72 + 0.028 * out["equity_protection"])
    conditions = [
        (out["base_resilience_value"] >= 8.15) & (out["implementation_burden"] <= 3.0),
        out["implementation_burden"] >= 3.5,
        out["trust"] < 7.8,
        out["equity_protection"] < 8.0,
        out["service_continuity"] < 8.0,
    ]
    choices = [
        "strong public health resilience profile with manageable implementation burden",
        "implementation burden review needed",
        "trust and communication review needed",
        "equity protection needs strengthening",
        "service continuity needs strengthening",
    ]
    out["diagnostic"] = np.select(conditions, choices, default="promising but requires public health scenario validation")
    return out

def score_strategies(strategies: pd.DataFrame, scenario: pd.Series) -> pd.DataFrame:
    result = strategies.copy()
    result["resilience_value"] = (
        scenario["prevention_weight"] * result["prevention"]
        + scenario["detection_weight"] * result["detection"]
        + scenario["service_continuity_weight"] * result["service_continuity"]
        + scenario["workforce_capacity_weight"] * result["workforce_capacity"]
        + scenario["adaptive_governance_weight"] * result["adaptive_governance"]
        + scenario["trust_weight"] * result["trust"]
        + scenario["equity_protection_weight"] * result["equity_protection"]
        - scenario["implementation_burden_weight"] * result["implementation_burden"]
    )
    result = result.sort_values("resilience_value", ascending=False).reset_index(drop=True)
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
                "resilience_value": row["resilience_value"],
                "winner": scored.iloc[0]["strategy"],
            })
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
            0.14 * record["prevention"]
            + 0.15 * record["detection"]
            + 0.15 * record["service_continuity"]
            + 0.14 * record["workforce_capacity"]
            + 0.14 * record["adaptive_governance"]
            + 0.13 * record["trust"]
            + 0.13 * record["equity_protection"]
            - 0.02 * record["implementation_burden"]
            + rng.normal(0, 0.18)
        )
        record["resilience_value"] = value
        record["high_value_feasible"] = 1 if value >= 8.05 and record["implementation_burden"] <= 3.2 else 0
        rows.append(record)
    return pd.DataFrame(rows)

def main() -> None:
    strategies = pd.read_csv(ROOT / "data/raw/public_health_resilience_strategies.csv")
    scenarios = pd.read_csv(ROOT / "data/raw/public_health_resilience_scenarios.csv")
    profiles = calculate_strategy_profiles(strategies)
    rankings = scenario_rankings(strategies, scenarios)
    baseline = scenarios.loc[scenarios["scenario"] == "Balanced"].iloc[0]
    simulation, robustness = strategy_monte_carlo(strategies, baseline)

    profiles.to_csv(OUT_TABLES / "public_health_resilience_strategy_profiles_advanced.csv", index=False)
    rankings.to_csv(OUT_TABLES / "public_health_resilience_strategy_rankings_advanced.csv", index=False)
    simulation.to_csv(OUT_TABLES / "public_health_resilience_monte_carlo_advanced.csv", index=False)
    robustness.to_csv(OUT_TABLES / "public_health_resilience_robustness_summary_advanced.csv", index=False)

    training = expand_training(strategies)
    X = training[FEATURES]
    y = training["high_value_feasible"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=450, min_samples_leaf=6, class_weight="balanced", random_state=42)
    model.fit(X_train, y_train)
    prob = model.predict_proba(X_test)[:, 1]
    pred = (prob >= 0.50).astype(int)

    metrics = pd.DataFrame([{
        "model": "random_forest_public_health_resilience_classifier",
        "accuracy": accuracy_score(y_test, pred),
        "precision": precision_score(y_test, pred, zero_division=0),
        "recall": recall_score(y_test, pred, zero_division=0),
        "f1": f1_score(y_test, pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, prob),
        "brier_score": brier_score_loss(y_test, prob),
    }])
    importance = pd.DataFrame({"feature": FEATURES, "importance": model.feature_importances_}).sort_values("importance", ascending=False)

    metrics.to_csv(OUT_TABLES / "advanced_public_health_resilience_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "public_health_resilience_classifier.joblib")

    plt.figure(figsize=(10, 6))
    plt.bar(robustness["strategy"], robustness["probability_ranked_first"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Probability ranked first (%)")
    plt.title("Robustness of Public Health Resilience Strategies")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "monte_carlo_probability_ranked_first.png", dpi=160)
    plt.close()

    print("Advanced public health resilience workflow complete.")
    print(profiles[["strategy", "base_resilience_value", "equity_adjusted_value", "diagnostic"]].round(4))
    print(metrics.round(4))

if __name__ == "__main__":
    main()
