#!/usr/bin/env python3
# Advanced Technology System Resilience workflow.
# Run: pip install -r requirements-advanced.txt && python python/technology_system_resilience_advanced.py

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
    "architecture",
    "redundancy",
    "observability",
    "cybersecurity",
    "data_integrity",
    "maintainability",
    "governance",
    "human_safeguards",
    "vendor_contingency",
    "technical_debt_risk",
    "implementation_burden",
]

def calculate_strategy_profiles(strategies: pd.DataFrame) -> pd.DataFrame:
    out = strategies.copy()
    out["technology_resilience_value"] = (
        0.10 * out["architecture"]
        + 0.10 * out["redundancy"]
        + 0.10 * out["observability"]
        + 0.11 * out["cybersecurity"]
        + 0.11 * out["data_integrity"]
        + 0.11 * out["maintainability"]
        + 0.11 * out["governance"]
        + 0.11 * out["human_safeguards"]
        + 0.10 * out["vendor_contingency"]
        - 0.03 * out["technical_debt_risk"]
        - 0.02 * out["implementation_burden"]
    )
    out["maintainability_gap"] = (8.3 - out["maintainability"]).clip(lower=0)
    out["governance_gap"] = (8.3 - out["governance"]).clip(lower=0)
    out["human_gap"] = (8.2 - out["human_safeguards"]).clip(lower=0)
    out["vendor_gap"] = (8.0 - out["vendor_contingency"]).clip(lower=0)
    out["adjusted_technology_resilience_value"] = (
        out["technology_resilience_value"]
        - 0.06 * out["maintainability_gap"]
        - 0.06 * out["governance_gap"]
        - 0.07 * out["human_gap"]
        - 0.05 * out["vendor_gap"]
    )
    out["human_adjusted_value"] = out["technology_resilience_value"] * (
        0.72 + 0.028 * out["human_safeguards"] - 0.010 * out["technical_debt_risk"]
    )
    conditions = [
        out["implementation_burden"] >= 3.7,
        out["technical_debt_risk"] >= 3.3,
        out["human_safeguards"] < 8.1,
        out["maintainability"] < 8.1,
        out["governance"] < 8.3,
        out["vendor_contingency"] < 7.9,
        out["technology_resilience_value"] >= 7.55,
    ]
    choices = [
        "implementation-burden review needed",
        "technical-debt review needed",
        "human-safeguards review needed",
        "maintainability review needed",
        "governance review needed",
        "vendor-contingency review needed",
        "strong technology resilience strategy candidate",
    ]
    out["diagnostic"] = np.select(conditions, choices, default="promising but requires stress testing")
    return out

def score_strategies(strategies: pd.DataFrame, scenario: pd.Series) -> pd.DataFrame:
    result = strategies.copy()
    result["technology_resilience_value"] = (
        scenario["architecture_weight"] * result["architecture"]
        + scenario["redundancy_weight"] * result["redundancy"]
        + scenario["observability_weight"] * result["observability"]
        + scenario["cybersecurity_weight"] * result["cybersecurity"]
        + scenario["data_integrity_weight"] * result["data_integrity"]
        + scenario["maintainability_weight"] * result["maintainability"]
        + scenario["governance_weight"] * result["governance"]
        + scenario["human_safeguards_weight"] * result["human_safeguards"]
        + scenario["vendor_contingency_weight"] * result["vendor_contingency"]
        - scenario["technical_debt_risk_weight"] * result["technical_debt_risk"]
        - scenario["implementation_burden_weight"] * result["implementation_burden"]
    )
    result = result.sort_values("technology_resilience_value", ascending=False).reset_index(drop=True)
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
                "technology_resilience_value": row["technology_resilience_value"],
                "winner": scored.iloc[0]["strategy"],
            })
    simulation = pd.DataFrame(rows)
    robustness = (
        simulation.groupby(["strategy_id", "strategy"])
        .agg(
            mean_technology_resilience_value=("technology_resilience_value", "mean"),
            median_technology_resilience_value=("technology_resilience_value", "median"),
            probability_ranked_first=("rank", lambda x: (x == 1).mean() * 100),
            probability_top_two=("rank", lambda x: (x <= 2).mean() * 100),
            probability_bottom_two=("rank", lambda x: (x >= len(strategies) - 1).mean() * 100),
        )
        .reset_index()
        .sort_values("probability_ranked_first", ascending=False)
    )
    return simulation, robustness

