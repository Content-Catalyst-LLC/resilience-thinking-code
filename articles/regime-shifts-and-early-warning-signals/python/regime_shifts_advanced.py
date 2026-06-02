#!/usr/bin/env python3
"""
Advanced regime-shift and early-warning workflow.

Uses pandas, numpy, matplotlib, scikit-learn, and joblib.

Run:
    pip install -r requirements-advanced.txt
    python python/regime_shifts_advanced.py
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
PROFILES_PATH = ROOT / "data" / "raw" / "regime_system_profiles.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "regime_scenarios.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_FIGURES = ROOT / "outputs" / "figures"
OUT_MODELS = ROOT / "outputs" / "models"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)
OUT_MODELS.mkdir(parents=True, exist_ok=True)

FEATURES = [
    "pressure",
    "feedback_strength",
    "variance_signal",
    "autocorr_signal",
    "recovery_speed",
    "adaptive_capacity",
    "system_memory",
    "monitoring_quality",
    "justice_visibility",
    "exposure",
]


def score_profiles(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["regime_risk_score"] = np.clip(
        0.18 * out["pressure"]
        + 0.17 * out["feedback_strength"]
        + 0.15 * out["variance_signal"]
        + 0.15 * out["autocorr_signal"]
        + 0.12 * out["exposure"]
        - 0.08 * out["recovery_speed"]
        - 0.06 * out["adaptive_capacity"]
        - 0.04 * out["system_memory"]
        - 0.03 * out["monitoring_quality"]
        - 0.02 * out["justice_visibility"],
        0,
        1,
    )
    out["threshold_protection_score"] = np.clip(
        0.22 * out["recovery_speed"]
        + 0.20 * out["adaptive_capacity"]
        + 0.18 * out["system_memory"]
        + 0.16 * out["monitoring_quality"]
        + 0.12 * out["justice_visibility"]
        + 0.12 * (1 - out["feedback_strength"]),
        0,
        1,
    )

    conditions = [
        out["regime_risk_score"] >= 0.55,
        out["recovery_speed"] < 0.38,
        out["monitoring_quality"] < 0.50,
        out["justice_visibility"] < 0.45,
    ]
    choices = [
        "high regime-shift risk concern",
        "critical slowing and weak recovery concern",
        "monitoring quality concern",
        "unequal warning and justice visibility concern",
    ]
    out["diagnostic"] = np.select(conditions, choices, default="mixed regime profile requiring monitoring")
    return out


def update_state(x: float, pressure: float, r: float = 1.2, dt: float = 0.05) -> float:
    return x + dt * (r * x - x**3 + pressure)


def lag1_autocorr(values):
    values = np.asarray(values)
    if len(values) < 3:
        return np.nan
    return pd.Series(values[:-1]).corr(pd.Series(values[1:]))


def simulate_scenarios(scenarios: pd.DataFrame) -> pd.DataFrame:
    all_rows = []

    for _, scenario in scenarios.iterrows():
        seed = 42 + int(str(scenario["scenario_id"])[-1])
        rng = np.random.default_rng(seed)
        steps = int(scenario["steps"])
        pressure_start = float(scenario["pressure_start"])
        pressure_end = float(scenario["pressure_end"])
        noise = float(scenario["noise_level"])
        intervention = float(scenario["adaptive_intervention"])

        pressure_base = np.linspace(pressure_start, pressure_end, steps)
        intervention_path = intervention * np.minimum(1.0, np.arange(1, steps + 1) / steps)
        pressure = pressure_base - 0.18 * intervention_path

        state = np.zeros(steps)
        state[0] = -0.90

        for t in range(1, steps):
            state[t] = update_state(state[t - 1], pressure[t]) + rng.normal(0.0, noise)

        df = pd.DataFrame(
            {
                "scenario_id": scenario["scenario_id"],
                "scenario_name": scenario["scenario_name"],
                "time": np.arange(1, steps + 1),
                "pressure": pressure,
                "state": state,
                "monitoring_quality": float(scenario["monitoring_quality"]),
            }
        )

        df["regime"] = np.where(df["state"] >= 0, "upper regime", "lower regime")
        df["rolling_variance"] = df["state"].rolling(window=18).var()
        df["rolling_autocorr"] = df["state"].rolling(window=18).apply(lag1_autocorr, raw=False)
        df["recovery_speed_proxy"] = 1 - df["rolling_autocorr"]
        df["threshold_proximity_score"] = (
            df["rolling_variance"].rank(pct=True)
            + df["rolling_autocorr"].rank(pct=True)
        ) / 2

        all_rows.append(df)

    return pd.concat(all_rows, ignore_index=True)


def expand_training(df: pd.DataFrame, n: int = 2600) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []

    for _ in range(n):
        base = df.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]
        record = {}

        for feature in FEATURES:
            record[feature] = float(np.clip(float(base[feature]) + rng.normal(0, 0.075), 0.02, 0.98))

        risk = (
            0.18 * record["pressure"]
            + 0.17 * record["feedback_strength"]
            + 0.15 * record["variance_signal"]
            + 0.15 * record["autocorr_signal"]
            + 0.12 * record["exposure"]
            - 0.08 * record["recovery_speed"]
            - 0.06 * record["adaptive_capacity"]
            - 0.04 * record["system_memory"]
            - 0.03 * record["monitoring_quality"]
            - 0.02 * record["justice_visibility"]
            + rng.normal(0, 0.035)
        )

        record["regime_risk_score"] = risk
        record["high_regime_shift_risk"] = 1 if risk >= 0.55 or record["recovery_speed"] < 0.34 else 0
        rows.append(record)

    return pd.DataFrame(rows)


def plot_outputs(profiles: pd.DataFrame, sim: pd.DataFrame) -> None:
    profile_plot = profiles[
        [
            "system_name",
            "regime_risk_score",
            "threshold_protection_score",
            "pressure",
            "feedback_strength",
            "variance_signal",
            "autocorr_signal",
            "recovery_speed",
            "adaptive_capacity",
        ]
    ].melt(id_vars="system_name", var_name="indicator", value_name="value")

    order = profiles.sort_values("regime_risk_score")["system_name"].tolist()
    plt.figure(figsize=(10, 6))
    for indicator, subset in profile_plot.groupby("indicator"):
        y = [order.index(s) for s in subset["system_name"]]
        plt.scatter(subset["value"], y, label=indicator, s=50)
    plt.yticks(range(len(order)), order)
    plt.xlabel("Indicator value")
    plt.title("Regime-Shift Risk and Protection Profiles")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "regime_shift_risk_profiles.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    for scenario_name in sim["scenario_name"].unique():
        subset = sim[sim["scenario_name"] == scenario_name]
        plt.plot(subset["pressure"], subset["state"], label=scenario_name)
    plt.xlabel("External pressure")
    plt.ylabel("System state")
    plt.title("Regime-Shift Trajectories Across Scenarios")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "regime_shift_trajectories.png", dpi=160)
    plt.close()

    selected = sim[sim["scenario_name"] == "Gradual pressure and moderate noise"]
    plt.figure(figsize=(10, 6))
    plt.plot(selected["time"], selected["rolling_variance"], label="Rolling variance")
    plt.plot(selected["time"], selected["rolling_autocorr"], label="Lag-1 autocorrelation")
    plt.plot(selected["time"], selected["threshold_proximity_score"], label="Threshold proximity score")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title("Early Warning Indicators Before Regime Shift")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "early_warning_indicators.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(selected["time"], selected["recovery_speed_proxy"])
    plt.xlabel("Time")
    plt.ylabel("Recovery speed proxy")
    plt.title("Recovery Speed Proxy Under Critical Slowing Down")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "recovery_speed_proxy.png", dpi=160)
    plt.close()


def main() -> None:
    raw_profiles = pd.read_csv(PROFILES_PATH)
    scenarios = pd.read_csv(SCENARIOS_PATH)

    profiles = score_profiles(raw_profiles)
    sim = simulate_scenarios(scenarios)

    profiles.to_csv(OUT_TABLES / "regime_system_profiles_advanced.csv", index=False)
    sim.to_csv(OUT_TABLES / "regime_shift_early_warning_simulation_advanced.csv", index=False)

    summary_rows = []
    for scenario_name, subset in sim.groupby("scenario_name"):
        upper = subset[subset["regime"] == "upper regime"]
        summary_rows.append(
            {
                "scenario_name": scenario_name,
                "transition_time": upper["time"].iloc[0] if not upper.empty else np.nan,
                "max_rolling_variance": subset["rolling_variance"].max(),
                "max_rolling_autocorr": subset["rolling_autocorr"].max(),
                "min_recovery_speed_proxy": subset["recovery_speed_proxy"].min(),
                "max_threshold_proximity_score": subset["threshold_proximity_score"].max(),
                "monitoring_quality": subset["monitoring_quality"].iloc[0],
            }
        )

    summary = pd.DataFrame(summary_rows)
    summary.to_csv(OUT_TABLES / "regime_shift_scenario_summary_advanced.csv", index=False)

    plot_outputs(profiles, sim)

    training = expand_training(raw_profiles)
    X = training[FEATURES]
    y = training["high_regime_shift_risk"]

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
            "model": "random_forest_regime_shift_risk_classifier",
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

    training.to_csv(OUT_TABLES / "synthetic_regime_shift_risk_training_data.csv", index=False)
    metrics.to_csv(OUT_TABLES / "advanced_regime_shift_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "regime_shift_risk_classifier.joblib")

    plt.figure(figsize=(10, 6))
    plt.barh(importance["feature"], importance["importance"])
    plt.gca().invert_yaxis()
    plt.xlabel("Importance")
    plt.title("Feature Importance for Regime-Shift Risk Classification")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "advanced_feature_importance.png", dpi=160)
    plt.close()

    print("Advanced regime shifts workflow complete.")
    print(profiles[["system_name", "regime_risk_score", "threshold_protection_score", "diagnostic"]].round(4))
    print(metrics.round(4))


if __name__ == "__main__":
    main()
