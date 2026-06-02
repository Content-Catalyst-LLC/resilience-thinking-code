#!/usr/bin/env python3
"""
Advanced slow-variable and hidden-system-change workflow.

Uses pandas, numpy, matplotlib, scikit-learn, and joblib.

Run:
    pip install -r requirements-advanced.txt
    python python/slow_variables_advanced.py
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
PROFILES_PATH = ROOT / "data" / "raw" / "slow_variable_profiles.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "slow_variable_scenarios.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_FIGURES = ROOT / "outputs" / "figures"
OUT_MODELS = ROOT / "outputs" / "models"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)
OUT_MODELS.mkdir(parents=True, exist_ok=True)

FEATURES = [
    "maintenance_backlog",
    "public_trust",
    "ecological_memory",
    "climate_pressure",
    "adaptive_capacity",
    "system_memory",
    "monitoring_quality",
    "justice_visibility",
    "exposure",
]


def score_profiles(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    out["hidden_risk_score"] = np.clip(
        0.20 * out["maintenance_backlog"]
        + 0.18 * out["climate_pressure"]
        + 0.16 * out["exposure"]
        + 0.12 * (1 - out["public_trust"])
        + 0.12 * (1 - out["ecological_memory"])
        + 0.10 * (1 - out["adaptive_capacity"])
        + 0.07 * (1 - out["monitoring_quality"])
        + 0.05 * (1 - out["justice_visibility"]),
        0,
        1,
    )

    out["threshold_distance"] = np.clip(
        1
        - 0.26 * out["maintenance_backlog"]
        - 0.24 * out["climate_pressure"]
        - 0.16 * out["exposure"]
        - 0.12 * (1 - out["public_trust"])
        - 0.12 * (1 - out["ecological_memory"])
        - 0.10 * (1 - out["adaptive_capacity"]),
        0,
        1,
    )

    conditions = [
        (out["hidden_risk_score"] >= 0.58) & (out["threshold_distance"] <= 0.45),
        out["monitoring_quality"] < 0.50,
        out["justice_visibility"] < 0.45,
        out["adaptive_capacity"] < 0.48,
    ]
    choices = [
        "high hidden-risk and narrowing threshold-distance concern",
        "monitoring and signal-quality concern",
        "justice visibility and slow-harm concern",
        "adaptive-capacity concern",
    ]
    out["diagnostic"] = np.select(conditions, choices, default="mixed slow-variable profile requiring monitoring")
    return out


def simulate_scenarios(scenarios: pd.DataFrame, steps: int = 120) -> pd.DataFrame:
    rows = []

    for _, scenario in scenarios.iterrows():
        maintenance_backlog = 0.25
        public_trust = 0.72
        ecological_memory = 0.68
        climate_pressure = 0.22
        system_memory = 0.60
        monitoring_quality = 0.54
        justice_visibility = 0.48
        system_function = 0.86

        for t in range(1, steps + 1):
            adaptive_investment = float(scenario["adaptive_investment"])
            monitoring_improvement = float(scenario["monitoring_improvement"])
            justice_improvement = float(scenario["justice_improvement"])

            maintenance_backlog = np.clip(
                maintenance_backlog
                + float(scenario["maintenance_growth"])
                - 0.006 * adaptive_investment,
                0,
                1,
            )
            public_trust = np.clip(
                public_trust
                - float(scenario["trust_decline"])
                + 0.007 * adaptive_investment,
                0,
                1,
            )
            ecological_memory = np.clip(
                ecological_memory
                - float(scenario["memory_decline"])
                + 0.005 * adaptive_investment,
                0,
                1,
            )
            climate_pressure = np.clip(
                climate_pressure + float(scenario["climate_growth"]),
                0,
                1,
            )
            monitoring_quality = np.clip(
                monitoring_quality + monitoring_improvement + 0.002 * adaptive_investment,
                0,
                1,
            )
            justice_visibility = np.clip(
                justice_visibility + justice_improvement + 0.0015 * adaptive_investment,
                0,
                1,
            )
            system_memory = np.clip(
                system_memory
                + 0.004 * monitoring_quality
                + 0.003 * public_trust
                - 0.002 * climate_pressure,
                0,
                1,
            )

            adaptive_capacity = np.clip(
                0.26 * public_trust
                + 0.22 * ecological_memory
                + 0.18 * (1 - maintenance_backlog)
                + 0.14 * (1 - climate_pressure)
                + 0.10 * system_memory
                + 0.06 * monitoring_quality
                + 0.04 * justice_visibility,
                0,
                1,
            )

            threshold_distance = np.clip(
                1
                - 0.30 * maintenance_backlog
                - 0.26 * climate_pressure
                - 0.18 * (1 - public_trust)
                - 0.16 * (1 - ecological_memory)
                - 0.10 * (1 - adaptive_capacity),
                0,
                1,
            )

            hidden_risk = np.clip(
                0.28 * maintenance_backlog
                + 0.26 * climate_pressure
                + 0.18 * (1 - public_trust)
                + 0.14 * (1 - ecological_memory)
                + 0.08 * (1 - monitoring_quality)
                + 0.06 * (1 - justice_visibility),
                0,
                1,
            )

            fast_shock = (
                float(scenario["shock_magnitude"])
                if t in [int(scenario["shock_time_1"]), int(scenario["shock_time_2"])]
                else 0.0
            )

            system_function = np.clip(
                system_function
                - 0.22 * hidden_risk
                - 0.46 * fast_shock
                + 0.18 * adaptive_capacity
                + 0.04 * system_memory,
                0,
                1,
            )

            rows.append(
                {
                    "scenario_id": scenario["scenario_id"],
                    "scenario_name": scenario["scenario_name"],
                    "time": t,
                    "maintenance_backlog": maintenance_backlog,
                    "public_trust": public_trust,
                    "ecological_memory": ecological_memory,
                    "climate_pressure": climate_pressure,
                    "system_memory": system_memory,
                    "monitoring_quality": monitoring_quality,
                    "justice_visibility": justice_visibility,
                    "adaptive_capacity": adaptive_capacity,
                    "threshold_distance": threshold_distance,
                    "hidden_risk": hidden_risk,
                    "fast_shock": fast_shock,
                    "system_function": system_function,
                }
            )

    return pd.DataFrame(rows)


def expand_training(df: pd.DataFrame, n: int = 2400) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []

    for _ in range(n):
        base = df.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]
        record = {}

        for feature in FEATURES:
            record[feature] = float(np.clip(float(base[feature]) + rng.normal(0, 0.08), 0.02, 0.98))

        risk = (
            0.20 * record["maintenance_backlog"]
            + 0.18 * record["climate_pressure"]
            + 0.16 * record["exposure"]
            + 0.12 * (1 - record["public_trust"])
            + 0.12 * (1 - record["ecological_memory"])
            + 0.10 * (1 - record["adaptive_capacity"])
            + 0.07 * (1 - record["monitoring_quality"])
            + 0.05 * (1 - record["justice_visibility"])
            + rng.normal(0, 0.035)
        )

        distance = (
            1
            - 0.26 * record["maintenance_backlog"]
            - 0.24 * record["climate_pressure"]
            - 0.16 * record["exposure"]
            - 0.12 * (1 - record["public_trust"])
            - 0.12 * (1 - record["ecological_memory"])
            - 0.10 * (1 - record["adaptive_capacity"])
        )

        record["hidden_risk_score"] = risk
        record["threshold_distance"] = distance
        record["high_hidden_risk"] = 1 if risk >= 0.58 or distance <= 0.42 else 0
        rows.append(record)

    return pd.DataFrame(rows)


def plot_outputs(profiles: pd.DataFrame, simulation: pd.DataFrame) -> None:
    profile_plot = profiles[
        [
            "system_name",
            "hidden_risk_score",
            "threshold_distance",
            "maintenance_backlog",
            "climate_pressure",
            "adaptive_capacity",
            "monitoring_quality",
            "justice_visibility",
        ]
    ].melt(id_vars="system_name", var_name="indicator", value_name="value")

    order = profiles.sort_values("hidden_risk_score")["system_name"].tolist()
    plt.figure(figsize=(10, 6))
    for indicator, subset in profile_plot.groupby("indicator"):
        y = [order.index(s) for s in subset["system_name"]]
        plt.scatter(subset["value"], y, label=indicator, s=50)
    plt.yticks(range(len(order)), order)
    plt.xlabel("Indicator value")
    plt.title("Slow-Variable Hidden Risk and Threshold Distance")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "slow_variable_risk_profiles.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    for scenario_name in simulation["scenario_name"].unique():
        subset = simulation[simulation["scenario_name"] == scenario_name]
        plt.plot(subset["time"], subset["hidden_risk"], label=scenario_name)
    plt.xlabel("Time")
    plt.ylabel("Hidden risk")
    plt.title("Hidden Risk Across Slow-Variable Scenarios")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "hidden_risk_scenarios.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    for scenario_name in simulation["scenario_name"].unique():
        subset = simulation[simulation["scenario_name"] == scenario_name]
        plt.plot(subset["time"], subset["threshold_distance"], label=scenario_name)
    plt.xlabel("Time")
    plt.ylabel("Threshold distance")
    plt.title("Threshold Distance Across Slow-Variable Scenarios")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "threshold_distance_scenarios.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    for scenario_name in simulation["scenario_name"].unique():
        subset = simulation[simulation["scenario_name"] == scenario_name]
        plt.plot(subset["time"], subset["system_function"], label=scenario_name)
    plt.xlabel("Time")
    plt.ylabel("System function")
    plt.title("System Function Under Fast Shocks and Slow Change")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "system_function_fast_shocks.png", dpi=160)
    plt.close()


def main() -> None:
    raw_profiles = pd.read_csv(PROFILES_PATH)
    scenarios = pd.read_csv(SCENARIOS_PATH)

    profiles = score_profiles(raw_profiles)
    simulation = simulate_scenarios(scenarios)

    profiles.to_csv(OUT_TABLES / "slow_variable_profiles_advanced.csv", index=False)
    simulation.to_csv(OUT_TABLES / "slow_variables_hidden_change_simulation_advanced.csv", index=False)

    summary = (
        simulation.groupby(["scenario_id", "scenario_name"])
        .agg(
            final_system_function=("system_function", "last"),
            minimum_threshold_distance=("threshold_distance", "min"),
            maximum_hidden_risk=("hidden_risk", "max"),
            final_adaptive_capacity=("adaptive_capacity", "last"),
            final_monitoring_quality=("monitoring_quality", "last"),
            final_justice_visibility=("justice_visibility", "last"),
            shock_count=("fast_shock", lambda x: (x > 0).sum()),
        )
        .reset_index()
    )
    summary.to_csv(OUT_TABLES / "slow_variables_scenario_summary_advanced.csv", index=False)

    plot_outputs(profiles, simulation)

    training = expand_training(raw_profiles)
    X = training[FEATURES]
    y = training["high_hidden_risk"]

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
            "model": "random_forest_hidden_slow_variable_risk_classifier",
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

    training.to_csv(OUT_TABLES / "synthetic_hidden_risk_training_data.csv", index=False)
    metrics.to_csv(OUT_TABLES / "advanced_hidden_risk_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "hidden_slow_variable_risk_classifier.joblib")

    plt.figure(figsize=(10, 6))
    plt.barh(importance["feature"], importance["importance"])
    plt.gca().invert_yaxis()
    plt.xlabel("Importance")
    plt.title("Feature Importance for Hidden Slow-Variable Risk")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "advanced_feature_importance.png", dpi=160)
    plt.close()

    print("Advanced slow variables workflow complete.")
    print(profiles[["system_name", "hidden_risk_score", "threshold_distance", "diagnostic"]].round(4))
    print(metrics.round(4))


if __name__ == "__main__":
    main()
