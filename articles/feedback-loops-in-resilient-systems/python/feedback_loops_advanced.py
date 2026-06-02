#!/usr/bin/env python3
"""
Advanced feedback-loop workflow.

Uses pandas, numpy, matplotlib, scikit-learn, and joblib.

Run:
    pip install -r requirements-advanced.txt
    python python/feedback_loops_advanced.py
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
PROFILES_PATH = ROOT / "data" / "raw" / "feedback_system_profiles.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "feedback_scenarios.csv"
LINKS_PATH = ROOT / "data" / "raw" / "causal_links.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_FIGURES = ROOT / "outputs" / "figures"
OUT_MODELS = ROOT / "outputs" / "models"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)
OUT_MODELS.mkdir(parents=True, exist_ok=True)

FEATURES = [
    "reinforcing_gain",
    "balancing_strength",
    "delay_steps_scaled",
    "disturbance_load",
    "adaptive_capacity",
    "signal_quality",
    "system_memory",
    "justice_visibility",
]

def score_profiles(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["delay_steps_scaled"] = out["delay_steps"] / 10.0
    out["feedback_risk_score"] = (
        0.24 * out["reinforcing_gain"]
        + 0.20 * out["disturbance_load"]
        + 0.18 * out["delay_steps_scaled"]
        - 0.16 * out["balancing_strength"]
        - 0.10 * out["adaptive_capacity"]
        - 0.07 * out["signal_quality"]
        - 0.03 * out["system_memory"]
        - 0.02 * out["justice_visibility"]
    )
    out["feedback_protection_score"] = (
        0.24 * out["balancing_strength"]
        + 0.20 * out["adaptive_capacity"]
        + 0.18 * out["signal_quality"]
        + 0.16 * out["system_memory"]
        + 0.12 * out["justice_visibility"]
        - 0.10 * out["delay_steps_scaled"]
    )
    conditions = [
        out["feedback_risk_score"] >= 0.12,
        out["delay_steps"] >= 7,
        out["balancing_strength"] < 0.10,
        out["signal_quality"] < 0.48,
    ]
    choices = [
        "high feedback-risk concern",
        "delay and overshoot concern",
        "weak balancing feedback concern",
        "feedback blindness or signal-quality concern",
    ]
    out["diagnostic"] = np.select(conditions, choices, default="mixed feedback profile requiring monitoring")
    return out

def loop_polarity(links: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        links.assign(is_negative=lambda x: x["polarity"].str.strip().eq("-"))
        .groupby(["loop_id", "loop_name"])
        .agg(link_count=("polarity", "count"), negative_link_count=("is_negative", "sum"))
        .reset_index()
    )
    grouped["loop_type"] = np.where(grouped["negative_link_count"] % 2 == 0, "reinforcing", "balancing")
    return grouped

def simulate_scenarios(scenarios: pd.DataFrame, steps: int = 80) -> pd.DataFrame:
    rows = []
    for _, scenario in scenarios.iterrows():
        gain = float(scenario["reinforcing_gain"])
        balancing = float(scenario["balancing_strength"])
        delay = int(scenario["delay_steps"])
        target = float(scenario["target"])
        shock = float(scenario["disturbance_shock"])
        adaptive_response = float(scenario["adaptive_response"])
        x = np.full(steps + delay + 2, 20.0)

        for t in range(1, steps):
            delayed_index = max(0, t - delay)
            disturbance = shock if t == 12 else 0.0
            effective_balancing = balancing + adaptive_response * min(1.0, t / steps)
            x[t] = x[t - 1] + gain * x[t - 1] - effective_balancing * (x[delayed_index] - target) + disturbance
            rows.append(
                {
                    "scenario_id": scenario["scenario_id"],
                    "scenario_name": scenario["scenario_name"],
                    "time": t,
                    "value": x[t],
                    "target": target,
                    "reinforcing_gain": gain,
                    "effective_balancing": effective_balancing,
                    "delay_steps": delay,
                    "disturbance": disturbance,
                    "overshoot": max(0.0, x[t] - target),
                    "distance_from_target": abs(x[t] - target),
                }
            )
    return pd.DataFrame(rows)

def delay_sensitivity(base: pd.Series, delays: list[int] | None = None, steps: int = 80) -> pd.DataFrame:
    if delays is None:
        delays = [1, 3, 5, 8, 12]
    rows = []
    for delay in delays:
        scenario = base.copy()
        scenario["delay_steps"] = delay
        sim = simulate_scenarios(pd.DataFrame([scenario]), steps=steps)
        sim["delay_experiment"] = delay
        rows.append(sim)
    return pd.concat(rows, ignore_index=True)

def policy_resistance(steps: int = 80) -> pd.DataFrame:
    rows = []
    fuel = 35.0
    visible_fire_damage = 20.0
    suppression = 0.70
    for t in range(1, steps + 1):
        fuel += 1.2 * suppression - 0.18 * visible_fire_damage
        fuel = max(0.0, fuel)
        visible_fire_damage = 0.22 * fuel * (1.0 + suppression) if t % 15 == 0 else max(0.0, visible_fire_damage * 0.72)
        suppression = min(1.0, suppression + 0.012 * visible_fire_damage / 20.0)
        rows.append({"time": t, "fuel_load": fuel, "visible_fire_damage": visible_fire_damage, "suppression_pressure": suppression})
    return pd.DataFrame(rows)

def adaptive_learning_loop(steps: int = 80) -> pd.DataFrame:
    rows = []
    signal_quality = 0.42
    memory = 0.48
    adaptive_capacity = 0.46
    system_stress = 0.72
    for t in range(1, steps + 1):
        disturbance = 0.16 + 0.10 * np.sin(t / 6.0)
        learning = 0.015 * signal_quality + 0.012 * memory
        adaptive_capacity = np.clip(adaptive_capacity + learning - 0.020 * disturbance, 0.0, 1.0)
        signal_quality = np.clip(signal_quality + 0.006 * adaptive_capacity - 0.004 * system_stress, 0.0, 1.0)
        memory = np.clip(memory + 0.006 * signal_quality - 0.003 * disturbance, 0.0, 1.0)
        system_stress = np.clip(system_stress + disturbance - 0.20 * adaptive_capacity, 0.0, 1.2)
        rows.append({"time": t, "signal_quality": signal_quality, "system_memory": memory, "adaptive_capacity": adaptive_capacity, "system_stress": system_stress, "disturbance": disturbance})
    return pd.DataFrame(rows)

def plot_outputs(profiles: pd.DataFrame, sim: pd.DataFrame, delay_df: pd.DataFrame, policy_df: pd.DataFrame, learning_df: pd.DataFrame) -> None:
    profile_plot = profiles[["system_name", "feedback_risk_score", "feedback_protection_score", "reinforcing_gain", "balancing_strength", "delay_steps_scaled", "adaptive_capacity"]].melt(id_vars="system_name", var_name="indicator", value_name="value")
    order = profiles.sort_values("feedback_risk_score")["system_name"].tolist()
    plt.figure(figsize=(10, 6))
    for indicator, subset in profile_plot.groupby("indicator"):
        y = [order.index(s) for s in subset["system_name"]]
        plt.scatter(subset["value"], y, label=indicator, s=50)
    plt.yticks(range(len(order)), order)
    plt.xlabel("Indicator value")
    plt.title("Feedback Risk and Protection Profiles")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "feedback_risk_profiles.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    for scenario_name in sim["scenario_name"].unique():
        subset = sim[sim["scenario_name"] == scenario_name]
        plt.plot(subset["time"], subset["value"], label=scenario_name)
    plt.axhline(sim["target"].iloc[0], linestyle="--", linewidth=1, label="Target")
    plt.xlabel("Time")
    plt.ylabel("System value")
    plt.title("Feedback Loop Dynamics Across Scenarios")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "feedback_loop_dynamics.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    for delay in sorted(delay_df["delay_experiment"].unique()):
        subset = delay_df[delay_df["delay_experiment"] == delay]
        plt.plot(subset["time"], subset["value"], label=f"Delay {delay}")
    plt.xlabel("Time")
    plt.ylabel("System value")
    plt.title("Delay Sensitivity in Balancing Feedback")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "feedback_delay_sensitivity.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(policy_df["time"], policy_df["fuel_load"], label="Fuel load")
    plt.plot(policy_df["time"], policy_df["visible_fire_damage"], label="Visible fire damage")
    plt.plot(policy_df["time"], policy_df["suppression_pressure"] * 50, label="Suppression pressure scaled")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title("Policy Resistance Example: Fire Suppression and Fuel Accumulation")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "policy_resistance_fire_suppression.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 6))
    for col in ["signal_quality", "system_memory", "adaptive_capacity", "system_stress"]:
        plt.plot(learning_df["time"], learning_df[col], label=col)
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title("Adaptive Learning Feedback Loop")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "adaptive_learning_loop.png", dpi=160)
    plt.close()

def expand_training(df: pd.DataFrame, n: int = 2400) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []
    base_df = df.copy()
    base_df["delay_steps_scaled"] = base_df["delay_steps"] / 10.0
    for _ in range(n):
        base = base_df.sample(1, random_state=int(rng.integers(0, 1000000))).iloc[0]
        record = {}
        for feature in FEATURES:
            noise = 0.06 if feature != "delay_steps_scaled" else 0.10
            record[feature] = float(np.clip(float(base[feature]) + rng.normal(0, noise), 0.01, 1.20))
        risk = (
            0.24 * record["reinforcing_gain"]
            + 0.20 * record["disturbance_load"]
            + 0.18 * record["delay_steps_scaled"]
            - 0.16 * record["balancing_strength"]
            - 0.10 * record["adaptive_capacity"]
            - 0.07 * record["signal_quality"]
            - 0.03 * record["system_memory"]
            - 0.02 * record["justice_visibility"]
            + rng.normal(0, 0.025)
        )
        record["feedback_risk_score"] = risk
        record["feedback_risk"] = 1 if risk >= 0.12 else 0
        rows.append(record)
    return pd.DataFrame(rows)

def main() -> None:
    raw_profiles = pd.read_csv(PROFILES_PATH)
    scenarios = pd.read_csv(SCENARIOS_PATH)
    links = pd.read_csv(LINKS_PATH)

    profiles = score_profiles(raw_profiles)
    loop_diagnostics = loop_polarity(links)
    sim = simulate_scenarios(scenarios)
    delay_df = delay_sensitivity(scenarios.iloc[0])
    policy_df = policy_resistance()
    learning_df = adaptive_learning_loop()

    profiles.to_csv(OUT_TABLES / "feedback_system_profiles_advanced.csv", index=False)
    loop_diagnostics.to_csv(OUT_TABLES / "feedback_loop_polarity_diagnostics_advanced.csv", index=False)
    sim.to_csv(OUT_TABLES / "feedback_loop_simulation_advanced.csv", index=False)
    delay_df.to_csv(OUT_TABLES / "feedback_delay_sensitivity_advanced.csv", index=False)
    policy_df.to_csv(OUT_TABLES / "policy_resistance_fire_suppression_advanced.csv", index=False)
    learning_df.to_csv(OUT_TABLES / "adaptive_learning_loop_advanced.csv", index=False)

    scenario_summary = sim.groupby(["scenario_id", "scenario_name"]).agg(
        final_value=("value", "last"),
        maximum_value=("value", "max"),
        maximum_overshoot=("overshoot", "max"),
        average_distance_from_target=("distance_from_target", "mean"),
        average_effective_balancing=("effective_balancing", "mean"),
    ).reset_index()
    scenario_summary.to_csv(OUT_TABLES / "feedback_scenario_summary_advanced.csv", index=False)

    plot_outputs(profiles, sim, delay_df, policy_df, learning_df)

    training = expand_training(raw_profiles)
    X = training[FEATURES]
    y = training["feedback_risk"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=450, min_samples_leaf=6, class_weight="balanced", random_state=42)
    model.fit(X_train, y_train)

    prob = model.predict_proba(X_test)[:, 1]
    pred = (prob >= 0.50).astype(int)

    metrics = pd.DataFrame([{
        "model": "random_forest_feedback_risk_classifier",
        "accuracy": accuracy_score(y_test, pred),
        "precision": precision_score(y_test, pred, zero_division=0),
        "recall": recall_score(y_test, pred, zero_division=0),
        "f1": f1_score(y_test, pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, prob),
        "brier_score": brier_score_loss(y_test, prob),
    }])

    importance = pd.DataFrame({"feature": FEATURES, "importance": model.feature_importances_}).sort_values("importance", ascending=False)

    training.to_csv(OUT_TABLES / "synthetic_feedback_risk_training_data.csv", index=False)
    metrics.to_csv(OUT_TABLES / "advanced_feedback_risk_model_metrics.csv", index=False)
    importance.to_csv(OUT_TABLES / "advanced_feature_importance.csv", index=False)
    joblib.dump(model, OUT_MODELS / "feedback_risk_classifier.joblib")

    plt.figure(figsize=(10, 6))
    plt.barh(importance["feature"], importance["importance"])
    plt.gca().invert_yaxis()
    plt.xlabel("Importance")
    plt.title("Feature Importance for Feedback-Risk Classification")
    plt.tight_layout()
    plt.savefig(OUT_FIGURES / "advanced_feature_importance.png", dpi=160)
    plt.close()

    print("Advanced feedback loops workflow complete.")
    print(profiles[["system_name", "feedback_risk_score", "feedback_protection_score", "diagnostic"]].round(4))
    print(metrics.round(4))

if __name__ == "__main__":
    main()
