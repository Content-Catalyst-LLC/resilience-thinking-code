"""
Threshold risk model for resilience thinking.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def simulate_threshold_risk(
    steps: int = 100,
    initial_pressure: float = 0.10,
    pressure_growth: float = 0.012,
    threshold_distance: float = 0.75,
    adaptive_response: float = 0.004
) -> pd.DataFrame:
    pressure = np.zeros(steps)
    threshold = np.zeros(steps)
    threshold_risk = np.zeros(steps)

    pressure[0] = initial_pressure
    threshold[0] = threshold_distance

    for t in range(1, steps):
        pressure[t] = pressure[t - 1] + pressure_growth
        threshold[t] = max(0.05, threshold[t - 1] + adaptive_response - 0.002 * pressure[t])
        threshold_risk[t] = pressure[t] / threshold[t]

    return pd.DataFrame({
        "time": np.arange(steps),
        "pressure": pressure,
        "threshold_distance": threshold,
        "threshold_risk": threshold_risk,
        "high_risk": threshold_risk > 1.0
    })


def main() -> None:
    results = simulate_threshold_risk()
    print(results.tail())

    results.to_csv("../outputs/threshold_risk_model.csv", index=False)


if __name__ == "__main__":
    main()
