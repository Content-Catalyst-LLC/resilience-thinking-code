#!/usr/bin/env python3
"""
Advanced threshold and tipping-point workflow.

Uses pandas, numpy, matplotlib, scikit-learn, and joblib.

Run:
    pip install -r requirements-advanced.txt
    python python/system_thresholds_advanced.py
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
PROFILES_PATH = ROOT / "data" / "raw" / "threshold_system_profiles.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "threshold_scenarios.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_FIGURES = ROOT / "outputs" / "figures"
OUT_MODELS = ROOT / "outputs" / "models"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)
OUT_MODELS.mkdir(parents=True, exist_ok=True)

FEATURES = [
    "pressure",
    "feedback_strength",
    "disturbance_load",
    "adaptive_capacity",
    "system_memory",
    "recovery_speed",
    "exposure",
]


def score_profiles(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["threshold_risk_score"] = (
        0.24 * out["pressure"]
        + 0.22 * out["feedback_strength"]
        + 0.18 * out["disturbance_load"]
        + 0.14 * out["exposure"]
        - 0.10 * out["adaptive_capacity"]
        - 0.07 * out["system_memory"]
        - 0.05 * out["recovery_speed"]
    )
    out["threshold_protection_score"] = (
        0.30 * out["adaptive_capacity"]
        + 0.24 * out["system_memory"]
        + 0.22 * out["recovery_speed"]
        + 0.14 * (1 - out["feedback_strength"])
        + 0.10 * (1 - out["pressure"])
    )
    conditions = [
        out["threshold_risk_score"] >= 0.55,
        (out["recovery_speed"] < 0.38) | (out["adaptive_capacity"] < 0.46),
        out["feedback_strength"] >= 0.72,
    ]
    choices = [
        "high threshold-risk concern",
        "low recovery or adaptive-capacity concern",
        "feedback amplification concern",
    ]
    out["diagnostic"] = np.select(conditions, choices, default="mixed threshold profile requiring monitoring")
    return out


def update_state(x: float, pressure: float, r: float = 1.2, dt: float = 0.05) -> float:
    return x + dt * (r * x - x**3 + pressure)


def simulate_hysteresis(scenarios: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(42)
    threshold_rows = []
    warning_rows = []

    for _, scenario in scenarios.iterrows():
        steps = int(scenario["steps"])
        start = float(scenario["pressure_start"])
        end = float(scenario["pressure_end"])
        noise = float(scenario["noise_level"])

        forward_pressure = np.linspace(start, end, steps)
        backward_pressure = np.linspace(end, start, steps)

        x_forward = np.zeros(steps)
        x_forward[0] = -0.90

        for i in range(1, steps):
            x_forward[i] = update_state(x_forward[i - 1], forward_pressure[i]) + rng.normal(0.0, noise)

        forward = pd.DataFrame({
            "scenario_id": scenario["scenario_id"],
            "scenario_name": scenario["scenario_name"],
            "step": np.arange(1, steps + 1),
            "pressure": forward_pressure,
            "state": x_forward,
            "direction": "Increasing Pressure",
        })

        x_backward = np.zeros(steps)
        x_backward[0] = x_forward[-1]

        for i in range(1, steps):
            x_backward[i] = update_state(x_backward[i - 1], backward_pressure[i]) + rng.normal(0.0, noise)

        backward = pd.DataFrame({
            "scenario_id": scenario["scenario_id"],
            "scenario_name": scenario["scenario_name"],
            "step": np.arange(1, steps + 1),
            "pressure": backward_pressure,
            "state": x_backward,
            "direction": "Decreasing Pressure",
        })

        combined = pd.concat([forward, backward], ignore_index=True)
        combined["regime"] = np.where(combined["state"] >= 0, "upper regime", "lower regime")
        threshold_rows.append(combined)

        ew = forward.copy()
        ew["rolling_variance"] = ew["state"].rolling(window=16).var()
        ew["rolling_autocorr"] = ew["state"].rolling(window=16).apply(
            lambda x: pd.Series(x[:-1]).corr(pd.Series(x[1:])),
            raw=False,
        )
        ew["recovery_speed_proxy"] = 1 - ew["rolling_autocorr"]
        ew["threshold_proximity_score"] = (
            ew["rolling_variance"].rank(pct=True)
            + ew["rolling_autocorr"].rank(pct=True)
        ) / 2
        warning_rows.append(ew)

    return pd.concat(threshold_rows, ignore_index=True), pd.concat(warning_rows, ignore_index=True)


def expand_training(df: pd.DataFrame, n: int = 2400) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []

    for _ in range(n):
        base = df.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]
        record = {}

        for feature in FEATURES:
            record[feature] = float(np.clip(float(base[feature]) + rng.normal(0, 0.08), 0.03, 0.98))

        risk = (
            0.24 * record["pressure"]
            + 0.22 * record["feedback_strength"]
            + 0.18 * record["disturbance_load"]
            + 0.14 * record["exposure"]
            - 0.10 * record["adaptive_capacity"]
            - 0.07 * record["system_memory"]
            - 0.05 * record["recovery_speed"]
            + rng.normal(0, 0.035)
        )
        record["threshold_risk_score"] = risk
        record["threshold_risk"] = 1 if risk > 0.55 else 0
        rows.append(record)

    return pd.DataFrame(rows)


def plot_outputs(profiles: pd.DataFrame, threshold_df: pd.DataFrame, early_warning_df: pd.DataFrame) -> None:
    profile_plot = profiles[
        ["system_name", "threshold_risk_score", "threshold_protection_score", "pressure", "feedback_strength", "adaptive_capacity", "recovery_speed"]
    ].melt(id_vars="system_name", var_name="indicator", value_name="value")

    order = profiles.sort_values("threshold_risk_score")["system_name"].tolist()
    plt.figure(figsize=(10, 6))
    for indicator, subset in profile_plot.groupby("indicator"):
        y = [order.index(s) for s in subset["system_name"]]
        plt.scatter(subset["value"], y, label=indicator, s=50)
    plt.yticks(range(len(order)), order)
    plt.xlabel("Indicator value")
    plt.title("Threshold Risk and Protection Profiles")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "threshold_risk_profiles.png", dpi=160)
    plt.close()

    scenario = threshold_df["scenario_name"].iloc[0]
    subset = threshold_df[threshold_df["scenario_name"] == scenario]
    plt.figure(figsize=(10, 6))
    for direction in subset["direction"].unique():
        direction_subset = subset[subset["direction"] == direction]
        plt.plot(direction_subset["pressure"], direction_subset["state"], label=direction)
    plt.xlabel("External pressure")
    plt.ylabel("System state")
    plt.title("Threshold Crossing and Hysteresis")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "threshold_hysteresis_path.png", dpi=160)
    plt.close()

    ew_subset = early_warning_df[early_warning_df["scenario_name"] == scenario]
    plt.figure(figsize=(10, 6))
    plt.plot(ew_subset["step"], ew_subset["rolling_variance"], label="Rolling variance")
    plt.plot(ew_subset["step"], ew_subset["rolling_autocorr"], label="Rolling autocorrelation")
    plt.plot(ew_subset["step"], ew_subset["threshold_proximity_score"], label="Threshold proximity score")
    plt.xlabel("Step")
    plt.ylabel("Value")
    plt.title("Early Warning Indicators Before Critical Transition")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "early_warning_indicators.png", dpi=160)
    plt.close()


def main() -> None:
    raw_profiles = pd.read_csv(PROFILES_PATH)
    scenarios = pd.read_csv(SCENARIOS_PATH)

    profiles = score_profiles(raw_profiles)
    threshold_df, early_warning_df = simulate_hysteresis(scenarios)

    profiles.to_csv(OUT_TABLES / "threshold_system_profiles_advanced.csv", index=False)
    threshold_df.to_csv(OUT_TABLES / "threshold_hysteresis_simulation_advanced.csv", index=False)
    early_warning_df.to_csv(OUT_TABLES / "threshold_early_warning_signals_advanced.csv", index=False)

    scenario_summary = (
        threshold_df.groupby(["scenario_id", "scenario_name"])
        .agg(
            maximum_state=("state", "max"),
            minimum_state=("state", "min"),
            mean_state=("state", "mean"),
            upper_regime_steps=("regime", lambda x: (x == "upper regime").sum()),
            lower_regime_steps=("regime", lambda x: (x == "lower regime").sum()),
        )
        .reset_index()
    )
    scenario_summary.to_csv(OUT_TABLES / "threshold_scenario_summary_advanced.csv", index=False)

    plot_outputs(profiles, threshold_df, early_warning_df)

    training = expand_training(raw_profiles)
    X = training[FEATURES]
    y = training["threshold_risk"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=450,
        min_samples_leaf=6,
        class_weight="balanced",
        random_state=42,
    )
    model.fit(X_train, y_train)

    prob = model.predict_proba(X_test)[:, 1]
    pred = (prob >= 0.50).astype(int)

    metrics = pd.DataFrame(
        [{
            "model": "random_forest_threshold_risk_classifier",
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

    training.to_csv(OUT_TABLES / "synthetic_threshold_risk_training_data.csv", index=False)
    metrics.to_csv(OUT_TABLES / "advanced_threshold_risk_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "threshold_risk_classifier.joblib")

    plt.figure(figsize=(10, 6))
    plt.barh(importance["feature"], importance["importance"])
    plt.gca().invert_yaxis()
    plt.xlabel("Importance")
    plt.title("Feature Importance for Threshold-Risk Classification")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "advanced_feature_importance.png", dpi=160)
    plt.close()

    print("Advanced system thresholds workflow complete.")
    print(profiles[["system_name", "threshold_risk_score", "threshold_protection_score", "diagnostic"]].round(3))
    print(metrics.round(4))


if __name__ == "__main__":
    main()
