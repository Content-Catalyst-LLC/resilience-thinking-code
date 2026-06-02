#!/usr/bin/env python3
# Advanced sustainable resilience workflow.
# Run: pip install -r requirements-advanced.txt && python python/sustainable_resilience_advanced.py

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
    "resilience",
    "ecological_integrity",
    "social_inclusion",
    "economic_sufficiency",
    "governance_capacity",
    "adaptive_capacity",
    "resource_pressure",
    "implementation_burden",
]

def calculate_pathway_profiles(pathways: pd.DataFrame) -> pd.DataFrame:
    out = pathways.copy()
    out["viability_value"] = (
        0.18 * out["resilience"]
        + 0.17 * out["ecological_integrity"]
        + 0.16 * out["social_inclusion"]
        + 0.14 * out["economic_sufficiency"]
        + 0.14 * out["governance_capacity"]
        + 0.15 * out["adaptive_capacity"]
        - 0.04 * out["resource_pressure"]
        - 0.02 * out["implementation_burden"]
    )
    out["boundary_adjusted_viability"] = (
        out["viability_value"]
        - (out["resource_pressure"] - 3.8).clip(lower=0) * 0.20
        - (8.2 - out["social_inclusion"]).clip(lower=0) * 0.12
        - (8.2 - out["ecological_integrity"]).clip(lower=0) * 0.12
    )
    out["equity_adjusted_viability"] = out["viability_value"] * (0.72 + 0.028 * out["social_inclusion"])
    conditions = [
        out["resource_pressure"] >= 4.2,
        out["social_inclusion"] < 8.0,
        out["ecological_integrity"] < 8.0,
        out["governance_capacity"] < 8.0,
        out["implementation_burden"] >= 3.6,
        out["viability_value"] >= 8.0,
    ]
    choices = [
        "resource-pressure review needed",
        "social-inclusion safeguards need strengthening",
        "ecological-integrity safeguards need strengthening",
        "governance-capacity review needed",
        "implementation-burden review needed",
        "strong sustainable resilience pathway candidate",
    ]
    out["diagnostic"] = np.select(conditions, choices, default="promising but requires scenario validation")
    return out

def score_pathways(pathways: pd.DataFrame, scenario: pd.Series) -> pd.DataFrame:
    result = pathways.copy()
    result["viability_value"] = (
        scenario["resilience_weight"] * result["resilience"]
        + scenario["ecological_integrity_weight"] * result["ecological_integrity"]
        + scenario["social_inclusion_weight"] * result["social_inclusion"]
        + scenario["economic_sufficiency_weight"] * result["economic_sufficiency"]
        + scenario["governance_capacity_weight"] * result["governance_capacity"]
        + scenario["adaptive_capacity_weight"] * result["adaptive_capacity"]
        - scenario["resource_pressure_weight"] * result["resource_pressure"]
        - scenario["implementation_burden_weight"] * result["implementation_burden"]
    )
    result = result.sort_values("viability_value", ascending=False).reset_index(drop=True)
    result["rank"] = np.arange(1, len(result) + 1)
    result["scenario"] = scenario["scenario"]
    return result

