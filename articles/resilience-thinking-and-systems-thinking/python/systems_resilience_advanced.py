#!/usr/bin/env python3
"""
Advanced systems-resilience workflow.

Uses pandas, numpy, matplotlib, scikit-learn, and joblib.

Run:
    pip install -r requirements-advanced.txt
    python python/systems_resilience_advanced.py
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

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
PROFILES_PATH = ROOT / "data" / "raw" / "systems_resilience_profiles.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_FIGURES = ROOT / "outputs" / "figures"
OUT_MODELS = ROOT / "outputs" / "models"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)
OUT_MODELS.mkdir(parents=True, exist_ok=True)

FEATURES = [
    "feedback_visibility",
    "boundary_clarity",
    "leverage_capacity",
    "delay_management",
    "adaptive_capacity",
    "redundancy",
    "threshold_distance",
    "buffer_capacity",
    "vulnerability_pressure",
    "disturbance_exposure",
    "reinforcing_vulnerability",
    "balancing_repair",
    "feedback_delay",
]


def score_profiles(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["systems_thinking_score"] = (
        0.28 * out["feedback_visibility"]
        + 0.24 * out["boundary_clarity"]
        + 0.24 * out["leverage_capacity"]
        + 0.24 * out["delay_management"]
    )
    out["resilience_thinking_score"] = (
        0.24 * out["adaptive_capacity"]
        + 0.20 * out["redundancy"]
        + 0.22 * out["threshold_distance"]
        + 0.18 * out["buffer_capacity"]
        - 0.08 * out["vulnerability_pressure"]
        - 0.08 * out["disturbance_exposure"]
    )
    out["combined_system_resilience"] = 0.5 * out["systems_thinking_score"] + 0.5 * out["resilience_thinking_score"]
    out["structural_fragility_index"] = np.clip(
        0.28 * (1 - out["feedback_visibility"])
        + 0.20 * (1 - out["boundary_clarity"])
        + 0.20 * (1 - out["delay_management"])
        + 0.18 * out["vulnerability_pressure"]
        + 0.14 * out["disturbance_exposure"],
        0,
        1,
    )
    return out


def expand_training(df: pd.DataFrame, n: int = 1800) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []

    for _ in range(n):
        base = df.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]
        record = {}
        for feature in FEATURES:
            if feature == "feedback_delay":
                record[feature] = int(np.clip(round(float(base[feature]) + rng.normal(0, 1.2)), 1, 8))
            else:
                record[feature] = float(np.clip(float(base[feature]) + rng.normal(0, 0.08), 0.05, 0.98))

        systems_score = (
            0.28 * record["feedback_visibility"]
            + 0.24 * record["boundary_clarity"]
            + 0.24 * record["leverage_capacity"]
            + 0.24 * record["delay_management"]
        )
        resilience_score = (
            0.24 * record["adaptive_capacity"]
            + 0.20 * record["redundancy"]
            + 0.22 * record["threshold_distance"]
            + 0.18 * record["buffer_capacity"]
            - 0.08 * record["vulnerability_pressure"]
            - 0.08 * record["disturbance_exposure"]
        )
        risk_pressure = (
            0.25 * record["vulnerability_pressure"]
            + 0.22 * record["disturbance_exposure"]
            + 0.20 * record["reinforcing_vulnerability"]
            + 0.18 * (record["feedback_delay"] / 8.0)
            - 0.15 * record["balancing_repair"]
        )
        latent_margin = 0.45 * systems_score + 0.55 * resilience_score - 0.55 * risk_pressure + rng.normal(0, 0.05)
        record["systems_thinking_score"] = systems_score
        record["resilience_thinking_score"] = resilience_score
        record["threshold_failure_risk"] = 1 if latent_margin < 0.32 else 0
        rows.append(record)

    return pd.DataFrame(rows)


def plot_profile_scores(profiles: pd.DataFrame) -> None:
    plot_df = profiles[["system_type", "systems_thinking_score", "resilience_thinking_score", "combined_system_resilience"]].melt(
        id_vars="system_type",
        var_name="index",
        value_name="score",
    )

    systems = profiles.sort_values("combined_system_resilience")["system_type"].tolist()
    plt.figure(figsize=(10, 6))

    for index_name, subset in plot_df.groupby("index"):
        y = [systems.index(s) for s in subset["system_type"]]
        plt.scatter(subset["score"], y, label=index_name, s=65)

    plt.yticks(range(len(systems)), systems)
    plt.xlabel("Score")
    plt.title("Systems Thinking and Resilience Thinking Indicators")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "systems_resilience_indicator_scores.png", dpi=160)
    plt.close()


def main() -> None:
    systems = pd.read_csv(PROFILES_PATH)
    profiles = score_profiles(systems)
    profiles.to_csv(OUT_TABLES / "systems_resilience_profiles_advanced.csv", index=False)
    plot_profile_scores(profiles)

    training = expand_training(systems)
    X = training[FEATURES]
    y = training["threshold_failure_risk"]

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
    pred = (prob >= 0.5).astype(int)

    metrics = pd.DataFrame(
        [{
            "model": "random_forest_threshold_failure_classifier",
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

    training.to_csv(OUT_TABLES / "synthetic_threshold_failure_training_data.csv", index=False)
    metrics.to_csv(OUT_TABLES / "advanced_threshold_failure_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "systems_resilience_threshold_classifier.joblib")

    plt.figure(figsize=(10, 6))
    plt.barh(importance["feature"], importance["importance"])
    plt.gca().invert_yaxis()
    plt.xlabel("Importance")
    plt.title("Feature Importance for Threshold-Failure Risk")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "advanced_feature_importance.png", dpi=160)
    plt.close()

    print("Advanced systems-resilience workflow complete.")
    print(profiles[["system_type", "systems_thinking_score", "resilience_thinking_score", "combined_system_resilience", "structural_fragility_index"]].round(3))
    print(metrics.round(4))


if __name__ == "__main__":
    main()
