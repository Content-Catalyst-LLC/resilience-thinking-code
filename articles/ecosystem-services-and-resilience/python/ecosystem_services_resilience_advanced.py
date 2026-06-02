#!/usr/bin/env python3
"""
Advanced ecosystem-service resilience workflow.

Uses pandas, numpy, matplotlib, scikit-learn, and joblib.

Run:
    pip install -r requirements-advanced.txt
    python python/ecosystem_services_resilience_advanced.py
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
PROFILES_PATH = ROOT / "data" / "raw" / "ecosystem_service_profiles.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "service_disturbance_scenarios.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_FIGURES = ROOT / "outputs" / "figures"
OUT_MODELS = ROOT / "outputs" / "models"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)
OUT_MODELS.mkdir(parents=True, exist_ok=True)

FEATURES = [
    "current_service_flow",
    "ecological_condition",
    "functional_diversity",
    "functional_redundancy",
    "threshold_distance",
    "governance_capacity",
    "disturbance_exposure",
    "access_equity",
    "ecological_memory",
]


def score_profiles(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["service_resilience_profile"] = (
        0.10 * out["current_service_flow"]
        + 0.17 * out["ecological_condition"]
        + 0.15 * out["functional_diversity"]
        + 0.14 * out["functional_redundancy"]
        + 0.15 * out["threshold_distance"]
        + 0.12 * out["governance_capacity"]
        + 0.09 * out["access_equity"]
        + 0.12 * out["ecological_memory"]
        - 0.12 * out["disturbance_exposure"]
    )
    out["service_resilience_gap"] = out["service_resilience_profile"] - out["current_service_flow"]
    out["service_threshold_risk_index"] = np.clip(
        0.26 * (1 - out["threshold_distance"])
        + 0.22 * out["disturbance_exposure"]
        + 0.16 * (1 - out["functional_redundancy"])
        + 0.14 * (1 - out["functional_diversity"])
        + 0.12 * (1 - out["governance_capacity"])
        + 0.10 * (1 - out["ecological_memory"])
        - 0.08 * out["access_equity"],
        0,
        1,
    )
    return out


def simulate_services(profiles: pd.DataFrame, scenarios: pd.DataFrame, steps: int = 100) -> pd.DataFrame:
    rows = []

    for _, service in profiles.iterrows():
        for _, scenario in scenarios.iterrows():
            condition = float(service["ecological_condition"])
            functional_capacity = float(service["functional_diversity"])
            redundancy = float(service["functional_redundancy"])
            memory = float(service["ecological_memory"])
            governance = float(service["governance_capacity"])
            exposure = float(service["disturbance_exposure"])
            access = float(service["access_equity"])

            for t in range(1, steps + 1):
                seasonal_pressure = 0.04 + 0.020 * np.sin(t / 8)
                shock = float(scenario["shock_intensity"]) if int(scenario["shock_frequency"]) > 0 and t % int(scenario["shock_frequency"]) == 0 else 0.0
                disturbance = float(scenario["disturbance_load"]) + seasonal_pressure + shock + 0.16 * exposure

                repair = (
                    0.010 * redundancy
                    + 0.009 * memory
                    + 0.007 * governance
                    + 0.004 * float(scenario["governance_response"])
                )
                erosion = disturbance * (0.40 + exposure)

                condition = float(np.clip(condition - 0.042 * erosion + repair, 0.01, 1.0))
                functional_capacity = float(np.clip(functional_capacity - 0.028 * erosion + 0.006 * redundancy, 0.01, 1.0))

                service_flow = float(np.clip(condition * functional_capacity * (1 - 0.33 * disturbance), 0.0, 1.0))
                margin = condition + functional_capacity + redundancy + memory + governance + 0.35 * access - disturbance - exposure

                rows.append(
                    {
                        "service_id": service["service_id"],
                        "service": service["service"],
                        "scenario_id": scenario["scenario_id"],
                        "scenario_name": scenario["scenario_name"],
                        "time": t,
                        "disturbance": disturbance,
                        "ecosystem_condition": condition,
                        "functional_capacity": functional_capacity,
                        "service_flow": service_flow,
                        "resilience_margin": margin,
                        "threshold_flag": "threshold risk" if margin < 1.30 else "viable margin",
                    }
                )

    return pd.DataFrame(rows)


def expand_training(df: pd.DataFrame, n: int = 1800) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []

    for _ in range(n):
        base = df.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]
        record = {}

        for feature in FEATURES:
            record[feature] = float(np.clip(float(base[feature]) + rng.normal(0, 0.08), 0.05, 0.98))

        profile = (
            0.10 * record["current_service_flow"]
            + 0.17 * record["ecological_condition"]
            + 0.15 * record["functional_diversity"]
            + 0.14 * record["functional_redundancy"]
            + 0.15 * record["threshold_distance"]
            + 0.12 * record["governance_capacity"]
            + 0.09 * record["access_equity"]
            + 0.12 * record["ecological_memory"]
            - 0.12 * record["disturbance_exposure"]
        )
        risk = (
            0.26 * (1 - record["threshold_distance"])
            + 0.22 * record["disturbance_exposure"]
            + 0.16 * (1 - record["functional_redundancy"])
            + 0.14 * (1 - record["functional_diversity"])
            + 0.12 * (1 - record["governance_capacity"])
            + 0.10 * (1 - record["ecological_memory"])
            - 0.08 * record["access_equity"]
            + rng.normal(0, 0.035)
        )

        record["service_resilience_profile"] = profile
        record["service_threshold_risk_index"] = risk
        record["threshold_risk"] = 1 if risk > 0.46 else 0
        rows.append(record)

    return pd.DataFrame(rows)


def plot_profiles(profiles: pd.DataFrame) -> None:
    plot_df = profiles[
        ["service", "current_service_flow", "service_resilience_profile", "service_threshold_risk_index", "access_equity"]
    ].melt(id_vars="service", var_name="indicator", value_name="value")

    order = profiles.sort_values("service_resilience_profile")["service"].tolist()
    plt.figure(figsize=(10, 6))

    for indicator, subset in plot_df.groupby("indicator"):
        y = [order.index(s) for s in subset["service"]]
        plt.scatter(subset["value"], y, label=indicator, s=60)

    plt.yticks(range(len(order)), order)
    plt.xlabel("Indicator value")
    plt.title("Ecosystem-Service Resilience Profiles")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "ecosystem_service_resilience_profiles.png", dpi=160)
    plt.close()


def plot_simulation(sim: pd.DataFrame) -> None:
    for y_col, y_label, filename, title in [
        ("service_flow", "Service flow", "service_flow_over_time.png", "Ecosystem-Service Flow Under Disturbance"),
        ("resilience_margin", "Resilience margin", "service_resilience_margin_over_time.png", "Ecosystem-Service Resilience Margin"),
    ]:
        plt.figure(figsize=(10, 6))
        subset_sim = sim[sim["scenario_name"] == "Climate-amplified disturbance"]
        for service_name in subset_sim["service"].unique():
            subset = subset_sim[subset_sim["service"] == service_name]
            plt.plot(subset["time"], subset[y_col], label=service_name)
        if y_col == "resilience_margin":
            plt.axhline(1.30, linestyle="--", linewidth=1, label="Threshold-risk reference")
        plt.xlabel("Time")
        plt.ylabel(y_label)
        plt.title(title)
        plt.legend(fontsize=8)
        plt.tight_layout()
        plt.savefig(OUT_FIGURES / filename, dpi=160)
        plt.close()


def main() -> None:
    raw = pd.read_csv(PROFILES_PATH)
    scenarios = pd.read_csv(SCENARIOS_PATH)

    profiles = score_profiles(raw)
    sim = simulate_services(raw, scenarios)

    profiles.to_csv(OUT_TABLES / "ecosystem_service_resilience_profiles_advanced.csv", index=False)
    sim.to_csv(OUT_TABLES / "ecosystem_service_disturbance_simulation_advanced.csv", index=False)

    summary = (
        sim.groupby(["service", "scenario_name"])
        .agg(
            minimum_service_flow=("service_flow", "min"),
            final_service_flow=("service_flow", "last"),
            minimum_resilience_margin=("resilience_margin", "min"),
            threshold_risk_steps=("threshold_flag", lambda x: (x == "threshold risk").sum()),
        )
        .reset_index()
    )
    summary.to_csv(OUT_TABLES / "ecosystem_service_disturbance_summary_advanced.csv", index=False)

    plot_profiles(profiles)
    plot_simulation(sim)

    training = expand_training(raw)
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
            "model": "random_forest_ecosystem_service_threshold_risk_classifier",
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

    training.to_csv(OUT_TABLES / "synthetic_service_threshold_training_data.csv", index=False)
    metrics.to_csv(OUT_TABLES / "advanced_service_threshold_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "ecosystem_service_threshold_risk_classifier.joblib")

    plt.figure(figsize=(10, 6))
    plt.barh(importance["feature"], importance["importance"])
    plt.gca().invert_yaxis()
    plt.xlabel("Importance")
    plt.title("Feature Importance for Ecosystem-Service Threshold Risk")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "advanced_feature_importance.png", dpi=160)
    plt.close()

    print("Advanced ecosystem-service resilience workflow complete.")
    print(profiles[["service", "current_service_flow", "service_resilience_profile", "service_threshold_risk_index"]].round(3))
    print(metrics.round(4))


if __name__ == "__main__":
    main()
