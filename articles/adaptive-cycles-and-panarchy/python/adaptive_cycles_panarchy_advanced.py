#!/usr/bin/env python3
"""
Advanced adaptive-cycle and panarchy workflow.

Uses pandas, numpy, matplotlib, scikit-learn, and joblib.

Run:
    pip install -r requirements-advanced.txt
    python python/adaptive_cycles_panarchy_advanced.py
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
SYSTEMS_PATH = ROOT / "data" / "raw" / "system_cycle_profiles.csv"
SCALES_PATH = ROOT / "data" / "raw" / "panarchy_scale_profiles.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "cycle_scenarios.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_FIGURES = ROOT / "outputs" / "figures"
OUT_MODELS = ROOT / "outputs" / "models"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)
OUT_MODELS.mkdir(parents=True, exist_ok=True)

FEATURES = [
    "potential",
    "connectedness",
    "resilience",
    "rigidity",
    "memory",
    "novelty",
    "disturbance_exposure",
]


def phase_diagnostic(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["release_risk_index"] = (
        0.30 * out["rigidity"]
        + 0.24 * out["connectedness"]
        + 0.20 * out["disturbance_exposure"]
        + 0.16 * (1 - out["resilience"])
        + 0.10 * (1 - out["novelty"])
    )
    out["renewal_potential_index"] = (
        0.26 * out["memory"]
        + 0.24 * out["novelty"]
        + 0.20 * out["resilience"]
        + 0.16 * (1 - out["rigidity"])
        + 0.14 * out["potential"]
    )
    conditions = [
        (out["initial_phase"] == "K") & (out["release_risk_index"] >= 0.62),
        (out["initial_phase"] == "alpha") & (out["renewal_potential_index"] >= 0.58),
        (out["initial_phase"] == "r") & (out["novelty"] >= 0.35),
    ]
    choices = [
        "conservation-phase brittleness concern",
        "strong reorganization potential",
        "high experimentation and growth potential",
    ]
    out["diagnostic"] = np.select(conditions, choices, default="mixed adaptive-cycle profile requiring monitoring")
    return out


def update_cycle(state: dict, scenario: pd.Series, rng: np.random.Generator, memory_input: float = 0.0) -> dict:
    phase = state["phase"]

    if phase in ["r", "K"]:
        state["potential"] = min(
            1.0,
            state["potential"] + float(scenario["growth_rate"]) * state["potential"] * (1 - state["potential"])
        )
        state["connectedness"] = min(
            1.0,
            state["connectedness"] + float(scenario["connect_rate"]) * (1 - state["connectedness"])
        )
        state["rigidity"] = min(
            1.0,
            state["rigidity"] + 0.050 * state["connectedness"] + 0.020 * float(scenario["disturbance_pressure"])
        )
        state["resilience"] = max(
            0.0,
            1.0 - 0.62 * state["connectedness"] - 0.34 * state["rigidity"] - 0.12 * float(scenario["disturbance_pressure"])
        )
        state["memory"] = min(1.0, state["memory"] + 0.012 * state["potential"])
        state["novelty"] = max(0.02, 0.25 * (1 - state["connectedness"]))
        state["phase"] = "K" if state["connectedness"] > 0.55 else "r"

        if state["rigidity"] > float(scenario["rigidity_threshold"]) and state["resilience"] < float(scenario["resilience_threshold"]):
            state["phase"] = "Omega"

    elif phase == "Omega":
        state["potential"] = max(0.05, state["potential"] * 0.42)
        state["connectedness"] = max(0.08, state["connectedness"] * 0.32)
        state["rigidity"] = max(0.05, state["rigidity"] * 0.38)
        state["resilience"] = min(1.0, state["resilience"] + 0.30)
        state["memory"] = max(0.20, state["memory"] * 0.86)
        state["novelty"] = rng.uniform(float(scenario["novelty_range_high"]), min(0.50, float(scenario["novelty_range_high"]) + 0.16))
        state["phase"] = "alpha"

    elif phase == "alpha":
        state["novelty"] = rng.uniform(float(scenario["novelty_range_low"]), float(scenario["novelty_range_high"]))
        state["potential"] = min(
            1.0,
            float(scenario["memory_strength"]) * state["memory"] + memory_input + state["novelty"]
        )
        state["connectedness"] = min(1.0, state["connectedness"] + rng.uniform(0.015, 0.045))
        state["rigidity"] = max(0.03, state["rigidity"] + rng.uniform(-0.020, 0.015))
        state["resilience"] = min(1.0, state["resilience"] + rng.uniform(0.025, 0.075))
        state["memory"] = min(1.0, state["memory"] + rng.uniform(-0.015, 0.025))
        state["phase"] = "r" if state["potential"] > 0.32 and state["connectedness"] < 0.50 else "alpha"

    return state


def simulate_systems(profiles: pd.DataFrame, scenarios: pd.DataFrame, steps: int = 120) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []

    for _, scenario in scenarios.iterrows():
        for _, system in profiles.iterrows():
            state = {
                "phase": system["initial_phase"],
                "potential": float(system["potential"]),
                "connectedness": float(system["connectedness"]),
                "resilience": float(system["resilience"]),
                "rigidity": float(system["rigidity"]),
                "memory": float(system["memory"]),
                "novelty": float(system["novelty"]),
            }

            for t in range(1, steps + 1):
                previous_phase = state["phase"]
                state = update_cycle(state, scenario, rng)

                rows.append(
                    {
                        "system_id": system["system_id"],
                        "system_name": system["system_name"],
                        "system_type": system["system_type"],
                        "scenario_id": scenario["scenario_id"],
                        "scenario_name": scenario["scenario_name"],
                        "time": t,
                        "phase": state["phase"],
                        "phase_changed": state["phase"] != previous_phase,
                        "potential": state["potential"],
                        "connectedness": state["connectedness"],
                        "resilience": state["resilience"],
                        "rigidity": state["rigidity"],
                        "memory": state["memory"],
                        "novelty": state["novelty"],
                        "release_flag": 1 if state["phase"] == "Omega" else 0,
                    }
                )

    return pd.DataFrame(rows)


def simulate_panarchy(scales: pd.DataFrame, scenarios: pd.DataFrame, steps: int = 120) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []

    systems = scales["system_id"].unique()

    for system_id in systems:
        system_scales = scales[scales["system_id"] == system_id]
        if not {"fast", "slow"}.issubset(set(system_scales["scale_speed"])):
            continue

        fast_row = system_scales[system_scales["scale_speed"] == "fast"].iloc[0]
        slow_row = system_scales[system_scales["scale_speed"] == "slow"].iloc[0]

        for _, scenario in scenarios.iterrows():
            fast = {
                "phase": "r" if float(fast_row["connectedness"]) < 0.55 else "K",
                "potential": float(fast_row["potential"]),
                "connectedness": float(fast_row["connectedness"]),
                "resilience": float(fast_row["resilience"]),
                "rigidity": float(fast_row["rigidity"]),
                "memory": float(fast_row["memory"]),
                "novelty": float(fast_row["innovation_capacity"]),
            }
            slow = {
                "phase": "K",
                "potential": float(slow_row["potential"]),
                "connectedness": float(slow_row["connectedness"]),
                "resilience": float(slow_row["resilience"]),
                "rigidity": float(slow_row["rigidity"]),
                "memory": float(slow_row["memory"]),
                "novelty": float(slow_row["innovation_capacity"]),
            }

            for t in range(1, steps + 1):
                previous_fast_phase = fast["phase"]
                previous_slow_phase = slow["phase"]

                remember_effect = float(scenario["remember_strength"]) * slow["memory"] if fast["phase"] == "alpha" else 0.0
                fast = update_cycle(fast, scenario, rng, memory_input=remember_effect)

                revolt_effect = 0.0
                if fast["phase"] == "Omega" and slow["connectedness"] > 0.72 and slow["resilience"] < 0.42:
                    revolt_effect = float(scenario["revolt_strength"])

                slow["rigidity"] = min(1.0, slow["rigidity"] + revolt_effect)
                slow = update_cycle(slow, scenario, rng)

                rows.append(
                    {
                        "system_id": system_id,
                        "fast_scale": fast_row["scale_name"],
                        "slow_scale": slow_row["scale_name"],
                        "scenario_id": scenario["scenario_id"],
                        "scenario_name": scenario["scenario_name"],
                        "time": t,
                        "fast_phase": fast["phase"],
                        "slow_phase": slow["phase"],
                        "fast_potential": fast["potential"],
                        "fast_connectedness": fast["connectedness"],
                        "fast_resilience": fast["resilience"],
                        "fast_rigidity": fast["rigidity"],
                        "fast_memory": fast["memory"],
                        "slow_potential": slow["potential"],
                        "slow_connectedness": slow["connectedness"],
                        "slow_resilience": slow["resilience"],
                        "slow_rigidity": slow["rigidity"],
                        "slow_memory": slow["memory"],
                        "revolt_effect": revolt_effect,
                        "remember_effect": remember_effect,
                        "fast_phase_changed": fast["phase"] != previous_fast_phase,
                        "slow_phase_changed": slow["phase"] != previous_slow_phase,
                    }
                )

    return pd.DataFrame(rows)


def expand_training(profiles: pd.DataFrame, n: int = 2200) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []

    for _ in range(n):
        base = profiles.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]
        record = {}

        for feature in FEATURES:
            record[feature] = float(np.clip(float(base[feature]) + rng.normal(0, 0.08), 0.03, 0.98))

        release_risk = (
            0.30 * record["rigidity"]
            + 0.24 * record["connectedness"]
            + 0.20 * record["disturbance_exposure"]
            + 0.16 * (1 - record["resilience"])
            + 0.10 * (1 - record["novelty"])
            + rng.normal(0, 0.035)
        )

        record["release_risk_index"] = release_risk
        record["release_risk"] = 1 if release_risk > 0.62 else 0
        rows.append(record)

    return pd.DataFrame(rows)


def plot_outputs(profiles: pd.DataFrame, cycle_sim: pd.DataFrame, panarchy_sim: pd.DataFrame) -> None:
    profile_plot = profiles[
        ["system_name", "release_risk_index", "renewal_potential_index", "rigidity", "resilience", "memory", "novelty"]
    ].melt(id_vars="system_name", var_name="indicator", value_name="value")

    order = profiles.sort_values("release_risk_index")["system_name"].tolist()
    plt.figure(figsize=(10, 6))
    for indicator, subset in profile_plot.groupby("indicator"):
        y = [order.index(s) for s in subset["system_name"]]
        plt.scatter(subset["value"], y, label=indicator, s=50)
    plt.yticks(range(len(order)), order)
    plt.xlabel("Indicator value")
    plt.title("Adaptive-Cycle Release Risk and Renewal Potential")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "adaptive_cycle_release_renewal_profiles.png", dpi=160)
    plt.close()

    scenario = "Rigidity and lock-in"
    subset = cycle_sim[(cycle_sim["scenario_name"] == scenario) & (cycle_sim["system_name"] == "Urban Stormwater System")]
    if not subset.empty:
        plt.figure(figsize=(10, 6))
        for col in ["potential", "connectedness", "resilience", "rigidity", "memory", "novelty"]:
            plt.plot(subset["time"], subset[col], label=col)
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.title("Adaptive-Cycle State Variables: Urban Stormwater System")
        plt.legend(fontsize=8)
        plt.tight_layout()
        plt.savefig(OUT_FIGURES / "adaptive_cycle_state_variables.png", dpi=160)
        plt.close()

    if not panarchy_sim.empty:
        subset_p = panarchy_sim[panarchy_sim["scenario_name"] == "Cascading revolt"]
        if not subset_p.empty:
            selected = subset_p[subset_p["system_id"] == subset_p["system_id"].iloc[0]]
            plt.figure(figsize=(10, 6))
            plt.plot(selected["time"], selected["fast_resilience"], label="Fast-cycle resilience")
            plt.plot(selected["time"], selected["slow_resilience"], label="Slow-cycle resilience")
            plt.plot(selected["time"], selected["fast_rigidity"], label="Fast-cycle rigidity")
            plt.plot(selected["time"], selected["slow_rigidity"], label="Slow-cycle rigidity")
            plt.xlabel("Time")
            plt.ylabel("Value")
            plt.title("Cross-Scale Panarchy Dynamics")
            plt.legend(fontsize=8)
            plt.tight_layout()
            plt.savefig(OUT_FIGURES / "panarchy_cross_scale_dynamics.png", dpi=160)
            plt.close()


def main() -> None:
    raw_profiles = pd.read_csv(SYSTEMS_PATH)
    scales = pd.read_csv(SCALES_PATH)
    scenarios = pd.read_csv(SCENARIOS_PATH)

    profiles = phase_diagnostic(raw_profiles)
    cycle_sim = simulate_systems(profiles, scenarios)
    panarchy_sim = simulate_panarchy(scales, scenarios)

    profiles.to_csv(OUT_TABLES / "adaptive_cycle_profiles_advanced.csv", index=False)
    cycle_sim.to_csv(OUT_TABLES / "adaptive_cycle_phase_simulation_advanced.csv", index=False)
    panarchy_sim.to_csv(OUT_TABLES / "panarchy_cross_scale_simulation_advanced.csv", index=False)

    summary = (
        cycle_sim.groupby(["system_name", "scenario_name"])
        .agg(
            release_events=("release_flag", "sum"),
            alpha_steps=("phase", lambda x: (x == "alpha").sum()),
            minimum_resilience=("resilience", "min"),
            maximum_rigidity=("rigidity", "max"),
            average_memory=("memory", "mean"),
        )
        .reset_index()
    )
    summary.to_csv(OUT_TABLES / "adaptive_cycle_summary_advanced.csv", index=False)

    panarchy_summary = (
        panarchy_sim.groupby(["system_id", "scenario_name"])
        .agg(
            revolt_events=("revolt_effect", lambda x: (x > 0).sum()),
            remember_events=("remember_effect", lambda x: (x > 0).sum()),
            fast_release_steps=("fast_phase", lambda x: (x == "Omega").sum()),
            slow_release_steps=("slow_phase", lambda x: (x == "Omega").sum()),
            minimum_fast_resilience=("fast_resilience", "min"),
            minimum_slow_resilience=("slow_resilience", "min"),
        )
        .reset_index()
    )
    panarchy_summary.to_csv(OUT_TABLES / "panarchy_cross_scale_summary_advanced.csv", index=False)

    plot_outputs(profiles, cycle_sim, panarchy_sim)

    training = expand_training(raw_profiles)
    X = training[FEATURES]
    y = training["release_risk"]

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
            "model": "random_forest_adaptive_cycle_release_risk_classifier",
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

    training.to_csv(OUT_TABLES / "synthetic_release_risk_training_data.csv", index=False)
    metrics.to_csv(OUT_TABLES / "advanced_release_risk_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "adaptive_cycle_release_risk_classifier.joblib")

    plt.figure(figsize=(10, 6))
    plt.barh(importance["feature"], importance["importance"])
    plt.gca().invert_yaxis()
    plt.xlabel("Importance")
    plt.title("Feature Importance for Adaptive-Cycle Release Risk")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "advanced_feature_importance.png", dpi=160)
    plt.close()

    print("Advanced adaptive cycles and panarchy workflow complete.")
    print(profiles[["system_name", "initial_phase", "release_risk_index", "renewal_potential_index", "diagnostic"]].round(3))
    print(metrics.round(4))


if __name__ == "__main__":
    main()
