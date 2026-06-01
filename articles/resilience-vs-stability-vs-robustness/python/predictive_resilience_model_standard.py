#!/usr/bin/env python3
"""
Dependency-light predictive resilience model.

This script generates synthetic training data and trains a logistic regression
model from scratch using only the Python standard library.

Purpose:
    Predict whether a system falls below a viable resilience threshold after
    repeated disturbance.

Run:
    python3 python/predictive_resilience_model_standard.py

Outputs:
    outputs/tables/synthetic_resilience_training_data.csv
    outputs/tables/standard_model_coefficients.csv
    outputs/tables/standard_model_metrics.csv
    outputs/tables/standard_scenario_predictions.csv
"""

from __future__ import annotations

import csv
import math
import random
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
OUT_TABLES = ROOT / "outputs" / "tables"
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
DATA_RAW.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

FEATURES = [
    "equilibrium_return",
    "stress_tolerance",
    "adaptive_capacity",
    "threshold_distance",
    "learning_capacity",
    "redundancy",
    "modularity",
    "exposure",
    "sensitivity",
    "dependency_concentration",
    "shock_intensity",
    "shock_frequency",
    "compound_disturbance_index",
]


def sigmoid(z: float) -> float:
    if z >= 0:
        ez = math.exp(-z)
        return 1 / (1 + ez)
    ez = math.exp(z)
    return ez / (1 + ez)


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def generate_record(i: int) -> dict[str, float | int | str]:
    system_types = [
        "ecological",
        "urban_infrastructure",
        "institutional",
        "supply_chain",
        "public_health",
        "community",
        "financial",
    ]

    system_type = random.choice(system_types)

    equilibrium_return = random.uniform(0.25, 0.95)
    stress_tolerance = random.uniform(0.25, 0.95)
    adaptive_capacity = random.uniform(0.20, 0.95)
    threshold_distance = random.uniform(0.15, 0.95)
    learning_capacity = random.uniform(0.15, 0.95)
    redundancy = random.uniform(0.15, 0.90)
    modularity = random.uniform(0.15, 0.90)
    exposure = random.uniform(0.15, 0.95)
    sensitivity = random.uniform(0.15, 0.95)
    dependency_concentration = random.uniform(0.10, 0.95)
    shock_intensity = random.uniform(0.05, 0.80)
    shock_frequency = random.randint(1, 12)
    compound_disturbance_index = clamp(
        0.45 * shock_intensity + 0.30 * (shock_frequency / 12.0) + 0.25 * exposure
    )

    stability_score = equilibrium_return
    robustness_score = 0.65 * stress_tolerance + 0.35 * equilibrium_return
    resilience_score = (
        0.22 * adaptive_capacity
        + 0.20 * threshold_distance
        + 0.18 * learning_capacity
        + 0.20 * redundancy
        + 0.20 * modularity
    )

    risk_pressure = (
        0.22 * exposure
        + 0.20 * sensitivity
        + 0.20 * dependency_concentration
        + 0.22 * shock_intensity
        + 0.16 * (shock_frequency / 12.0)
    )

    # Latent margin. Positive means the system keeps enough viability margin.
    viability_margin = (
        0.20 * stability_score
        + 0.24 * robustness_score
        + 0.44 * resilience_score
        + 0.20 * threshold_distance
        - 0.62 * risk_pressure
        - 0.18 * compound_disturbance_index
        + random.gauss(0, 0.06)
    )

    # Binary target: 1 means predicted threshold failure / resilience failure risk.
    resilience_failure_risk = 1 if viability_margin < 0.30 else 0

    return {
        "observation_id": i,
        "system_type": system_type,
        "equilibrium_return": round(equilibrium_return, 4),
        "stress_tolerance": round(stress_tolerance, 4),
        "adaptive_capacity": round(adaptive_capacity, 4),
        "threshold_distance": round(threshold_distance, 4),
        "learning_capacity": round(learning_capacity, 4),
        "redundancy": round(redundancy, 4),
        "modularity": round(modularity, 4),
        "exposure": round(exposure, 4),
        "sensitivity": round(sensitivity, 4),
        "dependency_concentration": round(dependency_concentration, 4),
        "shock_intensity": round(shock_intensity, 4),
        "shock_frequency": shock_frequency,
        "compound_disturbance_index": round(compound_disturbance_index, 4),
        "stability_score": round(stability_score, 4),
        "robustness_score": round(robustness_score, 4),
        "resilience_score": round(resilience_score, 4),
        "risk_pressure": round(risk_pressure, 4),
        "simulated_viability_margin": round(viability_margin, 4),
        "resilience_failure_risk": resilience_failure_risk,
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def train_test_split(rows: list[dict[str, object]], test_ratio: float = 0.25):
    shuffled = rows[:]
    random.shuffle(shuffled)
    split = int(len(shuffled) * (1 - test_ratio))
    return shuffled[:split], shuffled[split:]


def standardize(train: list[dict[str, object]], test: list[dict[str, object]]):
    means = {f: mean(float(r[f]) for r in train) for f in FEATURES}
    stds = {}
    for f in FEATURES:
        variance = mean((float(r[f]) - means[f]) ** 2 for r in train)
        stds[f] = math.sqrt(variance) or 1.0

    def transform(rows):
        output = []
        for row in rows:
            output.append([(float(row[f]) - means[f]) / stds[f] for f in FEATURES])
        return output

    return transform(train), transform(test), means, stds


def train_logistic_regression(x_train, y_train, learning_rate=0.035, epochs=2200, l2=0.012):
    n_features = len(x_train[0])
    weights = [0.0] * n_features
    bias = 0.0

    for _ in range(epochs):
        grad_w = [0.0] * n_features
        grad_b = 0.0

        for x, y in zip(x_train, y_train):
            z = bias + sum(w * xi for w, xi in zip(weights, x))
            p = sigmoid(z)
            error = p - y

            for j in range(n_features):
                grad_w[j] += error * x[j]
            grad_b += error

        n = len(x_train)
        for j in range(n_features):
            grad_w[j] = grad_w[j] / n + l2 * weights[j]
            weights[j] -= learning_rate * grad_w[j]

        bias -= learning_rate * (grad_b / n)

    return weights, bias


def predict_proba(x_rows, weights, bias):
    return [sigmoid(bias + sum(w * xi for w, xi in zip(weights, x))) for x in x_rows]


def evaluate(y_true, y_prob, threshold=0.50):
    y_pred = [1 if p >= threshold else 0 for p in y_prob]
    tp = sum(1 for y, p in zip(y_true, y_pred) if y == 1 and p == 1)
    tn = sum(1 for y, p in zip(y_true, y_pred) if y == 0 and p == 0)
    fp = sum(1 for y, p in zip(y_true, y_pred) if y == 0 and p == 1)
    fn = sum(1 for y, p in zip(y_true, y_pred) if y == 1 and p == 0)

    accuracy = (tp + tn) / len(y_true)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    brier = mean((p - y) ** 2 for p, y in zip(y_prob, y_true))

    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "brier_score": round(brier, 4),
        "true_positive": tp,
        "true_negative": tn,
        "false_positive": fp,
        "false_negative": fn,
    }


