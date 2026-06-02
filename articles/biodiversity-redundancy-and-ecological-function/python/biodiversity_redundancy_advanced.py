#!/usr/bin/env python3
"""
Advanced biodiversity, redundancy, and ecological-function workflow.

Uses pandas, numpy, matplotlib, scikit-learn, and joblib.

Run:
    pip install -r requirements-advanced.txt
    python python/biodiversity_redundancy_advanced.py
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
FUNCTIONS_PATH = ROOT / "data" / "raw" / "ecological_function_profiles.csv"
TRAITS_PATH = ROOT / "data" / "raw" / "species_trait_table.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "disturbance_scenarios.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_FIGURES = ROOT / "outputs" / "figures"
OUT_MODELS = ROOT / "outputs" / "models"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)
OUT_MODELS.mkdir(parents=True, exist_ok=True)

FEATURES = [
    "species_richness",
    "functional_diversity",
    "functional_redundancy",
    "response_diversity",
    "connectivity",
    "ecological_memory",
    "disturbance_exposure",
]


def score_profiles(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["functional_resilience_profile"] = (
        0.12 * out["species_richness"]
        + 0.19 * out["functional_diversity"]
        + 0.17 * out["functional_redundancy"]
        + 0.20 * out["response_diversity"]
        + 0.13 * out["connectivity"]
        + 0.16 * out["ecological_memory"]
        - 0.12 * out["disturbance_exposure"]
    )
    out["function_threshold_risk_index"] = np.clip(
        0.24 * (1 - out["response_diversity"])
        + 0.22 * (1 - out["functional_redundancy"])
        + 0.18 * out["disturbance_exposure"]
        + 0.14 * (1 - out["connectivity"])
        + 0.12 * (1 - out["ecological_memory"])
        + 0.10 * (1 - out["functional_diversity"]),
        0,
        1,
    )
    return out


def simulate_function_loss(traits: pd.DataFrame, scenarios: pd.DataFrame, steps: int = 100) -> pd.DataFrame:
    rows = []

    for _, scenario in scenarios.iterrows():
        species = traits.copy()
        species["abundance"] = species["initial_abundance"].astype(float)

        for t in range(1, steps + 1):
            seasonal = 0.055 + 0.025 * np.sin(t / 9)
            shock = float(scenario["shock_intensity"]) if int(scenario["shock_frequency"]) > 0 and t % int(scenario["shock_frequency"]) == 0 else 0.0
            disturbance = float(scenario["disturbance_pressure"]) + seasonal + shock

            mortality = disturbance * species["disturbance_sensitivity"].astype(float)
            recovery = 0.020 * species["recovery_capacity"].astype(float) + 0.006 * float(scenario["recovery_support"])
            species["abundance"] = np.clip(species["abundance"] - mortality * 0.085 + recovery, 0.0, 1.2)
            species["functional_output"] = species["abundance"] * species["trait_contribution"].astype(float)

            grouped = (
                species.groupby("functional_group")
                .agg(
                    species_present=("abundance", lambda x: int((x > 0.10).sum())),
                    mean_abundance=("abundance", "mean"),
                    functional_output=("functional_output", "sum"),
                    response_diversity=("disturbance_sensitivity", "var"),
                )
                .reset_index()
            )
            grouped["response_diversity"] = grouped["response_diversity"].fillna(0)
            grouped["resilience_margin"] = (
                grouped["functional_output"]
                + 0.055 * grouped["species_present"]
                + grouped["response_diversity"]
                - disturbance
            )
            grouped["threshold_flag"] = np.where(grouped["resilience_margin"] < 1.20, "threshold risk", "viable margin")
            grouped["scenario_id"] = scenario["scenario_id"]
            grouped["scenario_name"] = scenario["scenario_name"]
            grouped["time"] = t
            grouped["disturbance"] = disturbance
            rows.append(grouped)

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
            0.12 * record["species_richness"]
            + 0.19 * record["functional_diversity"]
            + 0.17 * record["functional_redundancy"]
            + 0.20 * record["response_diversity"]
            + 0.13 * record["connectivity"]
            + 0.16 * record["ecological_memory"]
            - 0.12 * record["disturbance_exposure"]
        )
        risk = (
            0.24 * (1 - record["response_diversity"])
            + 0.22 * (1 - record["functional_redundancy"])
            + 0.18 * record["disturbance_exposure"]
            + 0.14 * (1 - record["connectivity"])
            + 0.12 * (1 - record["ecological_memory"])
            + 0.10 * (1 - record["functional_diversity"])
            + rng.normal(0, 0.035)
        )

        record["functional_resilience_profile"] = profile
        record["function_threshold_risk_index"] = risk
        record["threshold_risk"] = 1 if risk > 0.46 else 0
        rows.append(record)

    return pd.DataFrame(rows)


def plot_profiles(profiles: pd.DataFrame) -> None:
    plot_df = profiles[
        ["ecosystem_function", "functional_resilience_profile", "function_threshold_risk_index", "functional_redundancy", "response_diversity"]
    ].melt(id_vars="ecosystem_function", var_name="indicator", value_name="value")

    order = profiles.sort_values("functional_resilience_profile")["ecosystem_function"].tolist()
    plt.figure(figsize=(10, 6))

    for indicator, subset in plot_df.groupby("indicator"):
        y = [order.index(s) for s in subset["ecosystem_function"]]
        plt.scatter(subset["value"], y, label=indicator, s=60)

    plt.yticks(range(len(order)), order)
    plt.xlabel("Indicator value")
    plt.title("Functional Diversity, Redundancy, and Resilience Profiles")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "functional_diversity_redundancy_profiles.png", dpi=160)
    plt.close()


def plot_simulation(sim: pd.DataFrame) -> None:
    scenario = "Climate-amplified stress"
    subset_sim = sim[sim["scenario_name"] == scenario]

    for y_col, y_label, filename, title in [
        ("functional_output", "Functional output", "function_output_over_time.png", "Ecological Function Under Disturbance"),
        ("species_present", "Species present", "functional_redundancy_over_time.png", "Functional Redundancy Over Time"),
        ("resilience_margin", "Resilience margin", "functional_resilience_margin_over_time.png", "Functional Resilience Margin"),
    ]:
        plt.figure(figsize=(10, 6))
        for group in subset_sim["functional_group"].unique():
            subset = subset_sim[subset_sim["functional_group"] == group]
            plt.plot(subset["time"], subset[y_col], label=group)
        if y_col == "resilience_margin":
            plt.axhline(1.20, linestyle="--", linewidth=1, label="Threshold-risk reference")
        plt.xlabel("Time")
        plt.ylabel(y_label)
        plt.title(title)
        plt.legend(fontsize=8)
        plt.tight_layout()
        plt.savefig(OUT_FIGURES / filename, dpi=160)
        plt.close()


def main() -> None:
    functions = pd.read_csv(FUNCTIONS_PATH)
    traits = pd.read_csv(TRAITS_PATH)
    scenarios = pd.read_csv(SCENARIOS_PATH)

    profiles = score_profiles(functions)
    sim = simulate_function_loss(traits, scenarios)

    profiles.to_csv(OUT_TABLES / "functional_diversity_redundancy_profiles_advanced.csv", index=False)
    sim.to_csv(OUT_TABLES / "function_loss_simulation_advanced.csv", index=False)

    summary = (
        sim.groupby(["scenario_name", "functional_group"])
        .agg(
            minimum_functional_output=("functional_output", "min"),
            final_functional_output=("functional_output", "last"),
            minimum_species_present=("species_present", "min"),
            minimum_resilience_margin=("resilience_margin", "min"),
            threshold_risk_steps=("threshold_flag", lambda x: (x == "threshold risk").sum()),
        )
        .reset_index()
    )
    summary.to_csv(OUT_TABLES / "function_loss_summary_advanced.csv", index=False)

    plot_profiles(profiles)
    plot_simulation(sim)

    training = expand_training(functions)
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
            "model": "random_forest_function_threshold_risk_classifier",
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

    training.to_csv(OUT_TABLES / "synthetic_function_threshold_training_data.csv", index=False)
    metrics.to_csv(OUT_TABLES / "advanced_function_threshold_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "function_threshold_risk_classifier.joblib")

    plt.figure(figsize=(10, 6))
    plt.barh(importance["feature"], importance["importance"])
    plt.gca().invert_yaxis()
    plt.xlabel("Importance")
    plt.title("Feature Importance for Ecological Function Threshold Risk")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "advanced_feature_importance.png", dpi=160)
    plt.close()

    print("Advanced biodiversity redundancy workflow complete.")
    print(profiles[["ecosystem_function", "functional_resilience_profile", "function_threshold_risk_index"]].round(3))
    print(metrics.round(4))


if __name__ == "__main__":
    main()
