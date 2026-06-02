#!/usr/bin/env python3
"""
Advanced landscape resilience workflow.

Uses pandas, numpy, matplotlib, scikit-learn, and joblib.

Run:
    pip install -r requirements-advanced.txt
    python python/landscape_resilience_advanced.py
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
PROFILES_PATH = ROOT / "data" / "raw" / "landscape_resilience_profiles.csv"
PATCHES_PATH = ROOT / "data" / "raw" / "landscape_patch_table.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "disturbance_regime_scenarios.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_FIGURES = ROOT / "outputs" / "figures"
OUT_MODELS = ROOT / "outputs" / "models"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)
OUT_MODELS.mkdir(parents=True, exist_ok=True)

FEATURES = [
    "spatial_heterogeneity",
    "viable_connectivity",
    "refugia_capacity",
    "ecological_memory",
    "disturbance_pressure",
    "fragmentation",
    "governance_capacity",
    "social_vulnerability",
]


def score_profiles(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["landscape_resilience_profile"] = (
        0.17 * out["spatial_heterogeneity"]
        + 0.15 * out["viable_connectivity"]
        + 0.17 * out["refugia_capacity"]
        + 0.17 * out["ecological_memory"]
        + 0.14 * out["governance_capacity"]
        - 0.11 * out["disturbance_pressure"]
        - 0.06 * out["fragmentation"]
        - 0.06 * out["social_vulnerability"]
    )
    out["disturbance_risk_index"] = (
        0.28 * out["disturbance_pressure"]
        + 0.20 * out["fragmentation"]
        + 0.18 * out["social_vulnerability"]
        + 0.14 * (1 - out["refugia_capacity"])
        + 0.10 * (1 - out["ecological_memory"])
        + 0.10 * (1 - out["governance_capacity"])
    )
    return out


def simulate_patches(patches: pd.DataFrame, scenarios: pd.DataFrame, steps: int = 80) -> pd.DataFrame:
    rows = []

    for _, scenario in scenarios.iterrows():
        state = patches.copy()
        state["condition"] = state["condition"].astype(float)
        state["disturbance"] = 0.08 + 0.10 * state["exposure"].astype(float)

        n = len(state)
        base_connectivity = np.zeros((n, n))
        weights = state["connectivity_weight"].astype(float).to_numpy()

        for i in range(n):
            base_connectivity[i, (i - 1) % n] = 0.5 * weights[i]
            base_connectivity[i, (i + 1) % n] = 0.5 * weights[i]

        for t in range(1, steps + 1):
            previous = state["disturbance"].to_numpy()
            incoming = base_connectivity @ previous
            mean_disturbance = previous.mean()

            shock = 0.24 if t in (18, 36, 55, 70) else 0.0
            seasonal = 0.04 + 0.025 * np.sin(t / 7.0)

            disturbance = (
                previous
                + float(scenario["disturbance_load"])
                + seasonal
                + shock
                + 0.18 * float(scenario["climate_pressure"])
                + 0.22 * state["exposure"].astype(float).to_numpy()
                + float(scenario["spread_amplifier"]) * incoming
                + 0.10 * float(scenario["spread_amplifier"]) * mean_disturbance
                - 0.26 * state["buffer_capacity"].astype(float).to_numpy()
                - 0.12 * state["refugia"].astype(float).to_numpy()
                - 0.06 * float(scenario["governance_response"])
            )
            disturbance = np.clip(disturbance, 0.0, 1.40)
            state["disturbance"] = disturbance

            condition = (
                state["condition"].to_numpy()
                - 0.055 * disturbance
                + 0.018 * state["ecological_memory"].astype(float).to_numpy()
                + 0.015 * state["recovery_capacity"].astype(float).to_numpy()
                + 0.008 * state["refugia"].astype(float).to_numpy()
                + 0.006 * float(scenario["governance_response"])
            )
            condition = np.clip(condition, 0.0, 1.0)
            state["condition"] = condition

            margin = (
                condition
                + state["buffer_capacity"].astype(float).to_numpy()
                + state["ecological_memory"].astype(float).to_numpy()
                + state["recovery_capacity"].astype(float).to_numpy()
                + 0.25 * state["refugia"].astype(float).to_numpy()
                + 0.20 * float(scenario["governance_response"])
                - disturbance
                - state["exposure"].astype(float).to_numpy()
                - 0.30 * state["social_exposure"].astype(float).to_numpy()
            )

            step = state[["patch_id", "landscape_id", "patch_type", "refugia"]].copy()
            step["scenario_id"] = scenario["scenario_id"]
            step["scenario_name"] = scenario["scenario_name"]
            step["time"] = t
            step["condition"] = condition
            step["disturbance"] = disturbance
            step["resilience_margin"] = margin
            step["threshold_flag"] = np.where(margin < 0.75, "threshold risk", "viable margin")
            rows.append(step)

    return pd.concat(rows, ignore_index=True)


def expand_training(df: pd.DataFrame, n: int = 1800) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []

    for _ in range(n):
        base = df.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]
        record = {}

        for feature in FEATURES:
            record[feature] = float(np.clip(float(base[feature]) + rng.normal(0, 0.08), 0.05, 0.98))

        profile = (
            0.17 * record["spatial_heterogeneity"]
            + 0.15 * record["viable_connectivity"]
            + 0.17 * record["refugia_capacity"]
            + 0.17 * record["ecological_memory"]
            + 0.14 * record["governance_capacity"]
            - 0.11 * record["disturbance_pressure"]
            - 0.06 * record["fragmentation"]
            - 0.06 * record["social_vulnerability"]
        )
        risk = (
            0.28 * record["disturbance_pressure"]
            + 0.20 * record["fragmentation"]
            + 0.18 * record["social_vulnerability"]
            + 0.14 * (1 - record["refugia_capacity"])
            + 0.10 * (1 - record["ecological_memory"])
            + 0.10 * (1 - record["governance_capacity"])
            + rng.normal(0, 0.035)
        )
        record["landscape_resilience_profile"] = profile
        record["disturbance_risk_index"] = risk
        record["threshold_risk"] = 1 if risk - profile > 0.16 else 0
        rows.append(record)

    return pd.DataFrame(rows)


def plot_profiles(profiles: pd.DataFrame) -> None:
    plot_df = profiles[
        ["landscape_type", "landscape_resilience_profile", "disturbance_risk_index", "refugia_capacity", "ecological_memory"]
    ].melt(id_vars="landscape_type", var_name="indicator", value_name="value")

    order = profiles.sort_values("landscape_resilience_profile")["landscape_type"].tolist()
    plt.figure(figsize=(10, 6))

    for indicator, subset in plot_df.groupby("indicator"):
        y = [order.index(s) for s in subset["landscape_type"]]
        plt.scatter(subset["value"], y, label=indicator, s=60)

    plt.yticks(range(len(order)), order)
    plt.xlabel("Indicator value")
    plt.title("Landscape Resilience and Disturbance-Regime Profiles")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "landscape_resilience_profiles.png", dpi=160)
    plt.close()


def plot_simulation(sim: pd.DataFrame) -> None:
    summary = (
        sim.groupby(["scenario_name", "time"])
        .agg(
            mean_condition=("condition", "mean"),
            mean_disturbance=("disturbance", "mean"),
            mean_resilience_margin=("resilience_margin", "mean"),
            threshold_risk_patches=("threshold_flag", lambda x: (x == "threshold risk").sum()),
        )
        .reset_index()
    )

    summary.to_csv(OUT_TABLES / "landscape_disturbance_time_summary_advanced.csv", index=False)

    for y_col, y_label, filename, title in [
        ("mean_condition", "Mean patch condition", "mean_patch_condition_over_time.png", "Mean Patch Condition Over Time"),
        ("mean_disturbance", "Mean disturbance", "mean_disturbance_over_time.png", "Mean Disturbance Over Time"),
        ("mean_resilience_margin", "Mean resilience margin", "mean_resilience_margin_over_time.png", "Mean Landscape Resilience Margin"),
        ("threshold_risk_patches", "Threshold-risk patches", "threshold_risk_patches_over_time.png", "Threshold-Risk Patches Over Time"),
    ]:
        plt.figure(figsize=(10, 6))
        for scenario_name in summary["scenario_name"].unique():
            subset = summary[summary["scenario_name"] == scenario_name]
            plt.plot(subset["time"], subset[y_col], label=scenario_name)
        if y_col == "mean_resilience_margin":
            plt.axhline(0.75, linestyle="--", linewidth=1, label="Threshold-risk reference")
        plt.xlabel("Time")
        plt.ylabel(y_label)
        plt.title(title)
        plt.legend(fontsize=8)
        plt.tight_layout()
        plt.savefig(OUT_FIGURES / filename, dpi=160)
        plt.close()


def main() -> None:
    raw_profiles = pd.read_csv(PROFILES_PATH)
    patches = pd.read_csv(PATCHES_PATH)
    scenarios = pd.read_csv(SCENARIOS_PATH)

    profiles = score_profiles(raw_profiles)
    sim = simulate_patches(patches, scenarios)

    profiles.to_csv(OUT_TABLES / "landscape_resilience_profiles_advanced.csv", index=False)
    sim.to_csv(OUT_TABLES / "landscape_disturbance_patch_simulation_advanced.csv", index=False)

    scenario_summary = (
        sim.groupby("scenario_name")
        .agg(
            minimum_condition=("condition", "min"),
            mean_final_condition=("condition", lambda x: x.tail(len(patches)).mean()),
            maximum_disturbance=("disturbance", "max"),
            minimum_resilience_margin=("resilience_margin", "min"),
            threshold_risk_patch_steps=("threshold_flag", lambda x: (x == "threshold risk").sum()),
        )
        .reset_index()
    )
    scenario_summary.to_csv(OUT_TABLES / "landscape_disturbance_scenario_summary_advanced.csv", index=False)

    plot_profiles(profiles)
    plot_simulation(sim)

    training = expand_training(raw_profiles)
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
            "model": "random_forest_landscape_disturbance_risk_classifier",
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

    training.to_csv(OUT_TABLES / "synthetic_landscape_disturbance_training_data.csv", index=False)
    metrics.to_csv(OUT_TABLES / "advanced_landscape_disturbance_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "landscape_disturbance_risk_classifier.joblib")

    plt.figure(figsize=(10, 6))
    plt.barh(importance["feature"], importance["importance"])
    plt.gca().invert_yaxis()
    plt.xlabel("Importance")
    plt.title("Feature Importance for Landscape Disturbance Risk")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "advanced_feature_importance.png", dpi=160)
    plt.close()

    print("Advanced landscape resilience workflow complete.")
    print(profiles[["landscape_type", "landscape_resilience_profile", "disturbance_risk_index"]].round(3))
    print(metrics.round(4))


if __name__ == "__main__":
    main()
