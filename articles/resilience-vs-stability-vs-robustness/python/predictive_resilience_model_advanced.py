#!/usr/bin/env python3
"""
Advanced predictive resilience model.

This pipeline uses pandas, scikit-learn, matplotlib, and joblib.

Run:
    pip install -r requirements-advanced.txt
    python python/predictive_resilience_model_advanced.py

Outputs:
    outputs/models/resilience_failure_random_forest.joblib
    outputs/tables/advanced_model_metrics.csv
    outputs/tables/advanced_feature_importance.csv
    outputs/tables/advanced_scenario_predictions.csv
    outputs/figures/advanced_feature_importance.png
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
    from sklearn.compose import ColumnTransformer
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.impute import SimpleImputer
    from sklearn.metrics import (
        accuracy_score,
        brier_score_loss,
        classification_report,
        confusion_matrix,
        f1_score,
        precision_score,
        recall_score,
        roc_auc_score,
    )
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
except ImportError as exc:
    raise SystemExit(
        "Missing advanced dependency. Run: pip install -r requirements-advanced.txt"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_FIGURES = ROOT / "outputs" / "figures"
OUT_MODELS = ROOT / "outputs" / "models"
DATA_PROCESSED = ROOT / "data" / "processed"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)
OUT_MODELS.mkdir(parents=True, exist_ok=True)

FEATURES = [
    "equilibrium_return",
    "stress_tolerance",
    "adaptive_capacity",
    "threshold_distance",
    "learning_capacity",
    "redundancy",
    "modularity",
    "exposure",
    "sensitivity",
    "dependency_concentration",
    "shock_intensity",
    "shock_frequency",
    "compound_disturbance_index",
]


def ensure_training_data() -> Path:
    path = DATA_PROCESSED / "synthetic_resilience_training_data.csv"
    if not path.exists():
        subprocess.run(
            [sys.executable, str(ROOT / "python" / "predictive_resilience_model_standard.py")],
            check=True,
        )
    return path


def scenario_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "scenario_name": "Stable but brittle institution",
                "equilibrium_return": 0.90,
                "stress_tolerance": 0.55,
                "adaptive_capacity": 0.28,
                "threshold_distance": 0.32,
                "learning_capacity": 0.24,
                "redundancy": 0.35,
                "modularity": 0.34,
                "exposure": 0.64,
                "sensitivity": 0.62,
                "dependency_concentration": 0.75,
                "shock_intensity": 0.45,
                "shock_frequency": 7,
                "compound_disturbance_index": 0.55,
            },
            {
                "scenario_name": "Robust but inflexible infrastructure",
                "equilibrium_return": 0.68,
                "stress_tolerance": 0.90,
                "adaptive_capacity": 0.38,
                "threshold_distance": 0.46,
                "learning_capacity": 0.33,
                "redundancy": 0.60,
                "modularity": 0.43,
                "exposure": 0.70,
                "sensitivity": 0.58,
                "dependency_concentration": 0.68,
                "shock_intensity": 0.52,
                "shock_frequency": 8,
                "compound_disturbance_index": 0.62,
            },
            {
                "scenario_name": "Adaptive resilient system",
                "equilibrium_return": 0.56,
                "stress_tolerance": 0.72,
                "adaptive_capacity": 0.88,
                "threshold_distance": 0.80,
                "learning_capacity": 0.86,
                "redundancy": 0.73,
                "modularity": 0.70,
                "exposure": 0.52,
                "sensitivity": 0.46,
                "dependency_concentration": 0.40,
                "shock_intensity": 0.50,
                "shock_frequency": 8,
                "compound_disturbance_index": 0.54,
            },
        ]
    )


def main() -> None:
    data_path = ensure_training_data()
    df = pd.read_csv(data_path)

    X = df[FEATURES]
    y = df["resilience_failure_risk"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, FEATURES),
        ]
    )

    models = {
        "random_forest": RandomForestClassifier(
            n_estimators=350,
            min_samples_leaf=8,
            max_depth=None,
            class_weight="balanced",
            random_state=42,
        ),
        "gradient_boosting": GradientBoostingClassifier(random_state=42),
    }

    metric_rows = []
    fitted_models = {}

    for model_name, estimator in models.items():
        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", estimator),
            ]
        )

        pipeline.fit(X_train, y_train)
        y_prob = pipeline.predict_proba(X_test)[:, 1]
        y_pred = (y_prob >= 0.50).astype(int)

        metric_rows.append(
            {
                "model": model_name,
                "accuracy": accuracy_score(y_test, y_pred),
                "precision": precision_score(y_test, y_pred, zero_division=0),
                "recall": recall_score(y_test, y_pred, zero_division=0),
                "f1": f1_score(y_test, y_pred, zero_division=0),
                "roc_auc": roc_auc_score(y_test, y_prob),
                "brier_score": brier_score_loss(y_test, y_prob),
                "true_negative": confusion_matrix(y_test, y_pred).ravel()[0],
                "false_positive": confusion_matrix(y_test, y_pred).ravel()[1],
                "false_negative": confusion_matrix(y_test, y_pred).ravel()[2],
                "true_positive": confusion_matrix(y_test, y_pred).ravel()[3],
            }
        )

        fitted_models[model_name] = pipeline

    metrics = pd.DataFrame(metric_rows).sort_values("roc_auc", ascending=False)
    metrics.to_csv(OUT_TABLES / "advanced_model_metrics.csv", index=False)

    best_name = metrics.iloc[0]["model"]
    best_model = fitted_models[best_name]
    joblib.dump(best_model, OUT_MODELS / "resilience_failure_predictive_model.joblib")

    model_step = best_model.named_steps["model"]
    if hasattr(model_step, "feature_importances_"):
        importance = pd.DataFrame(
            {
                "feature": FEATURES,
                "importance": model_step.feature_importances_,
            }
        ).sort_values("importance", ascending=False)

        importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)

        plt.figure(figsize=(10, 6))
        plt.barh(importance["feature"], importance["importance"])
        plt.gca().invert_yaxis()
        plt.xlabel("Importance")
        plt.title(f"Feature Importance: {best_name}")
        plt.tight_layout()
        plt.savefig(OUT_FIGURES / "advanced_feature_importance.png", dpi=160)
        plt.close()

    scenarios = scenario_frame()
    scenario_prob = best_model.predict_proba(scenarios[FEATURES])[:, 1]
    scenarios["predicted_failure_probability"] = scenario_prob
    scenarios["prediction_band"] = pd.cut(
        scenarios["predicted_failure_probability"],
        bins=[-0.01, 0.35, 0.65, 1.01],
        labels=[
            "lower predicted resilience failure risk",
            "moderate predicted resilience failure risk",
            "high predicted resilience failure risk",
        ],
    )

    scenarios.to_csv(OUT_TABLES / "advanced_scenario_predictions.csv", index=False)

    print("Advanced predictive resilience model complete.")
    print(metrics.round(4))
    print("\nScenario predictions:")
    print(scenarios[["scenario_name", "predicted_failure_probability", "prediction_band"]].round(4))


if __name__ == "__main__":
    main()