def scenario_rankings(pathways: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    return pd.concat([score_pathways(pathways, scenario) for _, scenario in scenarios.iterrows()], ignore_index=True)

def pathway_monte_carlo(pathways: pd.DataFrame, scenario: pd.Series, n: int = 5000):
    rng = np.random.default_rng(42)
    rows = []
    for simulation_id in range(n):
        sampled = pathways.copy()
        for criterion in FEATURES:
            sampled[criterion] = rng.normal(loc=pathways[criterion], scale=0.6).clip(1, 10)
        scored = score_pathways(sampled, scenario)
        for _, row in scored.iterrows():
            rows.append({
                "simulation_id": simulation_id,
                "pathway_id": row["pathway_id"],
                "pathway": row["pathway"],
                "rank": int(row["rank"]),
                "viability_value": row["viability_value"],
                "winner": scored.iloc[0]["pathway"],
            })
    simulation = pd.DataFrame(rows)
    robustness = (
        simulation.groupby(["pathway_id", "pathway"])
        .agg(
            mean_viability_value=("viability_value", "mean"),
            median_viability_value=("viability_value", "median"),
            probability_ranked_first=("rank", lambda x: (x == 1).mean() * 100),
            probability_top_two=("rank", lambda x: (x <= 2).mean() * 100),
            probability_bottom_two=("rank", lambda x: (x >= len(pathways) - 1).mean() * 100),
        )
        .reset_index()
        .sort_values("probability_ranked_first", ascending=False)
    )
    return simulation, robustness

def expand_training(pathways: pd.DataFrame, n: int = 2600) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []
    for _ in range(n):
        base = pathways.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]
        record = {}
        for feature in FEATURES:
            record[feature] = float(np.clip(float(base[feature]) + rng.normal(0, 0.7), 1, 10))
        value = (
            0.18 * record["resilience"]
            + 0.17 * record["ecological_integrity"]
            + 0.16 * record["social_inclusion"]
            + 0.14 * record["economic_sufficiency"]
            + 0.14 * record["governance_capacity"]
            + 0.15 * record["adaptive_capacity"]
            - 0.04 * record["resource_pressure"]
            - 0.02 * record["implementation_burden"]
            + rng.normal(0, 0.18)
        )
        boundary_risk = max(0, record["resource_pressure"] - 3.8) + max(0, 8.2 - record["ecological_integrity"]) + max(0, 8.2 - record["social_inclusion"])
        record["viability_value"] = value
        record["boundary_risk"] = boundary_risk
        record["high_value_feasible"] = 1 if value >= 7.85 and record["implementation_burden"] <= 3.5 and boundary_risk <= 0.9 else 0
        rows.append(record)
    return pd.DataFrame(rows)

def main() -> None:
    pathways = pd.read_csv(ROOT / "data/raw/sustainable_resilience_pathways.csv")
    scenarios = pd.read_csv(ROOT / "data/raw/sustainable_resilience_scenarios.csv")
    profiles = calculate_pathway_profiles(pathways)
    rankings = scenario_rankings(pathways, scenarios)
    baseline = scenarios.loc[scenarios["scenario"] == "Balanced"].iloc[0]
    simulation, robustness = pathway_monte_carlo(pathways, baseline)

    profiles.to_csv(OUT_TABLES / "sustainable_resilience_pathway_profiles_advanced.csv", index=False)
    rankings.to_csv(OUT_TABLES / "sustainable_resilience_pathway_rankings_advanced.csv", index=False)
    simulation.to_csv(OUT_TABLES / "sustainable_resilience_monte_carlo_advanced.csv", index=False)
    robustness.to_csv(OUT_TABLES / "sustainable_resilience_robustness_summary_advanced.csv", index=False)

    training = expand_training(pathways)
    X = training[FEATURES + ["boundary_risk"]]
    y = training["high_value_feasible"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=450, min_samples_leaf=6, class_weight="balanced", random_state=42)
    model.fit(X_train, y_train)
    prob = model.predict_proba(X_test)[:, 1]
    pred = (prob >= 0.50).astype(int)

    metrics = pd.DataFrame([{
        "model": "random_forest_sustainable_resilience_classifier",
        "accuracy": accuracy_score(y_test, pred),
        "precision": precision_score(y_test, pred, zero_division=0),
        "recall": recall_score(y_test, pred, zero_division=0),
        "f1": f1_score(y_test, pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, prob),
        "brier_score": brier_score_loss(y_test, prob),
    }])
    importance = pd.DataFrame({"feature": FEATURES + ["boundary_risk"], "importance": model.feature_importances_}).sort_values("importance", ascending=False)

    metrics.to_csv(OUT_TABLES / "advanced_sustainable_resilience_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "sustainable_resilience_classifier.joblib")

    plt.figure(figsize=(10, 6))
    plt.bar(robustness["pathway"], robustness["probability_ranked_first"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Probability ranked first (%)")
    plt.title("Robustness of Sustainable Resilience Pathways")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "monte_carlo_probability_ranked_first.png", dpi=160)
    plt.close()

    print("Advanced sustainable resilience workflow complete.")
    print(profiles[["pathway", "viability_value", "boundary_adjusted_viability", "diagnostic"]].round(4))
    print(metrics.round(4))

if __name__ == "__main__":
    main()
