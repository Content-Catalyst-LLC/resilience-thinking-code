#!/usr/bin/env python3
"""
Advanced engineering/ecological resilience workflow.

Uses pandas, numpy, matplotlib, scikit-learn, and joblib.

Run:
    pip install -r requirements-advanced.txt
    python python/engineering_ecological_resilience_advanced.py
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
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_absolute_error, r2_score
    from sklearn.model_selection import train_test_split
except ImportError as exc:
    raise SystemExit(
        "Missing advanced dependency. Run: pip install -r requirements-advanced.txt"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
SYSTEMS_PATH = ROOT / "data" / "raw" / "engineering_ecological_resilience_systems.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_FIGURES = ROOT / "outputs" / "figures"
OUT_MODELS = ROOT / "outputs" / "models"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)
OUT_MODELS.mkdir(parents=True, exist_ok=True)

FEATURES = [
    "return_speed",
    "reliability",
    "repair_capacity",
    "backup_capacity",
    "service_continuity",
    "threshold_distance",
    "basin_width",
    "adaptive_capacity",
    "functional_diversity",
    "redundancy",
    "modularity",
    "disturbance_exposure",
    "regime_shift_sensitivity",
]


def score_profiles(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    out["engineering_resilience"] = (
        0.28 * out["return_speed"]
        + 0.24 * out["reliability"]
        + 0.18 * out["repair_capacity"]
        + 0.15 * out["backup_capacity"]
        + 0.15 * out["service_continuity"]
    )

    out["ecological_resilience"] = (
        0.20 * out["threshold_distance"]
        + 0.18 * out["basin_width"]
        + 0.18 * out["adaptive_capacity"]
        + 0.15 * out["functional_diversity"]
        + 0.13 * out["redundancy"]
        + 0.10 * out["modularity"]
        - 0.08 * out["disturbance_exposure"]
        - 0.08 * out["regime_shift_sensitivity"]
    )

    out["resilience_gap"] = out["ecological_resilience"] - out["engineering_resilience"]
    out["regime_shift_risk"] = np.clip(
        0.42 * out["disturbance_exposure"]
        + 0.34 * out["regime_shift_sensitivity"]
        - 0.28 * out["threshold_distance"]
        - 0.22 * out["adaptive_capacity"]
        - 0.16 * out["functional_diversity"],
        0,
        1,
    )

    return out


def expand_synthetic_training(df: pd.DataFrame, n: int = 1500) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []

    for _ in range(n):
        base = df.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0].copy()
        record = {}
        for col in FEATURES:
            record[col] = float(np.clip(base[col] + rng.normal(0, 0.08), 0.05, 0.98))

        record["target_ecological_resilience"] = (
            0.20 * record["threshold_distance"]
            + 0.18 * record["basin_width"]
            + 0.18 * record["adaptive_capacity"]
            + 0.15 * record["functional_diversity"]
            + 0.13 * record["redundancy"]
            + 0.10 * record["modularity"]
            - 0.08 * record["disturbance_exposure"]
            - 0.08 * record["regime_shift_sensitivity"]
            + rng.normal(0, 0.025)
        )
        rows.append(record)

    return pd.DataFrame(rows)


def plot_profiles(profiles: pd.DataFrame) -> None:
    plot_df = profiles[["system_type", "engineering_resilience", "ecological_resilience"]].melt(
        id_vars="system_type",
        var_name="resilience_type",
        value_name="score",
    )

    pivot_order = profiles.sort_values("ecological_resilience")["system_type"].tolist()

    plt.figure(figsize=(10, 6))
    width = 0.38
    x = np.arange(len(pivot_order))

    eng = profiles.set_index("system_type").loc[pivot_order, "engineering_resilience"]
    eco = profiles.set_index("system_type").loc[pivot_order, "ecological_resilience"]

    plt.barh(x - width / 2, eng, height=width, label="Engineering resilience")
    plt.barh(x + width / 2, eco, height=width, label="Ecological resilience")
    plt.yticks(x, pivot_order)
    plt.xlabel("Score")
    plt.title("Engineering vs Ecological Resilience Profiles")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "engineering_vs_ecological_profiles.png", dpi=160)
    plt.close()


def main() -> None:
    systems = pd.read_csv(SYSTEMS_PATH)
    profiles = score_profiles(systems)

    profiles.to_csv(OUT_TABLES / "engineering_ecological_profiles_advanced.csv", index=False)
    plot_profiles(profiles)

    training = expand_synthetic_training(systems)
    X = training[FEATURES]
    y = training["target_ecological_resilience"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=350,
        min_samples_leaf=6,
        random_state=42,
    )
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    metrics = pd.DataFrame(
        [
            {
                "model": "random_forest_regressor",
                "mean_absolute_error": mean_absolute_error(y_test, predictions),
                "r2_score": r2_score(y_test, predictions),
            }
        ]
    )

    importance = pd.DataFrame(
        {
            "feature": FEATURES,
            "importance": model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)

    training.to_csv(OUT_TABLES / "synthetic_training_data_advanced.csv", index=False)
    metrics.to_csv(OUT_TABLES / "advanced_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "ecological_resilience_regressor.joblib")

    plt.figure(figsize=(10, 6))
    plt.barh(importance["feature"], importance["importance"])
    plt.gca().invert_yaxis()
    plt.xlabel("Importance")
    plt.title("Feature Importance for Ecological Resilience Prediction")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "advanced_feature_importance.png", dpi=160)
    plt.close()

    print("Advanced engineering/ecological resilience workflow complete.")
    print(profiles[["system_type", "engineering_resilience", "ecological_resilience", "resilience_gap", "regime_shift_risk"]].round(3))
    print(metrics.round(4))


if __name__ == "__main__":
    main()
