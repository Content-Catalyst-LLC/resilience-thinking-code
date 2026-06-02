#!/usr/bin/env python3
"""
Dependency-light transformation pathway workflow.

Reads synthetic transformation pathways and scenario weights, calculates
pathway rankings, transformation readiness, structural-risk diagnostics,
and deterministic uncertainty samples using only the Python standard library.

Run:
    python3 python/transformation_standard.py
"""

from __future__ import annotations

import csv
import random
from pathlib import Path
from statistics import mean, median


ROOT = Path(__file__).resolve().parents[1]
PATHWAYS_PATH = ROOT / "data" / "raw" / "transformation_pathways.csv"
SCENARIOS_PATH = ROOT / "data" / "raw" / "transformation_scenarios.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
DATA_PROCESSED = ROOT / "data" / "processed"
OUT_TABLES.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

BENEFIT_CRITERIA = [
    "adaptive_support",
    "transformability",
    "governance_readiness",
    "justice_contribution",
    "ecological_viability",
    "legitimacy",
    "resource_feasibility",
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


def transformation_readiness(row: dict[str, str]) -> float:
    return (
        0.18 * f(row, "adaptive_support")
        + 0.20 * f(row, "transformability")
        + 0.18 * f(row, "governance_readiness")
        + 0.16 * f(row, "justice_contribution")
        + 0.14 * f(row, "ecological_viability")
        + 0.08 * f(row, "legitimacy")
        + 0.06 * f(row, "resource_feasibility")
        - 0.10 * f(row, "structural_risk")
    )


def score_pathway(row: dict[str, str], scenario: dict[str, str]) -> float:
    return (
        f(scenario, "adaptive_support_weight") * f(row, "adaptive_support")
        + f(scenario, "transformability_weight") * f(row, "transformability")
        + f(scenario, "governance_readiness_weight") * f(row, "governance_readiness")
        + f(scenario, "justice_contribution_weight") * f(row, "justice_contribution")
        + f(scenario, "ecological_viability_weight") * f(row, "ecological_viability")
        + f(scenario, "legitimacy_weight") * f(row, "legitimacy")
        + f(scenario, "resource_feasibility_weight") * f(row, "resource_feasibility")
        - f(scenario, "structural_risk_weight") * f(row, "structural_risk")
    )


def diagnostic(row: dict[str, str], readiness: float) -> str:
    if readiness >= 7.55 and f(row, "structural_risk") <= 4.1:
        return "high readiness with manageable structural-risk concern"
    if f(row, "justice_contribution") < 7.5:
        return "justice contribution needs stronger design"
    if f(row, "governance_readiness") < 7.4:
        return "governance readiness constraint"
    if f(row, "resource_feasibility") < 7.0:
        return "resource feasibility constraint"
    return "promising but requires participatory validation"


def scenario_rankings(pathways: list[dict[str, str]], scenarios: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for scenario in scenarios:
        scored = []
        for pathway in pathways:
            value = score_pathway(pathway, scenario)
            scored.append((value, pathway))
        scored.sort(key=lambda x: x[0], reverse=True)

        for rank, (value, pathway) in enumerate(scored, start=1):
            rows.append(
                {
                    "scenario": scenario["scenario"],
                    "pathway_id": pathway["pathway_id"],
                    "pathway": pathway["pathway"],
                    "system_domain": pathway["system_domain"],
                    "rank": rank,
                    "transformation_value": round(value, 5),
                    "structural_risk": pathway["structural_risk"],
                    "critical_function": pathway["critical_function"],
                }
            )
    return rows


def monte_carlo(pathways: list[dict[str, str]], scenario: dict[str, str], n: int = 3000) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rng = random.Random(42)
    simulation_rows = []

    for simulation_id in range(n):
        scored = []
        for pathway in pathways:
            sampled = dict(pathway)
            for criterion in BENEFIT_CRITERIA + ["structural_risk"]:
                sampled_value = max(1.0, min(10.0, f(pathway, criterion) + rng.gauss(0, 0.6)))
                sampled[criterion] = str(sampled_value)

            value = score_pathway(sampled, scenario)
            scored.append((value, pathway))

        scored.sort(key=lambda x: x[0], reverse=True)

        for rank, (value, pathway) in enumerate(scored, start=1):
            simulation_rows.append(
                {
                    "simulation_id": simulation_id,
                    "pathway_id": pathway["pathway_id"],
                    "pathway": pathway["pathway"],
                    "rank": rank,
                    "transformation_value": round(value, 5),
                    "winner": scored[0][1]["pathway"],
                }
            )

    summary_rows = []
    for pathway in pathways:
        subset = [row for row in simulation_rows if row["pathway_id"] == pathway["pathway_id"]]
        ranks = [int(row["rank"]) for row in subset]
        values = [float(row["transformation_value"]) for row in subset]
        summary_rows.append(
            {
                "pathway_id": pathway["pathway_id"],
                "pathway": pathway["pathway"],
                "mean_transformation_value": round(mean(values), 5),
                "median_transformation_value": round(median(values), 5),
                "probability_ranked_first": round(100 * sum(1 for r in ranks if r == 1) / n, 2),
                "probability_top_two": round(100 * sum(1 for r in ranks if r <= 2) / n, 2),
                "probability_bottom_two": round(100 * sum(1 for r in ranks if r >= len(pathways) - 1) / n, 2),
            }
        )

    summary_rows.sort(key=lambda row: row["probability_ranked_first"], reverse=True)
    return simulation_rows, summary_rows


def main() -> None:
    pathways = read_csv(PATHWAYS_PATH)
    scenarios = read_csv(SCENARIOS_PATH)

    profile_rows = []
    for row in pathways:
        readiness = transformation_readiness(row)
        profile_rows.append(
            {
                "pathway_id": row["pathway_id"],
                "pathway": row["pathway"],
                "system_domain": row["system_domain"],
                "critical_function": row["critical_function"],
                "transformation_readiness": round(readiness, 5),
                "adaptive_support": row["adaptive_support"],
                "transformability": row["transformability"],
                "governance_readiness": row["governance_readiness"],
                "justice_contribution": row["justice_contribution"],
                "ecological_viability": row["ecological_viability"],
                "legitimacy": row["legitimacy"],
                "resource_feasibility": row["resource_feasibility"],
                "structural_risk": row["structural_risk"],
                "diagnostic": diagnostic(row, readiness),
            }
        )

    rankings = scenario_rankings(pathways, scenarios)
    baseline = next(s for s in scenarios if s["scenario"] == "Balanced")
    simulation_rows, robustness_rows = monte_carlo(pathways, baseline, n=3000)

    first_place_summary = {}
    for row in rankings:
        if int(row["rank"]) == 1:
            first_place_summary[row["pathway"]] = first_place_summary.get(row["pathway"], 0) + 1

    top_rank_rows = [
        {"pathway": pathway, "times_ranked_first": count}
        for pathway, count in sorted(first_place_summary.items(), key=lambda item: item[1], reverse=True)
    ]

    write_csv(OUT_TABLES / "transformation_pathway_profiles_standard.csv", profile_rows)
    write_csv(OUT_TABLES / "transformation_pathway_rankings_standard.csv", rankings)
    write_csv(OUT_TABLES / "transformation_top_rank_summary_standard.csv", top_rank_rows)
    write_csv(OUT_TABLES / "transformation_monte_carlo_standard.csv", simulation_rows)
    write_csv(OUT_TABLES / "transformation_robustness_summary_standard.csv", robustness_rows)
    write_csv(DATA_PROCESSED / "transformation_pathway_profiles_standard.csv", profile_rows)

    print("Transformation pathway workflow complete.")
    print(f"Wrote outputs to: {OUT_TABLES}")
    for row in profile_rows:
        print(
            f"  {row['pathway']}: readiness={row['transformation_readiness']} "
            f"diagnostic={row['diagnostic']}"
        )


if __name__ == "__main__":
    main()
