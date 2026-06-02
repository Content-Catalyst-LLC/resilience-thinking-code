#!/usr/bin/env python3
# Advanced Strategic Slack and Resilience workflow.
# Run: pip install -r requirements-advanced.txt && python python/strategic_slack_resilience_advanced.py

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
    "financial_slack",
    "workforce_slack",
    "operational_slack",
    "knowledge_slack",
    "network_slack",
    "governance_slack",
    "ethical_safeguards",
    "ethical_burden",
    "implementation_burden",
]

def calculate_portfolio_profiles(portfolios: pd.DataFrame) -> pd.DataFrame:
    out = portfolios.copy()
    out["slack_resilience_value"] = (
        0.13 * out["financial_slack"]
        + 0.14 * out["workforce_slack"]
        + 0.13 * out["operational_slack"]
        + 0.13 * out["knowledge_slack"]
        + 0.13 * out["network_slack"]
        + 0.14 * out["governance_slack"]
        + 0.13 * out["ethical_safeguards"]
        - 0.04 * out["ethical_burden"]
        - 0.03 * out["implementation_burden"]
    )
    out["workforce_gap"] = (8.2 - out["workforce_slack"]).clip(lower=0)
    out["knowledge_gap"] = (8.2 - out["knowledge_slack"]).clip(lower=0)
    out["governance_gap"] = (8.2 - out["governance_slack"]).clip(lower=0)
    out["adjusted_slack_resilience_value"] = (
        out["slack_resilience_value"]
        - 0.07 * out["workforce_gap"]
        - 0.06 * out["knowledge_gap"]
        - 0.06 * out["governance_gap"]
    )
    out["ethical_adjusted_value"] = out["slack_resilience_value"] * (
        0.72 + 0.028 * out["ethical_safeguards"] - 0.010 * out["ethical_burden"]
    )
    conditions = [
        out["implementation_burden"] >= 3.6,
        out["ethical_burden"] >= 3.2,
        out["workforce_slack"] < 7.6,
        out["knowledge_slack"] < 7.6,
        out["governance_slack"] < 7.8,
        out["slack_resilience_value"] >= 7.25,
    ]
    choices = [
        "implementation-burden review needed",
        "ethical-burden review needed",
        "workforce-slack review needed",
        "knowledge-slack review needed",
        "governance-slack review needed",
        "strong strategic slack portfolio candidate",
    ]
    out["diagnostic"] = np.select(conditions, choices, default="promising but requires scenario testing")
    return out

def score_portfolios(portfolios: pd.DataFrame, scenario: pd.Series) -> pd.DataFrame:
    result = portfolios.copy()
    result["slack_resilience_value"] = (
        scenario["financial_slack_weight"] * result["financial_slack"]
        + scenario["workforce_slack_weight"] * result["workforce_slack"]
        + scenario["operational_slack_weight"] * result["operational_slack"]
        + scenario["knowledge_slack_weight"] * result["knowledge_slack"]
        + scenario["network_slack_weight"] * result["network_slack"]
        + scenario["governance_slack_weight"] * result["governance_slack"]
        + scenario["ethical_safeguards_weight"] * result["ethical_safeguards"]
        - scenario["ethical_burden_weight"] * result["ethical_burden"]
        - scenario["implementation_burden_weight"] * result["implementation_burden"]
    )
    result = result.sort_values("slack_resilience_value", ascending=False).reset_index(drop=True)
    result["rank"] = np.arange(1, len(result) + 1)
    result["scenario"] = scenario["scenario"]
    return result