def expand_training(strategies: pd.DataFrame, n: int = 3200) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []
    for _ in range(n):
        base = strategies.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]
        record = {}
        for feature in FEATURES:
            record[feature] = float(np.clip(float(base[feature]) + rng.normal(0, 0.65), 1, 10))
        value = (
            0.10 * record["architecture"]
            + 0.10 * record["redundancy"]
            + 0.10 * record["observability"]
            + 0.11 * record["cybersecurity"]
            + 0.11 * record["data_integrity"]
            + 0.11 * record["maintainability"]
            + 0.11 * record["governance"]
            + 0.11 * record["human_safeguards"]
            + 0.10 * record["vendor_contingency"]
            - 0.03 * record["technical_debt_risk"]
            - 0.02 * record["implementation_burden"]
            + rng.normal(0, 0.15)
        )
        review_gap = (
            max(0, 8.3 - record["maintainability"])
            + max(0, 8.3 - record["governance"])
            + max(0, 8.2 - record["human_safeguards"])
            + max(0, 8.0 - record["vendor_contingency"])
            + max(0, record["technical_debt_risk"] - 3.3)
            + max(0, record["implementation_burden"] - 3.6)
        )
        record["technology_resilience_value"] = value
        record["review_gap"] = review_gap
        record["high_value_feasible"] = 1 if value >= 7.25 and record["technical_debt_risk"] <= 3.3 and record["implementation_burden"] <= 3.6 and review_gap <= 1.5 else 0
        rows.append(record)
    return pd.DataFrame(rows)

def main() -> None:
    strategies = pd.read_csv(ROOT / "data/raw/technology_resilience_strategies.csv")
    scenarios = pd.read_csv(ROOT / "data/raw/technology_resilience_scenarios.csv")
    profiles = calculate_strategy_profiles(strategies)
    rankings = scenario_rankings(strategies, scenarios)
    baseline = scenarios.loc[scenarios["scenario"] == "Balanced"].iloc[0]
    simulation, robustness = strategy_monte_carlo(strategies, baseline)

    profiles.to_csv(OUT_TABLES / "technology_resilience_strategy_profiles_advanced.csv", index=False)
    rankings.to_csv(OUT_TABLES / "technology_resilience_strategy_rankings_advanced.csv", index=False)
    simulation.to_csv(OUT_TABLES / "technology_resilience_monte_carlo_advanced.csv", index=False)
    robustness.to_csv(OUT_TABLES / "technology_resilience_robustness_summary_advanced.csv", index=False)

    training = expand_training(strategies)
    X = training[FEATURES + ["review_gap"]]
    y = training["high_value_feasible"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=450, min_samples_leaf=6, class_weight="balanced", random_state=42)
    model.fit(X_train, y_train)
    prob = model.predict_proba(X_test)[:, 1]
    pred = (prob >= 0.50).astype(int)

    metrics = pd.DataFrame([{
        "model": "random_forest_technology_resilience_classifier",
        "accuracy": accuracy_score(y_test, pred),
        "precision": precision_score(y_test, pred, zero_division=0),
        "recall": recall_score(y_test, pred, zero_division=0),
        "f1": f1_score(y_test, pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, prob),
        "brier_score": brier_score_loss(y_test, prob),
    }])
    importance = pd.DataFrame({"feature": FEATURES + ["review_gap"], "importance": model.feature_importances_}).sort_values("importance", ascending=False)

    metrics.to_csv(OUT_TABLES / "advanced_technology_resilience_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "technology_resilience_classifier.joblib")

    plt.figure(figsize=(10, 6))
    plt.bar(robustness["strategy"], robustness["probability_ranked_first"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Probability ranked first (%)")
    plt.title("Robustness of Technology Resilience Strategies")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "monte_carlo_probability_ranked_first.png", dpi=160)
    plt.close()

    print("Advanced technology resilience workflow complete.")
    print(profiles[["strategy", "technology_resilience_value", "adjusted_technology_resilience_value", "diagnostic"]].round(4))
    print(metrics.round(4))

if __name__ == "__main__":
    main()