def scenario_rows() -> list[dict[str, object]]:
    return [
        {
            "scenario_name": "Stable but brittle institution",
            "equilibrium_return": 0.90,
            "stress_tolerance": 0.55,
            "adaptive_capacity": 0.28,
            "threshold_distance": 0.32,
            "learning_capacity": 0.24,
            "redundancy": 0.35,
            "modularity": 0.34,
            "exposure": 0.64,
            "sensitivity": 0.62,
            "dependency_concentration": 0.75,
            "shock_intensity": 0.45,
            "shock_frequency": 7,
            "compound_disturbance_index": 0.55,
        },
        {
            "scenario_name": "Robust but inflexible infrastructure",
            "equilibrium_return": 0.68,
            "stress_tolerance": 0.90,
            "adaptive_capacity": 0.38,
            "threshold_distance": 0.46,
            "learning_capacity": 0.33,
            "redundancy": 0.60,
            "modularity": 0.43,
            "exposure": 0.70,
            "sensitivity": 0.58,
            "dependency_concentration": 0.68,
            "shock_intensity": 0.52,
            "shock_frequency": 8,
            "compound_disturbance_index": 0.62,
        },
        {
            "scenario_name": "Adaptive resilient system",
            "equilibrium_return": 0.56,
            "stress_tolerance": 0.72,
            "adaptive_capacity": 0.88,
            "threshold_distance": 0.80,
            "learning_capacity": 0.86,
            "redundancy": 0.73,
            "modularity": 0.70,
            "exposure": 0.52,
            "sensitivity": 0.46,
            "dependency_concentration": 0.40,
            "shock_intensity": 0.50,
            "shock_frequency": 8,
            "compound_disturbance_index": 0.54,
        },
    ]


