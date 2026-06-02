#!/usr/bin/env python3
"""
Advanced modularity and cascading failure workflow.

Uses pandas, numpy, matplotlib, scikit-learn, and joblib.

Run:
    pip install -r requirements-advanced.txt
    python python/modularity_cascade_advanced.py
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
NODES_PATH = ROOT / "data" / "raw" / "cascade_nodes.csv"
EDGES_PATH = ROOT / "data" / "raw" / "cascade_edges.csv"
STRATEGIES_PATH = ROOT / "data" / "raw" / "containment_strategies.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "containment_scenarios.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_FIGURES = ROOT / "outputs" / "figures"
OUT_MODELS = ROOT / "outputs" / "models"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)
OUT_MODELS.mkdir(parents=True, exist_ok=True)

BENEFIT_CRITERIA = [
    "modularity",
    "redundancy",
    "dependency_mapping",
    "isolation_capacity",
    "coordination_readiness",
    "justice_protection",
]

FEATURES = BENEFIT_CRITERIA + ["common_mode_risk"]


def calculate_strategy_profiles(strategies: pd.DataFrame) -> pd.DataFrame:
    out = strategies.copy()
    out["base_containment_value"] = (
        0.18 * out["modularity"]
        + 0.16 * out["redundancy"]
        + 0.16 * out["dependency_mapping"]
        + 0.18 * out["isolation_capacity"]
        + 0.14 * out["coordination_readiness"]
        + 0.10 * out["justice_protection"]
        - 0.08 * out["common_mode_risk"]
    )

    conditions = [
        (out["base_containment_value"] >= 7.15) & (out["common_mode_risk"] <= 3.6),
        out["common_mode_risk"] >= 4.0,
        out["coordination_readiness"] < 7.5,
        out["justice_protection"] < 7.5,
    ]
    choices = [
        "strong containment profile with manageable common-mode risk",
        "common-mode failure review needed",
        "coordination readiness constraint",
        "justice protection needs strengthening",
    ]
    out["diagnostic"] = np.select(conditions, choices, default="promising but requires stress testing and dependency validation")
    return out


def simulate_one_cascade(initial_failure: str, nodes: pd.DataFrame, edges: pd.DataFrame, rng: np.random.Generator, max_steps: int = 7) -> dict:
    failed = {initial_failure}

    for step in range(max_steps):
        new_failures = set()
        active_edges = edges[edges["source"].isin(failed)]

        for _, edge in active_edges.iterrows():
            target = edge["target"]
            if target in failed:
                continue

            target_row = nodes[nodes["node"] == target].iloc[0]
            probability = (
                edge["coupling_strength"]
                + 0.35 * target_row["common_mode_exposure"]
                - 0.30 * target_row["redundancy"]
                - 0.25 * target_row["isolation_capacity"]
            )
            probability = float(np.clip(probability, 0.02, 0.95))

            if rng.random() < probability:
                new_failures.add(target)

        failed = failed.union(new_failures)

        if not new_failures:
            break

    failed_nodes = sorted(failed)
    impact = nodes[nodes["node"].isin(failed_nodes)]["justice_sensitivity"].sum()

    return {
        "initial_failure": initial_failure,
        "final_failures": len(failed_nodes),
        "cascade_steps": step + 1,
        "justice_weighted_impact": impact,
        "failed_nodes": "; ".join(failed_nodes),
    }


def run_cascade_monte_carlo(nodes: pd.DataFrame, edges: pd.DataFrame, n: int = 5000) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []

    for _, node in nodes.iterrows():
        initial = node["node"]
        for simulation_id in range(n):
            rng = np.random.default_rng(simulation_id + 1000 * int(str(node["node_id"])[1:]))
            result = simulate_one_cascade(initial, nodes, edges, rng)
            result["simulation_id"] = simulation_id
            rows.append(result)

    simulation = pd.DataFrame(rows)

    summary = (
        simulation.groupby("initial_failure")
        .agg(
            mean_final_failures=("final_failures", "mean"),
            median_final_failures=("final_failures", "median"),
            probability_large_cascade=("final_failures", lambda x: (x >= 5).mean() * 100),
            mean_justice_weighted_impact=("justice_weighted_impact", "mean"),
            max_justice_weighted_impact=("justice_weighted_impact", "max"),
        )
        .reset_index()
        .merge(nodes[["node", "system_domain", "critical_function"]], left_on="initial_failure", right_on="node", how="left")
        .drop(columns=["node"])
        .sort_values("probability_large_cascade", ascending=False)
    )

    return simulation, summary


def score_strategies(strategies: pd.DataFrame, scenario: pd.Series) -> pd.DataFrame:
    result = strategies.copy()
    result["containment_value"] = (
        scenario["modularity_weight"] * result["modularity"]
        + scenario["redundancy_weight"] * result["redundancy"]
        + scenario["dependency_mapping_weight"] * result["dependency_mapping"]
        + scenario["isolation_capacity_weight"] * result["isolation_capacity"]
        + scenario["coordination_readiness_weight"] * result["coordination_readiness"]
        + scenario["justice_protection_weight"] * result["justice_protection"]
        - scenario["common_mode_risk_weight"] * result["common_mode_risk"]
    )
    result = result.sort_values("containment_value", ascending=False).reset_index(drop=True)
    result["rank"] = np.arange(1, len(result) + 1)
    result["scenario"] = scenario["scenario"]
    return result


def scenario_rankings(strategies: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, scenario in scenarios.iterrows():
        rows.append(score_strategies(strategies, scenario))
    return pd.concat(rows, ignore_index=True)


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
                    "containment_value": row["containment_value"],
                    "winner": scored.iloc[0]["strategy"],
                }
            )

    simulation = pd.DataFrame(rows)

    robustness = (
        simulation.groupby(["strategy_id", "strategy"])
        .agg(
            mean_containment_value=("containment_value", "mean"),
            median_containment_value=("containment_value", "median"),
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
            0.18 * record["modularity"]
            + 0.16 * record["redundancy"]
            + 0.16 * record["dependency_mapping"]
            + 0.18 * record["isolation_capacity"]
            + 0.14 * record["coordination_readiness"]
            + 0.10 * record["justice_protection"]
            - 0.08 * record["common_mode_risk"]
            + rng.normal(0, 0.18)
        )

        record["containment_value"] = value
        record["high_containment_manageable_common_mode"] = 1 if value >= 7.10 and record["common_mode_risk"] <= 3.8 else 0
        rows.append(record)

    return pd.DataFrame(rows)


def plot_outputs(
    profiles: pd.DataFrame,
    cascade_summary: pd.DataFrame,
    rankings: pd.DataFrame,
    robustness: pd.DataFrame,
    importance: pd.DataFrame | None = None,
) -> None:
    profile_plot = profiles[
        [
            "strategy",
            "base_containment_value",
            "modularity",
            "redundancy",
            "dependency_mapping",
            "isolation_capacity",
            "coordination_readiness",
            "justice_protection",
            "common_mode_risk",
        ]
    ].melt(id_vars="strategy", var_name="criterion", value_name="value")

    order = profiles.sort_values("base_containment_value")["strategy"].tolist()

    plt.figure(figsize=(11, 7))
    for criterion, subset in profile_plot.groupby("criterion"):
        y = [order.index(p) for p in subset["strategy"]]
        plt.scatter(subset["value"], y, label=criterion, s=50)
    plt.yticks(range(len(order)), order)
    plt.xlabel("Criterion value")
    plt.title("Modularity and Cascade-Containment Strategy Profiles")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "cascade_containment_strategy_profiles.png", dpi=160)
    plt.close()

    pivot = rankings.pivot(index="strategy", columns="scenario", values="containment_value")
    plt.figure(figsize=(11, 7))
    for scenario in pivot.columns:
        plt.plot(pivot.index, pivot[scenario], marker="o", label=scenario)
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Containment value")
    plt.title("Containment Strategy Value Across Priorities")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "cascade_containment_scenario_rankings.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(cascade_summary["initial_failure"], cascade_summary["probability_large_cascade"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Probability of large cascade (%)")
    plt.title("Cascade Risk by Initial Failure Node")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "cascade_probability_by_initial_failure.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(cascade_summary["initial_failure"], cascade_summary["mean_justice_weighted_impact"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Mean justice-weighted impact")
    plt.title("Justice-Weighted Impact by Initial Failure Node")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "cascade_justice_weighted_impact.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(robustness["strategy"], robustness["probability_ranked_first"])
    plt.xticks(rotation=25, ha="right")
    plt.ylabel("Probability ranked first (%)")
    plt.title("Robustness of Cascade-Containment Strategies")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "monte_carlo_probability_ranked_first.png", dpi=160)
    plt.close()

    if importance is not None:
        plt.figure(figsize=(10, 6))
        plt.barh(importance["feature"], importance["importance"])
        plt.gca().invert_yaxis()
        plt.xlabel("Importance")
        plt.title("Feature Importance for Containment Strategy Classification")
        plt.tight_layout()
        plt.savefig(OUT_FIGURES / "advanced_feature_importance.png", dpi=160)
        plt.close()


def main() -> None:
    nodes = pd.read_csv(NODES_PATH)
    edges = pd.read_csv(EDGES_PATH)
    strategies = pd.read_csv(STRATEGIES_PATH)
    scenarios = pd.read_csv(SCENARIOS_PATH)

    profiles = calculate_strategy_profiles(strategies)
    cascade_simulation, cascade_summary = run_cascade_monte_carlo(nodes, edges, n=5000)
    rankings = scenario_rankings(strategies, scenarios)
    baseline = scenarios.loc[scenarios["scenario"] == "Balanced"].iloc[0]
    strategy_simulation, robustness = strategy_monte_carlo(strategies, baseline, n=5000)

    profiles.to_csv(OUT_TABLES / "modularity_cascade_strategy_profiles_advanced.csv", index=False)
    cascade_simulation.to_csv(OUT_TABLES / "cascade_monte_carlo_advanced.csv", index=False)
    cascade_summary.to_csv(OUT_TABLES / "cascade_summary_advanced.csv", index=False)
    rankings.to_csv(OUT_TABLES / "containment_strategy_rankings_advanced.csv", index=False)
    strategy_simulation.to_csv(OUT_TABLES / "containment_strategy_monte_carlo_advanced.csv", index=False)
    robustness.to_csv(OUT_TABLES / "containment_strategy_robustness_summary_advanced.csv", index=False)

    training = expand_training(strategies)
    X = training[FEATURES]
    y = training["high_containment_manageable_common_mode"]

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
            "model": "random_forest_cascade_containment_classifier",
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

    training.to_csv(OUT_TABLES / "synthetic_cascade_containment_training_data.csv", index=False)
    metrics.to_csv(OUT_TABLES / "advanced_cascade_containment_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "cascade_containment_classifier.joblib")

    plot_outputs(profiles, cascade_summary, rankings, robustness, importance)

    print("Advanced modularity and cascade workflow complete.")
    print("Highest cascade-risk nodes:")
    print(cascade_summary[["initial_failure", "probability_large_cascade", "mean_justice_weighted_impact"]].head().round(4))
    print("Model metrics:")
    print(metrics.round(4))


if __name__ == "__main__":
    main()
