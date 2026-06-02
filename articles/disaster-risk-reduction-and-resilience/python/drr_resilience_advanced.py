#!/usr/bin/env python3
"""
Advanced Disaster Risk Reduction and resilience workflow.

Uses pandas, numpy, matplotlib, scikit-learn, and joblib.

Run:
    pip install -r requirements-advanced.txt
    python python/drr_resilience_advanced.py
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
STRATEGIES_PATH = ROOT / "data" / "raw" / "drr_resilience_strategies.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "drr_resilience_scenarios.csv"
SYSTEMS_PATH = ROOT / "data" / "raw" / "drr_resilience_systems.csv"
EVENTS_PATH = ROOT / "data" / "raw" / "disaster_stress_events.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_FIGURES = ROOT / "outputs" / "figures"
OUT_MODELS = ROOT / "outputs" / "models"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)
OUT_MODELS.mkdir(parents=True, exist_ok=True)

FEATURES = [
    "hazard_reduction",
    "exposure_reduction",
    "vulnerability_reduction",
    "capacity_enhancement",
    "justice_protection",
    "maladaptation_risk",
]


def calculate_strategy_profiles(strategies: pd.DataFrame) -> pd.DataFrame:
    out = strategies.copy()
    out["base_drr_value"] = (
        0.17 * out["hazard_reduction"]
        + 0.18 * out["exposure_reduction"]
        + 0.18 * out["vulnerability_reduction"]
        + 0.17 * out["capacity_enhancement"]
        + 0.18 * out["justice_protection"]
        - 0.12 * out["maladaptation_risk"]
    )
    out["justice_adjusted_value"] = out["base_drr_value"] * (0.72 + 0.028 * out["justice_protection"])

    conditions = [
        (out["base_drr_value"] >= 7.35) & (out["maladaptation_risk"] <= 2.7),
        out["maladaptation_risk"] >= 3.6,
        out["justice_protection"] < 7.5,
        out["capacity_enhancement"] < 7.2,
    ]
    choices = [
        "strong DRR and resilience profile with manageable maladaptation risk",
        "maladaptation review needed",
        "justice protection needs strengthening",
        "capacity constraint",
    ]
    out["diagnostic"] = np.select(conditions, choices, default="promising but requires scenario and implementation validation")
    return out


def score_strategies(strategies: pd.DataFrame, scenario: pd.Series) -> pd.DataFrame:
    result = strategies.copy()
    result["drr_value"] = (
        scenario["hazard_reduction_weight"] * result["hazard_reduction"]
        + scenario["exposure_reduction_weight"] * result["exposure_reduction"]
        + scenario["vulnerability_reduction_weight"] * result["vulnerability_reduction"]
        + scenario["capacity_enhancement_weight"] * result["capacity_enhancement"]
        + scenario["justice_protection_weight"] * result["justice_protection"]
        - scenario["maladaptation_risk_weight"] * result["maladaptation_risk"]
    )
    result = result.sort_values("drr_value", ascending=False).reset_index(drop=True)
    result["rank"] = np.arange(1, len(result) + 1)
    result["scenario"] = scenario["scenario"]
    return result


def scenario_rankings(strategies: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    return pd.concat([score_strategies(strategies, scenario) for _, scenario in scenarios.iterrows()], ignore_index=True)


def simulate_system_response(system: pd.Series, events: pd.DataFrame, seed: int = 42, time_steps: int = 80) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    function_level = system["baseline_function"]
    preparedness = system["preparedness_capacity"]
    recovery = system["recovery_capacity"]
    dependency = system["dependency_coupling"]
    justice_sensitivity = system["justice_sensitivity"]

    event_by_step = {
        12: events.iloc[0],
        28: events.iloc[1],
        43: events.iloc[2],
        59: events.iloc[3],
        70: events.iloc[4],
    }

    rows = []

    for t in range(time_steps):
        event = event_by_step.get(t)

        if event is not None:
            shock = event["shock_intensity"]
            slow = event["slow_stress"]
            compound = event["compound_risk"]
            cascade = event["cascading_dependency"]
            justice_burden = event["justice_burden"]
            event_name = event["event_name"]
        else:
            shock = 0.04 + rng.uniform(0.00, 0.02)
            slow = 0.16 + 0.0025 * t
            compound = 0.10
            cascade = 0.12
            justice_burden = 0.20
            event_name = "background risk stress"

        stress_load = (
            0.38 * shock
            + 0.20 * slow
            + 0.18 * compound
            + 0.16 * cascade
            + 0.08 * dependency
        )

        response_capacity = (
            0.45 * preparedness
            + 0.34 * recovery
            - 0.24 * system["hazard_exposure"]
            - 0.18 * system["vulnerability"]
            - 0.12 * dependency
        )
        response_capacity = np.clip(response_capacity, 0, 1)

        function_level = (
            function_level
            - 0.34 * stress_load
            + 0.23 * response_capacity
            + 0.13 * recovery
            - 0.07 * dependency
        )
        function_level = np.clip(function_level, 0, 1)

        dependency = np.clip(dependency + 0.018 * stress_load - 0.010 * response_capacity, 0, 1)
        justice_adjusted_function = function_level * (0.72 + 0.28 * (1.0 - justice_burden + justice_sensitivity * 0.45))
        justice_adjusted_function = np.clip(justice_adjusted_function, 0, 1)

        rows.append(
            {
                "system_id": system["system_id"],
                "system": system["system"],
                "system_domain": system["system_domain"],
                "time": t,
                "event": event_name,
                "stress_load": stress_load,
                "response_capacity": response_capacity,
                "function_level": function_level,
                "dependency_coupling": dependency,
                "justice_adjusted_function": justice_adjusted_function,
            }
        )

    return pd.DataFrame(rows)


def run_dynamic_simulations(systems: pd.DataFrame, events: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    simulation = pd.concat(
        [simulate_system_response(row, events, seed=100 + i) for i, row in systems.iterrows()],
        ignore_index=True,
    )

    summary = (
        simulation.groupby("system")
        .agg(
            mean_function=("function_level", "mean"),
            minimum_function=("function_level", "min"),
            final_function=("function_level", "last"),
            mean_justice_adjusted_function=("justice_adjusted_function", "mean"),
            maximum_dependency_coupling=("dependency_coupling", "max"),
            final_dependency_coupling=("dependency_coupling", "last"),
        )
        .reset_index()
        .sort_values("mean_justice_adjusted_function", ascending=False)
    )
    return simulation, summary


def strategy_monte_carlo(strategies: pd.DataFrame, scenario: pd.Series, n: int = 5000) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(42)
    rows = []

    for simulation_id in range(n):
        sampled = strategies.copy()
        for criterion in FEATURES:
            sampled[criterion] = rng.normal(loc=strategies[criterion], scale=0.6).clip(1, 10)

        scored = score_strategies(sampled, scenario)

        for _, row in scored.iterrows():
            rows.append(
                {
                    "simulation_id": simulation_id,
                    "strategy_id": row["strategy_id"],
                    "strategy": row["strategy"],
                    "rank": int(row["rank"]),
                    "drr_value": row["drr_value"],
                    "winner": scored.iloc[0]["strategy"],
                }
            )

    simulation = pd.DataFrame(rows)
    robustness = (
        simulation.groupby(["strategy_id", "strategy"])
        .agg(
            mean_drr_value=("drr_value", "mean"),
            median_drr_value=("drr_value", "median"),
            probability_ranked_first=("rank", lambda x: (x == 1).mean() * 100),
            probability_top_two=("rank", lambda x: (x <= 2).mean() * 100),
            probability_bottom_two=("rank", lambda x: (x >= len(strategies) - 1).mean() * 100),
        )
        .reset_index()
        .sort_values("probability_ranked_first", ascending=False)
    )
    return simulation, robustness


def expand_training(strategies: pd.DataFrame, n: int = 2600) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []

    for _ in range(n):
        base = strategies.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]
        record = {}

        for feature in FEATURES:
            record[feature] = float(np.clip(float(base[feature]) + rng.normal(0, 0.7), 1, 10))

        value = (
            0.17 * record["hazard_reduction"]
            + 0.18 * record["exposure_reduction"]
            + 0.18 * record["vulnerability_reduction"]
            + 0.17 * record["capacity_enhancement"]
            + 0.18 * record["justice_protection"]
            - 0.12 * record["maladaptation_risk"]
            + rng.normal(0, 0.18)
        )

        record["drr_value"] = value
        record["high_value_low_maladaptation"] = 1 if value >= 7.25 and record["maladaptation_risk"] <= 3.0 else 0
        rows.append(record)

    return pd.DataFrame(rows)


def plot_outputs(
    profiles: pd.DataFrame,
    rankings: pd.DataFrame,
    dynamic_simulation: pd.DataFrame,
    dynamic_summary: pd.DataFrame,
    robustness: pd.DataFrame,
    importance: pd.DataFrame | None = None,
) -> None:
    profile_plot = profiles[
        [
            "strategy",
            "base_drr_value",
            "hazard_reduction",
            "exposure_reduction",
            "vulnerability_reduction",
            "capacity_enhancement",
            "justice_protection",
            "maladaptation_risk",
        ]
    ].melt(id_vars="strategy", var_name="criterion", value_name="value")

    order = profiles.sort_values("base_drr_value")["strategy"].tolist()

    plt.figure(figsize=(11, 7))
    for criterion, subset in profile_plot.groupby("criterion"):
        y = [order.index(p) for p in subset["strategy"]]
        plt.scatter(subset["value"], y, label=criterion, s=50)
    plt.yticks(range(len(order)), order)
    plt.xlabel("Criterion value")
    plt.title("DRR and Resilience Strategy Profiles")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "drr_resilience_strategy_profiles.png", dpi=160)
    plt.close()

    pivot = rankings.pivot(index="strategy", columns="scenario", values="drr_value")
    plt.figure(figsize=(11, 7))
    for scenario in pivot.columns:
        plt.plot(pivot.index, pivot[scenario], marker="o", label=scenario)
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("DRR value")
    plt.title("DRR Strategy Value Across Priorities")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "drr_resilience_scenario_rankings.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    for system, subset in dynamic_simulation.groupby("system"):
        plt.plot(subset["time"], subset["function_level"], label=system)
    plt.xlabel("Time")
    plt.ylabel("System function")
    plt.title("System Function Under Disaster Stress")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "system_function_under_disaster_stress.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(dynamic_summary["system"], dynamic_summary["mean_justice_adjusted_function"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Mean justice-adjusted function")
    plt.title("Justice-Adjusted Function by System")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "justice_adjusted_function_by_system.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(robustness["strategy"], robustness["probability_ranked_first"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Probability ranked first (%)")
    plt.title("Robustness of DRR Strategies")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "monte_carlo_probability_ranked_first.png", dpi=160)
    plt.close()

    if importance is not None:
        plt.figure(figsize=(10, 6))
        plt.barh(importance["feature"], importance["importance"])
        plt.gca().invert_yaxis()
        plt.xlabel("Importance")
        plt.title("Feature Importance for DRR Classification")
        plt.tight_layout()
        plt.savefig(OUT_FIGURES / "advanced_feature_importance.png", dpi=160)
        plt.close()


def main() -> None:
    strategies = pd.read_csv(STRATEGIES_PATH)
    scenarios = pd.read_csv(SCENARIOS_PATH)
    systems = pd.read_csv(SYSTEMS_PATH)
    events = pd.read_csv(EVENTS_PATH)

    profiles = calculate_strategy_profiles(strategies)
    rankings = scenario_rankings(strategies, scenarios)
    dynamic_simulation, dynamic_summary = run_dynamic_simulations(systems, events)

    baseline = scenarios.loc[scenarios["scenario"] == "Balanced"].iloc[0]
    strategy_simulation, robustness = strategy_monte_carlo(strategies, baseline, n=5000)

    profiles.to_csv(OUT_TABLES / "drr_resilience_strategy_profiles_advanced.csv", index=False)
    rankings.to_csv(OUT_TABLES / "drr_resilience_strategy_rankings_advanced.csv", index=False)
    dynamic_simulation.to_csv(OUT_TABLES / "drr_resilience_dynamic_simulation_advanced.csv", index=False)
    dynamic_summary.to_csv(OUT_TABLES / "drr_resilience_dynamic_summary_advanced.csv", index=False)
    strategy_simulation.to_csv(OUT_TABLES / "drr_resilience_monte_carlo_advanced.csv", index=False)
    robustness.to_csv(OUT_TABLES / "drr_resilience_robustness_summary_advanced.csv", index=False)

    training = expand_training(strategies)
    X = training[FEATURES]
    y = training["high_value_low_maladaptation"]

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
            "model": "random_forest_drr_resilience_classifier",
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

    training.to_csv(OUT_TABLES / "synthetic_drr_resilience_training_data.csv", index=False)
    metrics.to_csv(OUT_TABLES / "advanced_drr_resilience_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "drr_resilience_classifier.joblib")

    plot_outputs(profiles, rankings, dynamic_simulation, dynamic_summary, robustness, importance)

    print("Advanced DRR and resilience workflow complete.")
    print("Strategy profile summary:")
    print(profiles[["strategy", "base_drr_value", "justice_adjusted_value", "diagnostic"]].round(4))
    print("Model metrics:")
    print(metrics.round(4))


if __name__ == "__main__":
    main()