def scenario_rankings(portfolios: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    return pd.concat([score_portfolios(portfolios, scenario) for _, scenario in scenarios.iterrows()], ignore_index=True)

def portfolio_monte_carlo(portfolios: pd.DataFrame, scenario: pd.Series, n: int = 5000):
    rng = np.random.default_rng(42)
    rows = []
    for simulation_id in range(n):
        sampled = portfolios.copy()
        for criterion in FEATURES:
            sampled[criterion] = rng.normal(loc=portfolios[criterion], scale=0.55).clip(1, 10)
        scored = score_portfolios(sampled, scenario)
        for _, row in scored.iterrows():
            rows.append({
                "simulation_id": simulation_id,
                "portfolio_id": row["portfolio_id"],
                "portfolio": row["portfolio"],
                "rank": int(row["rank"]),
                "slack_resilience_value": row["slack_resilience_value"],
                "winner": scored.iloc[0]["portfolio"],
            })
    simulation = pd.DataFrame(rows)
    robustness = (
        simulation.groupby(["portfolio_id", "portfolio"])
        .agg(
            mean_slack_resilience_value=("slack_resilience_value", "mean"),
            median_slack_resilience_value=("slack_resilience_value", "median"),
            probability_ranked_first=("rank", lambda x: (x == 1).mean() * 100),
            probability_top_two=("rank", lambda x: (x <= 2).mean() * 100),
            probability_bottom_two=("rank", lambda x: (x >= len(portfolios) - 1).mean() * 100),
        )
        .reset_index()
        .sort_values("probability_ranked_first", ascending=False)
    )
    return simulation, robustness

def expand_training(portfolios: pd.DataFrame, n: int = 2800) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []
    for _ in range(n):
        base = portfolios.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]
        record = {}
        for feature in FEATURES:
            record[feature] = float(np.clip(float(base[feature]) + rng.normal(0, 0.65), 1, 10))
        value = (
            0.13 * record["financial_slack"]
            + 0.14 * record["workforce_slack"]
            + 0.13 * record["operational_slack"]
            + 0.13 * record["knowledge_slack"]
            + 0.13 * record["network_slack"]
            + 0.14 * record["governance_slack"]
            + 0.13 * record["ethical_safeguards"]
            - 0.04 * record["ethical_burden"]
            - 0.03 * record["implementation_burden"]
            + rng.normal(0, 0.15)
        )
        review_gap = (
            max(0, 8.2 - record["workforce_slack"])
            + max(0, 8.2 - record["knowledge_slack"])
            + max(0, 8.2 - record["governance_slack"])
            + max(0, record["ethical_burden"] - 3.1)
            + max(0, record["implementation_burden"] - 3.5)
        )
        record["slack_resilience_value"] = value
        record["review_gap"] = review_gap
        record["high_value_feasible"] = 1 if value >= 7.15 and record["ethical_burden"] <= 3.1 and record["implementation_burden"] <= 3.5 and review_gap <= 1.2 else 0
        rows.append(record)
    return pd.DataFrame(rows)

def main() -> None:
    portfolios = pd.read_csv(ROOT / "data/raw/strategic_slack_portfolios.csv")
    scenarios = pd.read_csv(ROOT / "data/raw/strategic_slack_scenarios.csv")
    profiles = calculate_portfolio_profiles(portfolios)
    rankings = scenario_rankings(portfolios, scenarios)
    baseline = scenarios.loc[scenarios["scenario"] == "Balanced"].iloc[0]
    simulation, robustness = portfolio_monte_carlo(portfolios, baseline)

    profiles.to_csv(OUT_TABLES / "strategic_slack_portfolio_profiles_advanced.csv", index=False)
    rankings.to_csv(OUT_TABLES / "strategic_slack_portfolio_rankings_advanced.csv", index=False)
    simulation.to_csv(OUT_TABLES / "strategic_slack_monte_carlo_advanced.csv", index=False)
    robustness.to_csv(OUT_TABLES / "strategic_slack_robustness_summary_advanced.csv", index=False)

    training = expand_training(portfolios)
    X = training[FEATURES + ["review_gap"]]
    y = training["high_value_feasible"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=450, min_samples_leaf=6, class_weight="balanced", random_state=42)
    model.fit(X_train, y_train)
    prob = model.predict_proba(X_test)[:, 1]
    pred = (prob >= 0.50).astype(int)

    metrics = pd.DataFrame([{
        "model": "random_forest_strategic_slack_resilience_classifier",
        "accuracy": accuracy_score(y_test, pred),
        "precision": precision_score(y_test, pred, zero_division=0),
        "recall": recall_score(y_test, pred, zero_division=0),
        "f1": f1_score(y_test, pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, prob),
        "brier_score": brier_score_loss(y_test, prob),
    }])
    importance = pd.DataFrame({"feature": FEATURES + ["review_gap"], "importance": model.feature_importances_}).sort_values("importance", ascending=False)

    metrics.to_csv(OUT_TABLES / "advanced_strategic_slack_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "strategic_slack_resilience_classifier.joblib")

    plt.figure(figsize=(10, 6))
    plt.bar(robustness["portfolio"], robustness["probability_ranked_first"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Probability ranked first (%)")
    plt.title("Robustness of Strategic Slack Portfolios")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "monte_carlo_probability_ranked_first.png", dpi=160)
    plt.close()

    print("Advanced strategic slack resilience workflow complete.")
    print(profiles[["portfolio", "slack_resilience_value", "adjusted_slack_resilience_value", "diagnostic"]].round(4))
    print(metrics.round(4))

if __name__ == "__main__":
    main()
