#!/usr/bin/env python3
"""
Advanced risk-governance and resilience workflow.

Uses pandas, numpy, matplotlib, scikit-learn, and joblib.

Run:
    pip install -r requirements-advanced.txt
    python python/risk_governance_resilience_advanced.py
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
PROFILES_PATH = ROOT / "data" / "raw" / "risk_governance_resilience_profiles.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_FIGURES = ROOT / "outputs" / "figures"
OUT_MODELS = ROOT / "outputs" / "models"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)
OUT_MODELS.mkdir(parents=True, exist_ok=True)

FEATURES = [
    "hazard_intensity",
    "exposure",
    "vulnerability",
    "buffer_capacity",
    "adaptive_capacity",
    "learning_capacity",
    "trust",
    "participation_quality",
    "knowledge_integration",
    "coordination_quality",
    "transparency",
    "accountability",
]


def score_profiles(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["risk_pressure"] = (
        out["hazard_intensity"]
        * out["exposure"]
        * out["vulnerability"]
        * (1 - 0.55 * out["adaptive_capacity"])
    )
    out["governance_capacity"] = (
        0.18 * out["trust"]
        + 0.17 * out["participation_quality"]
        + 0.17 * out["knowledge_integration"]
        + 0.18 * out["coordination_quality"]
        + 0.15 * out["transparency"]
        + 0.15 * out["accountability"]
    )
    out["resilience_capacity"] = (
        0.26 * out["buffer_capacity"]
        + 0.28 * out["adaptive_capacity"]
        + 0.22 * out["learning_capacity"]
        + 0.24 * out["governance_capacity"]
    )
    out["resilience_margin"] = (
        out["buffer_capacity"]
        + out["adaptive_capacity"]
        + out["learning_capacity"]
        + out["governance_capacity"]
        - out["risk_pressure"]
        - out["vulnerability"]
    )
    return out


def expand_training(df: pd.DataFrame, n: int = 1800) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []

    for _ in range(n):
        base = df.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]
        record = {}

        for feature in FEATURES:
            record[feature] = float(np.clip(float(base[feature]) + rng.normal(0, 0.08), 0.05, 0.98))

        risk_pressure = (
            record["hazard_intensity"]
            * record["exposure"]
            * record["vulnerability"]
            * (1 - 0.55 * record["adaptive_capacity"])
        )
        governance_capacity = (
            0.18 * record["trust"]
            + 0.17 * record["participation_quality"]
            + 0.17 * record["knowledge_integration"]
            + 0.18 * record["coordination_quality"]
            + 0.15 * record["transparency"]
            + 0.15 * record["accountability"]
        )
        resilience_margin = (
            record["buffer_capacity"]
            + record["adaptive_capacity"]
            + record["learning_capacity"]
            + governance_capacity
            - risk_pressure
            - record["vulnerability"]
            + rng.normal(0, 0.05)
        )

        record["risk_pressure"] = risk_pressure
        record["governance_capacity"] = governance_capacity
        record["resilience_margin"] = resilience_margin
        record["threshold_risk"] = 1 if resilience_margin < 1.05 else 0
        rows.append(record)

    return pd.DataFrame(rows)


def plot_profiles(profiles: pd.DataFrame) -> None:
    plot_df = profiles[["system_type", "risk_pressure", "governance_capacity", "resilience_capacity", "resilience_margin"]].melt(
        id_vars="system_type",
        var_name="indicator",
        value_name="value",
    )

    order = profiles.sort_values("resilience_margin")["system_type"].tolist()
    plt.figure(figsize=(10, 6))

    for indicator, subset in plot_df.groupby("indicator"):
        y = [order.index(s) for s in subset["system_type"]]
        plt.scatter(subset["value"], y, label=indicator, s=58)

    plt.yticks(range(len(order)), order)
    plt.xlabel("Indicator value")
    plt.title("Risk Governance and Resilience Indicators")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "risk_governance_indicator_profiles.png", dpi=160)
    plt.close()


def main() -> None:
    profiles_raw = pd.read_csv(PROFILES_PATH)
    profiles = score_profiles(profiles_raw)

    profiles.to_csv(OUT_TABLES / "risk_governance_profiles_advanced.csv", index=False)
    plot_profiles(profiles)

    training = expand_training(profiles_raw)
    X = training[FEATURES]
    y = training["threshold_risk"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=350,
        min_samples_leaf=6,
        class_weight="balanced",
        random_state=42,
    )
    model.fit(X_train, y_train)
    prob = model.predict_proba(X_test)[:, 1]
    pred = (prob >= 0.50).astype(int)

    metrics = pd.DataFrame(
        [{
            "model": "random_forest_governance_resilience_threshold_classifier",
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

    training.to_csv(OUT_TABLES / "synthetic_governance_resilience_training_data.csv", index=False)
    metrics.to_csv(OUT_TABLES / "advanced_threshold_risk_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "risk_governance_threshold_classifier.joblib")

    plt.figure(figsize=(10, 6))
    plt.barh(importance["feature"], importance["importance"])
    plt.gca().invert_yaxis()
    plt.xlabel("Importance")
    plt.title("Feature Importance for Governance-Resilience Threshold Risk")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "advanced_feature_importance.png", dpi=160)
    plt.close()

    print("Advanced risk-governance resilience workflow complete.")
    print(profiles[["system_type", "risk_pressure", "governance_capacity", "resilience_margin"]].round(3))
    print(metrics.round(4))


if __name__ == "__main__":
    main()
