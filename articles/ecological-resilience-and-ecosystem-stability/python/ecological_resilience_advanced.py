#!/usr/bin/env python3
"""
Advanced ecological resilience workflow.

Run:
    pip install -r requirements-advanced.txt
    python python/ecological_resilience_advanced.py
"""

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
PROFILES_PATH = ROOT / "data" / "raw" / "ecosystem_resilience_profiles.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_FIGURES = ROOT / "outputs" / "figures"
OUT_MODELS = ROOT / "outputs" / "models"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)
OUT_MODELS.mkdir(parents=True, exist_ok=True)

FEATURES = [
    "short_run_stability",
    "biodiversity",
    "functional_diversity",
    "response_diversity",
    "threshold_distance",
    "basin_width",
    "regenerative_capacity",
    "ecological_memory",
    "connectivity",
    "disturbance_exposure",
    "slow_variable_pressure",
]


def score_profiles(df):
    out = df.copy()
    out["stability_score"] = out["short_run_stability"]
    out["ecological_resilience_profile"] = (
        0.11 * out["short_run_stability"]
        + 0.13 * out["biodiversity"]
        + 0.13 * out["functional_diversity"]
        + 0.13 * out["response_diversity"]
        + 0.16 * out["threshold_distance"]
        + 0.14 * out["basin_width"]
        + 0.12 * out["regenerative_capacity"]
        + 0.10 * out["ecological_memory"]
        + 0.08 * out["connectivity"]
        - 0.06 * out["disturbance_exposure"]
        - 0.06 * out["slow_variable_pressure"]
    )
    out["threshold_risk_index"] = np.clip(
        0.30 * (1 - out["threshold_distance"])
        + 0.25 * (1 - out["basin_width"])
        + 0.20 * out["disturbance_exposure"]
        + 0.18 * out["slow_variable_pressure"]
        - 0.15 * out["regenerative_capacity"]
        - 0.12 * out["response_diversity"],
        0,
        1,
    )
    return out


def main():
    raw = pd.read_csv(PROFILES_PATH)
    profiles = score_profiles(raw)
    profiles.to_csv(OUT_TABLES / "ecosystem_resilience_profiles_advanced.csv", index=False)

    plot_df = profiles[["ecosystem_type", "stability_score", "ecological_resilience_profile", "threshold_risk_index"]].melt(
        id_vars="ecosystem_type",
        var_name="indicator",
        value_name="value",
    )

    order = profiles.sort_values("ecological_resilience_profile")["ecosystem_type"].tolist()
    plt.figure(figsize=(10, 6))
    for indicator, subset in plot_df.groupby("indicator"):
        y = [order.index(e) for e in subset["ecosystem_type"]]
        plt.scatter(subset["value"], y, label=indicator, s=60)
    plt.yticks(range(len(order)), order)
    plt.xlabel("Indicator value")
    plt.title("Ecosystem Stability and Ecological Resilience Profiles")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "ecosystem_stability_resilience_profiles.png", dpi=160)
    plt.close()

    rng = np.random.default_rng(42)
    rows = []
    for _ in range(1800):
        base = raw.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]
        record = {}
        for feature in FEATURES:
            record[feature] = float(np.clip(float(base[feature]) + rng.normal(0, 0.08), 0.05, 0.98))
        risk = (
            0.30 * (1 - record["threshold_distance"])
            + 0.25 * (1 - record["basin_width"])
            + 0.20 * record["disturbance_exposure"]
            + 0.18 * record["slow_variable_pressure"]
            - 0.15 * record["regenerative_capacity"]
            - 0.12 * record["response_diversity"]
            + rng.normal(0, 0.04)
        )
        record["threshold_risk"] = 1 if risk > 0.46 else 0
        rows.append(record)

    training = pd.DataFrame(rows)
    X = training[FEATURES]
    y = training["threshold_risk"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

    model = RandomForestClassifier(n_estimators=350, min_samples_leaf=6, class_weight="balanced", random_state=42)
    model.fit(X_train, y_train)
    prob = model.predict_proba(X_test)[:, 1]
    pred = (prob >= 0.50).astype(int)

    metrics = pd.DataFrame([{
        "model": "random_forest_ecological_threshold_risk_classifier",
        "accuracy": accuracy_score(y_test, pred),
        "precision": precision_score(y_test, pred, zero_division=0),
        "recall": recall_score(y_test, pred, zero_division=0),
        "f1": f1_score(y_test, pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, prob),
        "brier_score": brier_score_loss(y_test, prob),
    }])

    importance = pd.DataFrame({"feature": FEATURES, "importance": model.feature_importances_}).sort_values("importance", ascending=False)

    training.to_csv(OUT_TABLES / "synthetic_ecological_threshold_training_data.csv", index=False)
    metrics.to_csv(OUT_TABLES / "advanced_ecological_threshold_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "ecological_threshold_risk_classifier.joblib")

    print("Advanced ecological resilience workflow complete.")
    print(metrics.round(4))


if __name__ == "__main__":
    main()
