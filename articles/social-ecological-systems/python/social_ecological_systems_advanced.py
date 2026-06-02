#!/usr/bin/env python3
"""
Advanced social-ecological systems workflow.

Uses pandas, numpy, matplotlib, scikit-learn, and joblib.

Run:
    pip install -r requirements-advanced.txt
    python python/social_ecological_systems_advanced.py
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
PROFILES_PATH = ROOT / "data" / "raw" / "social_ecological_system_profiles.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "coupled_scenarios.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_FIGURES = ROOT / "outputs" / "figures"
OUT_MODELS = ROOT / "outputs" / "models"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)
OUT_MODELS.mkdir(parents=True, exist_ok=True)

FEATURES = [
    "ecological_condition",
    "governance_quality",
    "livelihood_diversity",
    "infrastructure_support",
    "knowledge_integration",
    "social_trust",
    "market_pressure",
    "climate_exposure",
    "adaptive_capacity",
    "resource_dependency",
]


def score_profiles(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["ses_resilience_profile"] = (
        0.18 * out["ecological_condition"]
        + 0.16 * out["governance_quality"]
        + 0.12 * out["livelihood_diversity"]
        + 0.12 * out["infrastructure_support"]
        + 0.13 * out["knowledge_integration"]
        + 0.11 * out["social_trust"]
        + 0.10 * out["adaptive_capacity"]
        - 0.09 * out["market_pressure"]
        - 0.07 * out["climate_exposure"]
        - 0.02 * out["resource_dependency"]
    )
    out["coupled_vulnerability"] = (
        0.26 * out["market_pressure"]
        + 0.25 * out["climate_exposure"]
        + 0.18 * out["resource_dependency"]
        + 0.15 * (1 - out["governance_quality"])
        + 0.10 * (1 - out["livelihood_diversity"])
        + 0.06 * (1 - out["social_trust"])
    )
    return out


def simulate_scenarios(scenarios: pd.DataFrame, steps: int = 90) -> pd.DataFrame:
    rows = []
    time_steps = np.arange(1, steps + 1)

    for _, scenario in scenarios.iterrows():
        ecology = float(scenario["initial_ecology"])
        social_pressure = float(scenario["initial_social_pressure"])
        governance = float(scenario["governance_effectiveness"])
        livelihood_pressure = float(scenario["livelihood_pressure"])
        climate_pressure = float(scenario["climate_pressure"])
        market_shock = float(scenario["market_shock"])

        r = 0.08
        k = 1.0
        q = 0.10

        for t in time_steps:
            extraction = q * social_pressure * ecology
            ecological_growth = r * ecology * (1 - ecology / k)
            climate_effect = 0.022 * climate_pressure
            governance_repair = 0.017 * governance

            ecology = ecology + ecological_growth - extraction - climate_effect + governance_repair
            ecology = float(np.clip(ecology, 0.01, 1.20))

            market_pulse = 0.035 * market_shock if t in (20, 42, 68) else 0.0
            social_pressure = (
                social_pressure
                + 0.050 * livelihood_pressure
                + 0.028 * (1 - governance)
                + market_pulse
                - 0.043 * ecology
            )
            social_pressure = float(np.clip(social_pressure, 0.05, 1.20))

            resilience_margin = ecology + governance + 0.35 * (1 - livelihood_pressure) - social_pressure - 0.35 * climate_pressure

            rows.append(
                {
                    "scenario_id": scenario["scenario_id"],
                    "scenario_name": scenario["scenario_name"],
                    "time": int(t),
                    "ecology": ecology,
                    "social_pressure": social_pressure,
                    "extraction": extraction,
                    "resilience_margin": resilience_margin,
                    "threshold_flag": "threshold risk" if resilience_margin < 0.20 else "viable margin",
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

        resilience = (
            0.18 * record["ecological_condition"]
            + 0.16 * record["governance_quality"]
            + 0.12 * record["livelihood_diversity"]
            + 0.12 * record["infrastructure_support"]
            + 0.13 * record["knowledge_integration"]
            + 0.11 * record["social_trust"]
            + 0.10 * record["adaptive_capacity"]
            - 0.09 * record["market_pressure"]
            - 0.07 * record["climate_exposure"]
            - 0.02 * record["resource_dependency"]
        )

        vulnerability = (
            0.26 * record["market_pressure"]
            + 0.25 * record["climate_exposure"]
            + 0.18 * record["resource_dependency"]
            + 0.15 * (1 - record["governance_quality"])
            + 0.10 * (1 - record["livelihood_diversity"])
            + 0.06 * (1 - record["social_trust"])
            + rng.normal(0, 0.035)
        )

        record["ses_resilience_profile"] = resilience
        record["coupled_vulnerability"] = vulnerability
        record["threshold_risk"] = 1 if vulnerability - resilience > 0.18 else 0
        rows.append(record)

    return pd.DataFrame(rows)


def plot_profiles(profiles: pd.DataFrame) -> None:
    plot_df = profiles[
        ["system_type", "ses_resilience_profile", "coupled_vulnerability", "ecological_condition", "governance_quality"]
    ].melt(id_vars="system_type", var_name="indicator", value_name="value")

    order = profiles.sort_values("ses_resilience_profile")["system_type"].tolist()
    plt.figure(figsize=(10, 6))

    for indicator, subset in plot_df.groupby("indicator"):
        y = [order.index(s) for s in subset["system_type"]]
        plt.scatter(subset["value"], y, label=indicator, s=60)

    plt.yticks(range(len(order)), order)
    plt.xlabel("Indicator value")
    plt.title("Social-Ecological System Resilience Profiles")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "social_ecological_system_profiles.png", dpi=160)
    plt.close()


def plot_simulation(sim: pd.DataFrame) -> None:
    for y_col, y_label, filename, title in [
        ("ecology", "Ecological condition", "coupled_ecology_over_time.png", "Ecological Condition Under SES Scenarios"),
        ("social_pressure", "Social pressure", "coupled_social_pressure_over_time.png", "Social Pressure Under SES Scenarios"),
        ("resilience_margin", "SES resilience margin", "coupled_resilience_margin_over_time.png", "SES Resilience Margin Under Coupled Feedbacks"),
    ]:
        plt.figure(figsize=(10, 6))
        for scenario_name in sim["scenario_name"].unique():
            subset = sim[sim["scenario_name"] == scenario_name]
            plt.plot(subset["time"], subset[y_col], label=scenario_name)
        if y_col == "resilience_margin":
            plt.axhline(0.20, linestyle="--", linewidth=1, label="Threshold-risk reference")
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
    sim = simulate_scenarios(scenarios)

    profiles.to_csv(OUT_TABLES / "social_ecological_system_profiles_advanced.csv", index=False)
    sim.to_csv(OUT_TABLES / "social_ecological_coupled_simulation_advanced.csv", index=False)

    summary = (
        sim.groupby("scenario_name")
        .agg(
            minimum_ecology=("ecology", "min"),
            final_ecology=("ecology", "last"),
            maximum_social_pressure=("social_pressure", "max"),
            minimum_resilience_margin=("resilience_margin", "min"),
            threshold_risk_steps=("threshold_flag", lambda x: (x == "threshold risk").sum()),
        )
        .reset_index()
    )
    summary.to_csv(OUT_TABLES / "social_ecological_simulation_summary_advanced.csv", index=False)

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
            "model": "random_forest_ses_threshold_risk_classifier",
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

    training.to_csv(OUT_TABLES / "synthetic_ses_threshold_training_data.csv", index=False)
    metrics.to_csv(OUT_TABLES / "advanced_ses_threshold_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "ses_threshold_risk_classifier.joblib")

    plt.figure(figsize=(10, 6))
    plt.barh(importance["feature"], importance["importance"])
    plt.gca().invert_yaxis()
    plt.xlabel("Importance")
    plt.title("Feature Importance for SES Threshold Risk")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "advanced_feature_importance.png", dpi=160)
    plt.close()

    print("Advanced social-ecological systems workflow complete.")
    print(profiles[["system_type", "ses_resilience_profile", "coupled_vulnerability"]].round(3))
    print(metrics.round(4))


if __name__ == "__main__":
    main()
