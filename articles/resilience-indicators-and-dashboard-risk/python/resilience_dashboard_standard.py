#!/usr/bin/env python3
"""
Dependency-light resilience indicators and dashboard-risk workflow.

Reads synthetic dashboard design, scenario, system, and red-flag data.
Calculates dashboard design rankings, naive scores, threshold-adjusted
scores, uncertainty-adjusted scores, red flags, and Monte Carlo robustness
using only the Python standard library.

Run:
    python3 python/resilience_dashboard_standard.py
"""

from __future__ import annotations

import csv
import random
from pathlib import Path
from statistics import mean, median


ROOT = Path(__file__).resolve().parents[1]
DESIGNS_PATH = ROOT / "data" / "raw" / "dashboard_designs.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "dashboard_scenarios.csv"
SYSTEMS_PATH = ROOT / "data" / "raw" / "synthetic_resilience_dashboard_systems.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
DATA_PROCESSED = ROOT / "data" / "processed"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

BENEFIT_CRITERIA = [
    "indicator_coverage",
    "threshold_sensitivity",
    "justice_visibility",
    "uncertainty_transparency",
    "decision_trigger_clarity",
    "learning_integration",
]

SYSTEM_BENEFITS = [
    "exposure_reduction",
    "recovery_capacity",
    "adaptive_capacity",
    "buffer_capacity",
    "justice_visibility",
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


def base_dashboard_value(row: dict[str, str]) -> float:
    return (
        0.15 * f(row, "indicator_coverage")
        + 0.17 * f(row, "threshold_sensitivity")
        + 0.16 * f(row, "justice_visibility")
        + 0.14 * f(row, "uncertainty_transparency")
        + 0.16 * f(row, "decision_trigger_clarity")
        + 0.14 * f(row, "learning_integration")
        - 0.08 * f(row, "dashboard_risk")
    )


def score_design(row: dict[str, str], scenario: dict[str, str]) -> float:
    return (
        f(scenario, "indicator_coverage_weight") * f(row, "indicator_coverage")
        + f(scenario, "threshold_sensitivity_weight") * f(row, "threshold_sensitivity")
        + f(scenario, "justice_visibility_weight") * f(row, "justice_visibility")
        + f(scenario, "uncertainty_transparency_weight") * f(row, "uncertainty_transparency")
        + f(scenario, "decision_trigger_clarity_weight") * f(row, "decision_trigger_clarity")
        + f(scenario, "learning_integration_weight") * f(row, "learning_integration")
        - f(scenario, "dashboard_risk_weight") * f(row, "dashboard_risk")
    )


def design_diagnostic(row: dict[str, str], value: float) -> str:
    if value >= 6.8 and f(row, "dashboard_risk") <= 4.1:
        return "strong responsible-dashboard profile"
    if f(row, "dashboard_risk") >= 7.0:
        return "high false-precision and dashboard-risk exposure"
    if f(row, "justice_visibility") < 7.0:
        return "justice visibility needs strengthening"
    if f(row, "decision_trigger_clarity") < 7.0:
        return "decision-trigger clarity constraint"
    return "promising but requires governance and uncertainty validation"


def score_system(row: dict[str, str]) -> dict[str, object]:
    naive_score = (
        0.17 * f(row, "exposure_reduction")
        + 0.18 * f(row, "recovery_capacity")
        + 0.19 * f(row, "adaptive_capacity")
        + 0.16 * f(row, "buffer_capacity")
        + 0.16 * f(row, "justice_visibility")
    )
    threshold_adjusted = naive_score - 0.09 * f(row, "threshold_risk")
    uncertainty_adjusted = threshold_adjusted - 0.05 * f(row, "missingness")

    red_flags = []
    if f(row, "threshold_risk") >= 0.50:
        red_flags.append("threshold risk")
    if f(row, "justice_visibility") <= 0.52:
        red_flags.append("low justice visibility")
    if f(row, "missingness") >= 0.24:
        red_flags.append("high missingness")
    if f(row, "buffer_capacity") <= 0.55:
        red_flags.append("low buffer capacity")
    if f(row, "adaptive_capacity") <= 0.58:
        red_flags.append("low adaptive capacity")

    return {
        "system_id": row["system_id"],
        "system": row["system"],
        "system_domain": row["system_domain"],
        "critical_function": row["critical_function"],
        "naive_score": round(naive_score, 5),
        "threshold_adjusted_score": round(threshold_adjusted, 5),
        "uncertainty_adjusted_score": round(uncertainty_adjusted, 5),
        "threshold_risk": row["threshold_risk"],
        "missingness": row["missingness"],
        "justice_visibility": row["justice_visibility"],
        "red_flag_count": len(red_flags),
        "red_flags": "; ".join(red_flags) if red_flags else "none",
    }


def scenario_rankings(designs: list[dict[str, str]], scenarios: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for scenario in scenarios:
        scored = []
        for design in designs:
            value = score_design(design, scenario)
            scored.append((value, design))
        scored.sort(key=lambda item: item[0], reverse=True)

        for rank, (value, design) in enumerate(scored, start=1):
            rows.append(
                {
                    "scenario": scenario["scenario"],
                    "dashboard_id": design["dashboard_id"],
                    "dashboard": design["dashboard"],
                    "dashboard_type": design["dashboard_type"],
                    "rank": rank,
                    "dashboard_value": round(value, 5),
                    "dashboard_risk": design["dashboard_risk"],
                    "critical_use": design["critical_use"],
                }
            )
    return rows


def design_monte_carlo(
    designs: list[dict[str, str]],
    scenario: dict[str, str],
    n: int = 3000,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rng = random.Random(42)
    simulation_rows = []

    for simulation_id in range(n):
        scored = []
        for design in designs:
            sampled = dict(design)

            for criterion in BENEFIT_CRITERIA + ["dashboard_risk"]:
                sampled_value = max(1.0, min(10.0, f(design, criterion) + rng.gauss(0, 0.6)))
                sampled[criterion] = str(sampled_value)

            value = score_design(sampled, scenario)
            scored.append((value, design))

        scored.sort(key=lambda item: item[0], reverse=True)

        for rank, (value, design) in enumerate(scored, start=1):
            simulation_rows.append(
                {
                    "simulation_id": simulation_id,
                    "dashboard_id": design["dashboard_id"],
                    "dashboard": design["dashboard"],
                    "rank": rank,
                    "dashboard_value": round(value, 5),
                    "winner": scored[0][1]["dashboard"],
                }
            )

    robustness_rows = []
    design_count = len(designs)

    for design in designs:
        subset = [row for row in simulation_rows if row["dashboard_id"] == design["dashboard_id"]]
        ranks = [int(row["rank"]) for row in subset]
        values = [float(row["dashboard_value"]) for row in subset]
        robustness_rows.append(
            {
                "dashboard_id": design["dashboard_id"],
                "dashboard": design["dashboard"],
                "mean_dashboard_value": round(mean(values), 5),
                "median_dashboard_value": round(median(values), 5),
                "probability_ranked_first": round(100 * sum(1 for r in ranks if r == 1) / n, 2),
                "probability_top_two": round(100 * sum(1 for r in ranks if r <= 2) / n, 2),
                "probability_bottom_two": round(100 * sum(1 for r in ranks if r >= design_count - 1) / n, 2),
            }
        )

    robustness_rows.sort(key=lambda row: row["probability_ranked_first"], reverse=True)
    return simulation_rows, robustness_rows


def system_monte_carlo(
    systems: list[dict[str, str]],
    n: int = 3000,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rng = random.Random(100)
    rows = []

    for simulation_id in range(n):
        scored = []
        for system in systems:
            sampled = dict(system)
            for criterion in SYSTEM_BENEFITS + ["threshold_risk", "missingness"]:
                sampled_value = max(0.0, min(1.0, f(system, criterion) + rng.gauss(0, 0.06)))
                sampled[criterion] = str(sampled_value)
            scored_row = score_system(sampled)
            scored.append((float(scored_row["uncertainty_adjusted_score"]), scored_row))

        scored.sort(key=lambda item: item[0], reverse=True)

        for rank, (_, row) in enumerate(scored, start=1):
            rows.append(
                {
                    "simulation_id": simulation_id,
                    "system_id": row["system_id"],
                    "system": row["system"],
                    "rank": rank,
                    "naive_score": row["naive_score"],
                    "threshold_adjusted_score": row["threshold_adjusted_score"],
                    "uncertainty_adjusted_score": row["uncertainty_adjusted_score"],
                    "red_flag_count": row["red_flag_count"],
                    "red_flags": row["red_flags"],
                    "winner": scored[0][1]["system"],
                }
            )

    summary_rows = []
    system_count = len(systems)

    for system in systems:
        subset = [row for row in rows if row["system_id"] == system["system_id"]]
        adjusted = [float(row["uncertainty_adjusted_score"]) for row in subset]
        ranks = [int(row["rank"]) for row in subset]
        red_flags = [int(row["red_flag_count"]) for row in subset]

        summary_rows.append(
            {
                "system_id": system["system_id"],
                "system": system["system"],
                "mean_uncertainty_adjusted_score": round(mean(adjusted), 5),
                "probability_ranked_first": round(100 * sum(1 for r in ranks if r == 1) / n, 2),
                "probability_top_two": round(100 * sum(1 for r in ranks if r <= 2) / n, 2),
                "probability_bottom_two": round(100 * sum(1 for r in ranks if r >= system_count - 1) / n, 2),
                "mean_red_flag_count": round(mean(red_flags), 5),
                "probability_any_red_flag": round(100 * sum(1 for c in red_flags if c > 0) / n, 2),
            }
        )

    summary_rows.sort(key=lambda row: row["mean_uncertainty_adjusted_score"], reverse=True)
    return rows, summary_rows


def main() -> None:
    designs = read_csv(DESIGNS_PATH)
    scenarios = read_csv(SCENARIOS_PATH)
    systems = read_csv(SYSTEMS_PATH)

    design_profiles = []
    for row in designs:
        value = base_dashboard_value(row)
        design_profiles.append(
            {
                "dashboard_id": row["dashboard_id"],
                "dashboard": row["dashboard"],
                "dashboard_type": row["dashboard_type"],
                "critical_use": row["critical_use"],
                "base_dashboard_value": round(value, 5),
                "indicator_coverage": row["indicator_coverage"],
                "threshold_sensitivity": row["threshold_sensitivity"],
                "justice_visibility": row["justice_visibility"],
                "uncertainty_transparency": row["uncertainty_transparency"],
                "decision_trigger_clarity": row["decision_trigger_clarity"],
                "learning_integration": row["learning_integration"],
                "dashboard_risk": row["dashboard_risk"],
                "diagnostic": design_diagnostic(row, value),
            }
        )

    system_scores = [score_system(row) for row in systems]
    system_scores.sort(key=lambda row: float(row["uncertainty_adjusted_score"]), reverse=True)

    rankings = scenario_rankings(designs, scenarios)
    baseline = next(s for s in scenarios if s["scenario"] == "Balanced")
    design_simulation, design_robustness = design_monte_carlo(designs, baseline, n=3000)
    system_simulation, system_summary = system_monte_carlo(systems, n=3000)

    first_place_summary: dict[str, int] = {}
    for row in rankings:
        if int(row["rank"]) == 1:
            first_place_summary[row["dashboard"]] = first_place_summary.get(row["dashboard"], 0) + 1

    top_rank_rows = [
        {"dashboard": dashboard, "times_ranked_first": count}
        for dashboard, count in sorted(first_place_summary.items(), key=lambda item: item[1], reverse=True)
    ]

    write_csv(OUT_TABLES / "dashboard_design_profiles_standard.csv", design_profiles)
    write_csv(OUT_TABLES / "resilience_dashboard_system_scores_standard.csv", system_scores)
    write_csv(OUT_TABLES / "dashboard_design_rankings_standard.csv", rankings)
    write_csv(OUT_TABLES / "dashboard_design_top_rank_summary_standard.csv", top_rank_rows)
    write_csv(OUT_TABLES / "dashboard_design_monte_carlo_standard.csv", design_simulation)
    write_csv(OUT_TABLES / "dashboard_design_robustness_summary_standard.csv", design_robustness)
    write_csv(OUT_TABLES / "resilience_dashboard_system_monte_carlo_standard.csv", system_simulation)
    write_csv(OUT_TABLES / "resilience_dashboard_system_uncertainty_summary_standard.csv", system_summary)
    write_csv(DATA_PROCESSED / "dashboard_design_profiles_standard.csv", design_profiles)

    print("Resilience dashboard workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    print("Dashboard design diagnostics:")
    for row in design_profiles:
        print(
            f"  {row['dashboard']}: value={row['base_dashboard_value']} "
            f"diagnostic={row['diagnostic']}"
        )
    print("System dashboard red flags:")
    for row in system_scores:
        print(
            f"  {row['system']}: adjusted_score={row['uncertainty_adjusted_score']} "
            f"red_flags={row['red_flags']}"
        )


if __name__ == "__main__":
    main()
