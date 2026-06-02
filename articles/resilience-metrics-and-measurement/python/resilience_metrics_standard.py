#!/usr/bin/env python3
"""
Dependency-light resilience metrics and measurement workflow.

Reads synthetic framework and event data, calculates measurement framework
rankings, event-level resistance and recovery diagnostics, and Monte Carlo
robustness using only the Python standard library.

Run:
    python3 python/resilience_metrics_standard.py
"""

from __future__ import annotations

import csv
import random
from pathlib import Path
from statistics import mean, median


ROOT = Path(__file__).resolve().parents[1]
FRAMEWORKS_PATH = ROOT / "data" / "raw" / "resilience_measurement_frameworks.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "resilience_measurement_scenarios.csv"
EVENTS_PATH = ROOT / "data" / "raw" / "synthetic_system_events.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
DATA_PROCESSED = ROOT / "data" / "processed"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

BENEFIT_CRITERIA = [
    "resistance_coverage",
    "recovery_insight",
    "adaptive_capacity_visibility",
    "buffer_visibility",
    "justice_visibility",
    "data_quality_transparency",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def f(row: dict[str, str], key: str) -> float:
    return float(row[key])


def base_metric_value(row: dict[str, str]) -> float:
    return (
        0.16 * f(row, "resistance_coverage")
        + 0.16 * f(row, "recovery_insight")
        + 0.16 * f(row, "adaptive_capacity_visibility")
        + 0.15 * f(row, "buffer_visibility")
        + 0.13 * f(row, "justice_visibility")
        + 0.10 * f(row, "data_quality_transparency")
        - 0.14 * f(row, "threshold_blindness")
    )


def score_framework(row: dict[str, str], scenario: dict[str, str]) -> float:
    return (
        f(scenario, "resistance_coverage_weight") * f(row, "resistance_coverage")
        + f(scenario, "recovery_insight_weight") * f(row, "recovery_insight")
        + f(scenario, "adaptive_capacity_visibility_weight") * f(row, "adaptive_capacity_visibility")
        + f(scenario, "buffer_visibility_weight") * f(row, "buffer_visibility")
        + f(scenario, "justice_visibility_weight") * f(row, "justice_visibility")
        + f(scenario, "data_quality_transparency_weight") * f(row, "data_quality_transparency")
        - f(scenario, "threshold_blindness_weight") * f(row, "threshold_blindness")
    )


def framework_diagnostic(row: dict[str, str], value: float) -> str:
    if value >= 5.95 and f(row, "threshold_blindness") <= 3.4:
        return "strong hybrid measurement profile with low threshold blindness"
    if f(row, "threshold_blindness") >= 4.8:
        return "threshold blindness review needed"
    if f(row, "justice_visibility") < 7.2:
        return "justice visibility needs strengthening"
    if f(row, "data_quality_transparency") < 7.3:
        return "data-quality transparency constraint"
    return "promising but requires system-specific validation"


def event_metrics(row: dict[str, str]) -> dict[str, object]:
    baseline = f(row, "baseline_function")
    minimum = f(row, "min_function")
    recovered = f(row, "recovered_function")
    shock = f(row, "shock_intensity")
    recovery_days = f(row, "recovery_days")
    justice = f(row, "justice_visibility")
    affected = f(row, "affected_population_share")

    performance_loss = max(0.0, baseline - minimum)
    resistance_score = max(0.0, 1.0 - (performance_loss / max(0.01, shock)))
    recovery_completeness = max(0.0, min(1.0, (recovered - minimum) / max(0.01, baseline - minimum)))
    recovery_speed = 1.0 / (1.0 + recovery_days / 30.0)
    justice_adjusted_recovery = recovery_completeness * (0.70 + 0.30 * justice) * (1.0 - 0.20 * affected)

    if justice_adjusted_recovery < 0.55:
        diagnostic = "recovery may hide distributional or long-duration vulnerability"
    elif resistance_score < 0.45:
        diagnostic = "low resistance to disturbance"
    elif recovery_speed < 0.30:
        diagnostic = "slow recovery requires capacity review"
    else:
        diagnostic = "moderate to strong event-level resilience signal"

    return {
        "event_id": row["event_id"],
        "system_name": row["system_name"],
        "system_type": row["system_type"],
        "disturbance_type": row["disturbance_type"],
        "shock_intensity": shock,
        "performance_loss": round(performance_loss, 5),
        "resistance_score": round(resistance_score, 5),
        "recovery_completeness": round(recovery_completeness, 5),
        "recovery_speed": round(recovery_speed, 5),
        "justice_adjusted_recovery": round(justice_adjusted_recovery, 5),
        "diagnostic": diagnostic,
    }


def scenario_rankings(frameworks: list[dict[str, str]], scenarios: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for scenario in scenarios:
        scored = []
        for framework in frameworks:
            value = score_framework(framework, scenario)
            scored.append((value, framework))
        scored.sort(key=lambda item: item[0], reverse=True)

        for rank, (value, framework) in enumerate(scored, start=1):
            rows.append(
                {
                    "scenario": scenario["scenario"],
                    "framework_id": framework["framework_id"],
                    "framework": framework["framework"],
                    "framework_type": framework["framework_type"],
                    "rank": rank,
                    "metric_value": round(value, 5),
                    "threshold_blindness": framework["threshold_blindness"],
                    "critical_use": framework["critical_use"],
                }
            )
    return rows


def monte_carlo(
    frameworks: list[dict[str, str]],
    scenario: dict[str, str],
    n: int = 3000,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rng = random.Random(42)
    simulation_rows = []

    for simulation_id in range(n):
        scored = []
        for framework in frameworks:
            sampled = dict(framework)
            for criterion in BENEFIT_CRITERIA + ["threshold_blindness"]:
                sampled_value = max(1.0, min(10.0, f(framework, criterion) + rng.gauss(0, 0.6)))
                sampled[criterion] = str(sampled_value)

            value = score_framework(sampled, scenario)
            scored.append((value, framework))

        scored.sort(key=lambda item: item[0], reverse=True)

        for rank, (value, framework) in enumerate(scored, start=1):
            simulation_rows.append(
                {
                    "simulation_id": simulation_id,
                    "framework_id": framework["framework_id"],
                    "framework": framework["framework"],
                    "rank": rank,
                    "metric_value": round(value, 5),
                    "winner": scored[0][1]["framework"],
                }
            )

    summary_rows = []
    framework_count = len(frameworks)

    for framework in frameworks:
        subset = [row for row in simulation_rows if row["framework_id"] == framework["framework_id"]]
        ranks = [int(row["rank"]) for row in subset]
        values = [float(row["metric_value"]) for row in subset]
        summary_rows.append(
            {
                "framework_id": framework["framework_id"],
                "framework": framework["framework"],
                "mean_metric_value": round(mean(values), 5),
                "median_metric_value": round(median(values), 5),
                "probability_ranked_first": round(100 * sum(1 for r in ranks if r == 1) / n, 2),
                "probability_top_two": round(100 * sum(1 for r in ranks if r <= 2) / n, 2),
                "probability_bottom_two": round(100 * sum(1 for r in ranks if r >= framework_count - 1) / n, 2),
            }
        )

    summary_rows.sort(key=lambda row: row["probability_ranked_first"], reverse=True)
    return simulation_rows, summary_rows


def main() -> None:
    frameworks = read_csv(FRAMEWORKS_PATH)
    scenarios = read_csv(SCENARIOS_PATH)
    events = read_csv(EVENTS_PATH)

    profile_rows = []
    for row in frameworks:
        value = base_metric_value(row)
        profile_rows.append(
            {
                "framework_id": row["framework_id"],
                "framework": row["framework"],
                "framework_type": row["framework_type"],
                "critical_use": row["critical_use"],
                "base_metric_value": round(value, 5),
                "resistance_coverage": row["resistance_coverage"],
                "recovery_insight": row["recovery_insight"],
                "adaptive_capacity_visibility": row["adaptive_capacity_visibility"],
                "buffer_visibility": row["buffer_visibility"],
                "justice_visibility": row["justice_visibility"],
                "data_quality_transparency": row["data_quality_transparency"],
                "threshold_blindness": row["threshold_blindness"],
                "diagnostic": framework_diagnostic(row, value),
            }
        )

    event_rows = [event_metrics(row) for row in events]
    rankings = scenario_rankings(frameworks, scenarios)
    baseline = next(s for s in scenarios if s["scenario"] == "Balanced")
    simulation_rows, robustness_rows = monte_carlo(frameworks, baseline, n=3000)

    first_place_summary: dict[str, int] = {}
    for row in rankings:
        if int(row["rank"]) == 1:
            first_place_summary[row["framework"]] = first_place_summary.get(row["framework"], 0) + 1

    top_rank_rows = [
        {"framework": framework, "times_ranked_first": count}
        for framework, count in sorted(first_place_summary.items(), key=lambda item: item[1], reverse=True)
    ]

    write_csv(OUT_TABLES / "resilience_metric_framework_profiles_standard.csv", profile_rows)
    write_csv(OUT_TABLES / "resilience_event_performance_metrics_standard.csv", event_rows)
    write_csv(OUT_TABLES / "resilience_metric_framework_rankings_standard.csv", rankings)
    write_csv(OUT_TABLES / "resilience_measurement_top_rank_summary_standard.csv", top_rank_rows)
    write_csv(OUT_TABLES / "resilience_measurement_monte_carlo_standard.csv", simulation_rows)
    write_csv(OUT_TABLES / "resilience_measurement_robustness_summary_standard.csv", robustness_rows)
    write_csv(DATA_PROCESSED / "resilience_metric_framework_profiles_standard.csv", profile_rows)

    print("Resilience metrics workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    for row in profile_rows:
        print(
            f"  {row['framework']}: value={row['base_metric_value']} "
            f"diagnostic={row['diagnostic']}"
        )


if __name__ == "__main__":
    main()