def transform_scenarios(rows, means, stds):
    output = []
    for row in rows:
        output.append([(float(row[f]) - means[f]) / stds[f] for f in FEATURES])
    return output


def main() -> None:
    rows = [generate_record(i) for i in range(1, 2201)]

    training_path = OUT_TABLES / "synthetic_resilience_training_data.csv"
    write_csv(training_path, rows)

    train_rows, test_rows = train_test_split(rows)
    x_train, x_test, means, stds = standardize(train_rows, test_rows)
    y_train = [int(r["resilience_failure_risk"]) for r in train_rows]
    y_test = [int(r["resilience_failure_risk"]) for r in test_rows]

    weights, bias = train_logistic_regression(x_train, y_train)
    y_prob = predict_proba(x_test, weights, bias)
    metrics = evaluate(y_test, y_prob)

    coefficient_rows = [
        {"feature": feature, "coefficient": round(coef, 6)}
        for feature, coef in sorted(zip(FEATURES, weights), key=lambda item: abs(item[1]), reverse=True)
    ]
    coefficient_rows.append({"feature": "__bias__", "coefficient": round(bias, 6)})

    metrics_rows = [{"metric": k, "value": v} for k, v in metrics.items()]

    scenarios = scenario_rows()
    scenario_x = transform_scenarios(scenarios, means, stds)
    scenario_probs = predict_proba(scenario_x, weights, bias)
    scenario_predictions = []

    for row, p in zip(scenarios, scenario_probs):
        scenario_predictions.append(
            {
                "scenario_name": row["scenario_name"],
                "predicted_failure_probability": round(p, 4),
                "prediction_band": (
                    "high predicted resilience failure risk"
                    if p >= 0.65
                    else "moderate predicted resilience failure risk"
                    if p >= 0.35
                    else "lower predicted resilience failure risk"
                ),
            }
        )

    write_csv(OUT_TABLES / "standard_model_coefficients.csv", coefficient_rows)
    write_csv(OUT_TABLES / "standard_model_metrics.csv", metrics_rows)
    write_csv(OUT_TABLES / "standard_scenario_predictions.csv", scenario_predictions)

    # Also place the training data in data/processed for downstream workflows.
    write_csv(DATA_PROCESSED / "synthetic_resilience_training_data.csv", rows)

    print("Dependency-light predictive resilience model complete.")
    print(f"Wrote: {training_path.relative_to(ROOT)}")
    print("Metrics:")
    for k, v in metrics.items():
        print(f"  {k}: {v}")
    print("Scenario predictions:")
    for row in scenario_predictions:
        print(f"  {row['scenario_name']}: {row['predicted_failure_probability']} ({row['prediction_band']})")


if __name__ == "__main__":
    main()
