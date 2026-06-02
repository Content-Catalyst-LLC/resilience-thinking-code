#!/usr/bin/env python3
"""
Advanced adaptive capacity workflow.

Uses pandas, numpy, matplotlib, scikit-learn, and joblib.

Run:
    pip install -r requirements-advanced.txt
    python python/adaptive_capacity_advanced.py
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
PROFILES_PATH = ROOT / "data" / "raw" / "adaptive_capacity_profiles.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "disturbance_scenarios.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_FIGURES = ROOT / "outputs" / "figures"
OUT_MODELS = ROOT / "outputs" / "models"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)
OUT_MODELS.mkdir(parents=True, exist_ok=True)

FEATURES = [
    "learning",
    "flexibility",
    "diversity",
    "governance_capacity",
    "slack",
    "trust_legitimacy",
    "rigidity",
    "exposure",
]


def score_profiles(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["adaptive_capacity"] = (
        0.18 * out["learning"]
        + 0.18 * out["flexibility"]
        + 0.17 * out["diversity"]
        + 0.17 * out["governance_capacity"]
        + 0.14 * out["slack"]
        + 0.16 * out["trust_legitimacy"]
        - 0.12 * out["rigidity"]
    )
    out["adaptive_vulnerability"] = (
        0.34 * out["exposure"]
        + 0.24 * out["rigidity"]
        + 0.16 * (1 - out["slack"])
        + 0.14 * (1 - out["trust_legitimacy"])
        + 0.12 * (1 - out["governance_capacity"])
    )
    out["response_space_baseline"] = out["adaptive_capacity"] - out["adaptive_vulnerability"]

    conditions = [
        (out["adaptive_capacity"] >= 0.58) & (out["adaptive_vulnerability"] < 0.55),
        out["adaptive_vulnerability"] >= 0.66,
        out["rigidity"] >= 0.62,
    ]
    choices = [
        "stronger adaptive-capacity profile",
        "high adaptive-vulnerability concern",
        "rigidity and lock-in concern",
    ]
    out["diagnostic"] = np.select(conditions, choices, default="mixed adaptive-capacity profile requiring monitoring")
    return out


def simulate_viability(systems: pd.DataFrame, scenarios: pd.DataFrame, steps: int = 80) -> pd.DataFrame:
    rows = []

    for _, system in systems.iterrows():
        for _, scenario in scenarios.iterrows():
            capacity = float(system["adaptive_capacity"])
            vulnerability = float(system["adaptive_vulnerability"])
            rigidity = float(system["rigidity"])
            exposure = float(system["exposure"])
            viability = 1.0

            for t in range(1, steps + 1):
                seasonal = 0.04 + 0.025 * np.sin(t / 8.0)
                shock = float(scenario["shock_intensity"]) if int(scenario["shock_frequency"]) > 0 and t % int(scenario["shock_frequency"]) == 0 else 0.0
                disturbance = float(scenario["disturbance_load"]) + seasonal + shock + 0.18 * exposure

                capacity = float(np.clip(
                    capacity
                    + float(scenario["learning_gain"])
                    + 0.006 * float(scenario["governance_response"])
                    - 0.010 * rigidity,
                    0.0,
                    1.2,
                ))

                rigidity = float(np.clip(
                    rigidity
                    + float(scenario["rigidity_growth"])
                    + 0.004 * disturbance
                    - 0.006 * float(scenario["governance_response"]),
                    0.0,
                    1.0,
                ))

                response_space = (
                    capacity
                    + 0.35 * float(system["slack"])
                    + 0.25 * float(system["trust_legitimacy"])
                    - rigidity
                    - 0.25 * vulnerability
                )

                viability = (
                    viability
                    - 0.46 * disturbance
                    + 0.25 * capacity
                    + 0.08 * response_space
                    - 0.12 * rigidity
                )
                viability = float(np.clip(viability, 0.0, 1.2))

                rows.append(
                    {
                        "system_id": system["system_id"],
                        "system_type": system["system_type"],
                        "scenario_id": scenario["scenario_id"],
                        "scenario_name": scenario["scenario_name"],
                        "time": t,
                        "disturbance": disturbance,
                        "adaptive_capacity": capacity,
                        "adaptive_vulnerability": vulnerability,
                        "rigidity": rigidity,
                        "response_space": response_space,
                        "viability": viability,
                        "threshold_flag": "threshold risk" if viability < 0.45 else "viable margin",
                    }
                )

    return pd.DataFrame(rows)


def expand_training(df: pd.DataFrame, n: int = 2200) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []

    for _ in range(n):
        base = df.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]
        record = {}

        for feature in FEATURES:
            record[feature] = float(np.clip(float(base[feature]) + rng.normal(0, 0.08), 0.05, 0.98))

        capacity = (
            0.18 * record["learning"]
            + 0.18 * record["flexibility"]
            + 0.17 * record["diversity"]
            + 0.17 * record["governance_capacity"]
            + 0.14 * record["slack"]
            + 0.16 * record["trust_legitimacy"]
            - 0.12 * record["rigidity"]
        )
        vulnerability = (
            0.34 * record["exposure"]
            + 0.24 * record["rigidity"]
            + 0.16 * (1 - record["slack"])
            + 0.14 * (1 - record["trust_legitimacy"])
            + 0.12 * (1 - record["governance_capacity"])
        )
        risk_index = vulnerability - capacity + rng.normal(0, 0.035)

        record["adaptive_capacity"] = capacity
        record["adaptive_vulnerability"] = vulnerability
        record["response_space_baseline"] = capacity - vulnerability
        record["threshold_risk"] = 1 if risk_index > 0.08 else 0
        rows.append(record)

    return pd.DataFrame(rows)


def plot_profiles(profiles: pd.DataFrame) -> None:
    plot_df = profiles[
        ["system_type", "adaptive_capacity", "adaptive_vulnerability", "response_space_baseline", "rigidity"]
    ].melt(id_vars="system_type", var_name="indicator", value_name="value")

    order = profiles.sort_values("adaptive_capacity")["system_type"].tolist()
    plt.figure(figsize=(10, 6))

    for indicator, subset in plot_df.groupby("indicator"):
        y = [order.index(s) for s in subset["system_type"]]
        plt.scatter(subset["value"], y, label=indicator, s=60)

    plt.yticks(range(len(order)), order)
    plt.xlabel("Indicator value")
    plt.title("Adaptive Capacity, Vulnerability, Response Space, and Rigidity")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "adaptive_capacity_profiles.png", dpi=160)
    plt.close()


def plot_simulation(sim: pd.DataFrame) -> None:
    scenario_name = "Climate-amplified disturbance"
    subset_sim = sim[sim["scenario_name"] == scenario_name]

    for y_col, y_label, filename, title in [
        ("viability", "Viability", "viability_over_time.png", "System Viability Under Climate-Amplified Disturbance"),
        ("adaptive_capacity", "Adaptive capacity", "adaptive_capacity_over_time.png", "Adaptive Capacity Over Time"),
        ("response_space", "Response space", "response_space_over_time.png", "Response Space Over Time"),
        ("rigidity", "Rigidity", "rigidity_over_time.png", "Rigidity Over Time"),
    ]:
        plt.figure(figsize=(10, 6))
        for system_type in subset_sim["system_type"].unique():
            subset = subset_sim[subset_sim["system_type"] == system_type]
            plt.plot(subset["time"], subset[y_col], label=system_type)
        if y_col == "viability":
            plt.axhline(0.45, linestyle="--", linewidth=1, label="Threshold-risk reference")
        plt.xlabel("Time")
        plt.ylabel(y_label)
        plt.title(title)
        plt.legend(fontsize=8)
        plt.tight_layout()
        plt.savefig(OUT_FIGURES / filename, dpi=160)
        plt.close()


def main() -> None:
    raw_profiles = pd.read_csv(PROFILES_PATH)
    scenarios = pd.read_csv(SCENARIOS_PATH)

    profiles = score_profiles(raw_profiles)
    sim = simulate_viability(profiles, scenarios)

    profiles.to_csv(OUT_TABLES / "adaptive_capacity_profiles_advanced.csv", index=False)
    sim.to_csv(OUT_TABLES / "adaptive_capacity_viability_simulation_advanced.csv", index=False)

    summary = (
        sim.groupby(["system_type", "scenario_name"])
        .agg(
            minimum_viability=("viability", "min"),
            final_viability=("viability", "last"),
            minimum_response_space=("response_space", "min"),
            maximum_rigidity=("rigidity", "max"),
            threshold_risk_steps=("threshold_flag", lambda x: (x == "threshold risk").sum()),
        )
        .reset_index()
    )
    summary.to_csv(OUT_TABLES / "adaptive_capacity_viability_summary_advanced.csv", index=False)

    plot_profiles(profiles)
    plot_simulation(sim)

    training = expand_training(raw_profiles)
    X = training[FEATURES]
    y = training["threshold_risk"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=400,
        min_samples_leaf=6,
        class_weight="balanced",
        random_state=42,
    )
    model.fit(X_train, y_train)

    prob = model.predict_proba(X_test)[:, 1]
    pred = (prob >= 0.50).astype(int)

    metrics = pd.DataFrame(
        [{
            "model": "random_forest_adaptive_capacity_threshold_risk_classifier",
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

    training.to_csv(OUT_TABLES / "synthetic_adaptive_capacity_threshold_training_data.csv", index=False)
    metrics.to_csv(OUT_TABLES / "advanced_adaptive_capacity_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "adaptive_capacity_threshold_risk_classifier.joblib")

    plt.figure(figsize=(10, 6))
    plt.barh(importance["feature"], importance["importance"])
    plt.gca().invert_yaxis()
    plt.xlabel("Importance")
    plt.title("Feature Importance for Adaptive-Capacity Threshold Risk")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "advanced_feature_importance.png", dpi=160)
    plt.close()

    print("Advanced adaptive capacity workflow complete.")
    print(profiles[["system_type", "adaptive_capacity", "adaptive_vulnerability", "response_space_baseline", "diagnostic"]].round(3))
    print(metrics.round(4))


if __name__ == "__main__":
    main()
