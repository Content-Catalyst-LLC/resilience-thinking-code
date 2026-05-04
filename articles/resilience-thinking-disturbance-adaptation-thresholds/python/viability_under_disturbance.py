"""
Resilience Thinking: Viability Under Repeated Disturbance

Educational model showing how adaptive capacity, threshold distance,
learning capacity, and redundancy shape system viability under repeated shocks.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def compute_resilience_profile(row: pd.Series) -> float:
    """Compute a stylized resilience profile from core dimensions."""
    return (
        0.30 * row["adaptive_capacity"]
        + 0.28 * row["threshold_distance"]
        + 0.24 * row["learning_capacity"]
        + 0.18 * row["redundancy"]
    )


def simulate_viability(
    resilience_profile: float,
    threshold_distance: float,
    learning_capacity: float,
    time_steps: int = 60,
    initial_state: float = 1.0
) -> pd.DataFrame:
    """
    Simulate system viability under repeated disturbance.

    This is a conceptual model, not an empirical forecast.
    """
    disturbance = np.resize(
        np.array([0.06, 0.09, 0.12, 0.18, 0.08, 0.11, 0.22, 0.10]),
        time_steps
    )

    viability = np.zeros(time_steps)
    threshold_risk = np.zeros(time_steps)
    viability[0] = initial_state

    for t in range(1, time_steps):
        disturbance_load = disturbance[t]
        learning_gain = 0.08 * learning_capacity * (1.2 - viability[t - 1])
        adaptive_response = 0.18 * resilience_profile

        viability[t] = (
            viability[t - 1]
            - 0.60 * disturbance_load
            + adaptive_response
            + learning_gain
        )

        viability[t] = np.clip(viability[t], 0.0, 1.5)
        threshold_risk[t] = disturbance_load / max(threshold_distance, 0.01)

    return pd.DataFrame({
        "time": np.arange(1, time_steps + 1),
        "viability": viability,
        "threshold_risk": threshold_risk,
        "threshold_breach": viability < 0.35
    })


def main() -> None:
    systems = pd.read_csv("../data/resilience_profiles.csv")
    systems["resilience_profile"] = systems.apply(compute_resilience_profile, axis=1)

    rows = []

    for _, row in systems.iterrows():
        result = simulate_viability(
            resilience_profile=row["resilience_profile"],
            threshold_distance=row["threshold_distance"],
            learning_capacity=row["learning_capacity"]
        )
        result["system_type"] = row["system_type"]
        rows.append(result)

    simulation = pd.concat(rows, ignore_index=True)

    summary = simulation.groupby("system_type").agg(
        min_viability=("viability", "min"),
        final_viability=("viability", "last"),
        max_threshold_risk=("threshold_risk", "max"),
        threshold_breaches=("threshold_breach", "sum")
    ).reset_index()

    print(systems)
    print(summary)

    simulation.to_csv("../outputs/viability_under_disturbance.csv", index=False)
    summary.to_csv("../outputs/viability_summary.csv", index=False)
    systems.to_csv("../outputs/resilience_profiles_scored.csv", index=False)


if __name__ == "__main__":
    main()
