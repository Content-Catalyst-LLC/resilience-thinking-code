#!/usr/bin/env python3
"""
Advanced Infrastructure Resilience workflow.

Uses pandas, numpy, matplotlib, scikit-learn, and joblib.

Run:
    pip install -r requirements-advanced.txt
    python python/infrastructure_resilience_advanced.py
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
STRATEGIES_PATH = ROOT / "data" / "raw" / "infrastructure_resilience_strategies.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "infrastructure_resilience_scenarios.csv"
SYSTEMS_PATH = ROOT / "data" / "raw" / "infrastructure_systems.csv"
EVENTS_PATH = ROOT / "data" / "raw" / "infrastructure_stress_events.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_FIGURES = ROOT / "outputs" / "figures"
OUT_MODELS = ROOT / "outputs" / "models"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)
OUT_MODELS.mkdir(parents=True, exist_ok=True)

FEATURES = [
    "service_continuity",
    "redundancy",
    "recovery_speed",
    "adaptive_capacity",
    "equity_protection",
    "cascading_exposure",
]


def calculate_strategy_profiles(strategies: pd.DataFrame) -> pd.DataFrame:
    out = strategies.copy()
    out["base_resilience_value"] = (
        0.22 * out["service_continuity"]
        + 0.20 * out["redundancy"]
        + 0.18 * out["recovery_speed"]
        + 0.16 * out["adaptive_capacity"]
        + 0.16 * out["equity_protection"]
        - 0.08 * out["cascading_exposure"]
    )
    out["equity_adjusted_value"] = out["base_resilience_value"] * (0.72 + 0.028 * out["equity_protection"])

    conditions = [
        (out["base_resilience_value"] >= 7.45) & (out["cascading_exposure"] <= 3.6),
        out["cascading_exposure"] >= 4.0,
        out["equity_protection"] < 7.8,
        out["redundancy"] < 7.8,
        out["adaptive_capacity"] < 8.0,
    ]
    choices = [
        "strong infrastructure resilience profile with manageable cascade risk",
        "cascade review needed",
        "equity protection needs strengthening",
        "redundancy constraint",
        "adaptive capacity constraint",
    ]
    out["diagnostic"] = np.select(conditions, choices, default="promising but requires infrastructure scenario validation")
    return out


def score_strategies(strategies: pd.DataFrame, scenario: pd.Series) -> pd.DataFrame:
    result = strategies.copy()
    result["resilience_value"] = (
        scenario["service_continuity_weight"] * result["service_continuity"]
        + scenario["redundancy_weight"] * result["redundancy"]
        + scenario["recovery_speed_weight"] * result["recovery_speed"]
        + scenario["adaptive_capacity_weight"] * result["adaptive_capacity"]
        + scenario["equity_protection_weight"] * result["equity_protection"]
        - scenario["cascading_exposure_weight"] * result["cascading_exposure"]
    )
    result = result.sort_values("resilience_value", ascending=False).reset_index(drop=True)
    result["rank"] = np.arange(1, len(result) + 1)
    result["scenario"] = scenario["scenario"]
    return result


def scenario_rankings(strategies: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    return pd.concat([score_strategies(strategies, scenario) for _, scenario in scenarios.iterrows()], ignore_index=True)


def simulate_service_response(system: pd.Series, events: pd.DataFrame, seed: int = 42, time_steps: int = 80) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    service_level = system["baseline_service"]
    redundancy = system["redundancy_capacity"]
    recovery = system["recovery_capacity"]
    adaptive = system["adaptive_capacity"]
    interdependence = system["interdependence_coupling"]
    equity_sensitivity = system["equity_sensitivity"]

    event_by_step = {
        12: events.iloc[0],
        27: events.iloc[1],
        42: events.iloc[2],
        56: events.iloc[3],
        70: events.iloc[4],
    }

    rows = []

    for t in range(time_steps):
        event = event_by_step.get(t)

        if event is not None:
            shock = event["shock_intensity"]
            chronic = event["chronic_stress"]
            compound = event["compound_risk"]
            cascade = event["cascading_dependency"]
            equity_burden = event["equity_burden"]
            event_name = event["event_name"]
        else:
            shock = 0.04 + rng.uniform(0.00, 0.02)
            chronic = 0.14 + 0.0028 * t
            compound = 0.10
            cascade = 0.12
            equity_burden = 0.20
            event_name = "background infrastructure stress"

        stress_load = (
            0.34 * shock
            + 0.18 * chronic
            + 0.18 * compound
            + 0.18 * cascade
            + 0.12 * interdependence
        )

        response_capacity = (
            0.33 * redundancy
            + 0.30 * recovery
            + 0.24 * adaptive
            - 0.20 * system["shock_exposure"]
            - 0.12 * system["chronic_stress"]
            - 0.16 * interdependence
        )
        response_capacity = np.clip(response_capacity, 0, 1)

        service_level = (
            service_level
            - 0.32 * stress_load
            + 0.20 * response_capacity
            + 0.12 * recovery
            + 0.08 * adaptive
            - 0.08 * interdependence
        )
        service_level = np.clip(service_level, 0, 1)

        interdependence = np.clip(interdependence + 0.020 * stress_load - 0.012 * response_capacity, 0, 1)
        equity_adjusted_service = service_level * (0.72 + 0.28 * (1.0 - equity_burden + equity_sensitivity * 0.40))
        equity_adjusted_service = np.clip(equity_adjusted_service, 0, 1)

        rows.append(
            {
                "system_id": system["system_id"],
                "system": system["system"],
                "system_domain": system["system_domain"],
                "time": t,
                "event": event_name,
                "stress_load": stress_load,
                "response_capacity": response_capacity,
                "service_level": service_level,
                "interdependence_coupling": interdependence,
                "equity_adjusted_service": equity_adjusted_service,
            }
        )

    return pd.DataFrame(rows)


def run_dynamic_simulations(systems: pd.DataFrame, events: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    simulation = pd.concat(
        [simulate_service_response(row, events, seed=100 + i) for i, row in systems.iterrows()],
        ignore_index=True,
    )

    summary = (
        simulation.groupby("system")
        .agg(
            mean_service_level=("service_level", "mean"),
            minimum_service_level=("service_level", "min"),
            final_service_level=("service_level", "last"),
            mean_equity_adjusted_service=("equity_adjusted_service", "mean"),
            maximum_interdependence_coupling=("interdependence_coupling", "max"),
            final_interdependence_coupling=("interdependence_coupling", "last"),
        )
        .reset_index()
        .sort_values("mean_equity_adjusted_service", ascending=False)
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
                    "resilience_value": row["resilience_value"],
                    "winner": scored.iloc[0]["strategy"],
                }
            )

    simulation = pd.DataFrame(rows)
    robustness = (
        simulation.groupby(["strategy_id", "strategy"])
        .agg(
            mean_resilience_value=("resilience_value", "mean"),
            median_resilience_value=("resilience_value", "median"),
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
            0.22 * record["service_continuity"]
            + 0.20 * record["redundancy"]
            + 0.18 * record["recovery_speed"]
            + 0.16 * record["adaptive_capacity"]
            + 0.16 * record["equity_protection"]
            - 0.08 * record["cascading_exposure"]
            + rng.normal(0, 0.18)
        )

        record["resilience_value"] = value
        record["high_value_low_cascade"] = 1 if value >= 7.35 and record["cascading_exposure"] <= 3.7 else 0
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
            "base_resilience_value",
            "service_continuity",
            "redundancy",
            "recovery_speed",
            "adaptive_capacity",
            "equity_protection",
            "cascading_exposure",
        ]
    ].melt(id_vars="strategy", var_name="criterion", value_name="value")

    order = profiles.sort_values("base_resilience_value")["strategy"].tolist()

    plt.figure(figsize=(11, 7))
    for criterion, subset in profile_plot.groupby("criterion"):
        y = [order.index(p) for p in subset["strategy"]]
        plt.scatter(subset["value"], y, label=criterion, s=50)
    plt.yticks(range(len(order)), order)
    plt.xlabel("Criterion value")
    plt.title("Infrastructure Resilience Strategy Profiles")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "infrastructure_resilience_strategy_profiles.png", dpi=160)
    plt.close()

    pivot = rankings.pivot(index="strategy", columns="scenario", values="resilience_value")
    plt.figure(figsize=(11, 7))
    for scenario in pivot.columns:
        plt.plot(pivot.index, pivot[scenario], marker="o", label=scenario)
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Resilience value")
    plt.title("Infrastructure Resilience Strategy Value Across Priorities")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "infrastructure_resilience_scenario_rankings.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    for system, subset in dynamic_simulation.groupby("system"):
        plt.plot(subset["time"], subset["service_level"], label=system)
    plt.xlabel("Time")
    plt.ylabel("Service level")
    plt.title("Infrastructure Service Level Under Stress")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "infrastructure_service_under_stress.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(dynamic_summary["system"], dynamic_summary["mean_equity_adjusted_service"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Mean equity-adjusted service")
    plt.title("Equity-Adjusted Service by Infrastructure System")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "equity_adjusted_service_by_system.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(robustness["strategy"], robustness["probability_ranked_first"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Probability ranked first (%)")
    plt.title("Robustness of Infrastructure Resilience Strategies")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "monte_carlo_probability_ranked_first.png", dpi=160)
    plt.close()

    if importance is not None:
        plt.figure(figsize=(10, 6))
        plt.barh(importance["feature"], importance["importance"])
        plt.gca().invert_yaxis()
        plt.xlabel("Importance")
        plt.title("Feature Importance for Infrastructure Resilience Classification")
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

    profiles.to_csv(OUT_TABLES / "infrastructure_resilience_strategy_profiles_advanced.csv", index=False)
    rankings.to_csv(OUT_TABLES / "infrastructure_resilience_strategy_rankings_advanced.csv", index=False)
    dynamic_simulation.to_csv(OUT_TABLES / "infrastructure_service_dynamic_simulation_advanced.csv", index=False)
    dynamic_summary.to_csv(OUT_TABLES / "infrastructure_service_dynamic_summary_advanced.csv", index=False)
    strategy_simulation.to_csv(OUT_TABLES / "infrastructure_resilience_monte_carlo_advanced.csv", index=False)
    robustness.to_csv(OUT_TABLES / "infrastructure_resilience_robustness_summary_advanced.csv", index=False)

    training = expand_training(strategies)
    X = training[FEATURES]
    y = training["high_value_low_cascade"]

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
            "model": "random_forest_infrastructure_resilience_classifier",
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

    training.to_csv(OUT_TABLES / "synthetic_infrastructure_resilience_training_data.csv", index=False)
    metrics.to_csv(OUT_TABLES / "advanced_infrastructure_resilience_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "infrastructure_resilience_classifier.joblib")

    plot_outputs(profiles, rankings, dynamic_simulation, dynamic_summary, robustness, importance)

    print("Advanced infrastructure resilience workflow complete.")
    print("Strategy profile summary:")
    print(profiles[["strategy", "base_resilience_value", "equity_adjusted_value", "diagnostic"]].round(4))
    print("Model metrics:")
    print(metrics.round(4))


if __name__ == "__main__":
    main()
