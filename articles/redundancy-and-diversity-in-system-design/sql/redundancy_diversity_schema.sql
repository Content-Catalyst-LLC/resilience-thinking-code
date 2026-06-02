-- Redundancy and Diversity in System Design schema
-- Supports strategies, criteria, scenarios, model runs, and outputs.

CREATE TABLE IF NOT EXISTS redundancy_diversity_strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    redundancy REAL NOT NULL,
    diversity REAL NOT NULL,
    response_diversity REAL NOT NULL,
    coordination_capacity REAL NOT NULL,
    justice_contribution REAL NOT NULL,
    maintenance_reliability REAL NOT NULL,
    common_mode_risk REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS redundancy_diversity_scenarios (
    scenario TEXT PRIMARY KEY,
    redundancy_weight REAL NOT NULL,
    diversity_weight REAL NOT NULL,
    response_diversity_weight REAL NOT NULL,
    coordination_capacity_weight REAL NOT NULL,
    justice_contribution_weight REAL NOT NULL,
    maintenance_reliability_weight REAL NOT NULL,
    common_mode_risk_weight REAL NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS redundancy_diversity_criteria (
    criterion TEXT PRIMARY KEY,
    definition TEXT NOT NULL,
    measurement_note TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS model_runs (
    run_id TEXT PRIMARY KEY,
    model_name TEXT NOT NULL,
    model_purpose TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS model_outputs (
    output_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL REFERENCES model_runs(run_id),
    output_name TEXT NOT NULL,
    output_path TEXT NOT NULL,
    interpretation_note TEXT
);

CREATE VIEW IF NOT EXISTS base_resilience_value_view AS
SELECT
    strategy_id,
    strategy,
    system_domain,
    critical_function,
    redundancy,
    diversity,
    response_diversity,
    coordination_capacity,
    justice_contribution,
    maintenance_reliability,
    common_mode_risk,
    (
        0.22 * redundancy +
        0.18 * diversity +
        0.22 * response_diversity +
        0.13 * coordination_capacity +
        0.10 * justice_contribution +
        0.07 * maintenance_reliability -
        0.08 * common_mode_risk
    ) AS base_resilience_value
FROM redundancy_diversity_strategies;

CREATE VIEW IF NOT EXISTS common_mode_review_view AS
SELECT
    strategy_id,
    strategy,
    system_domain,
    common_mode_risk,
    CASE
        WHEN common_mode_risk >= 4.0 THEN 'common-mode failure review needed'
        WHEN common_mode_risk >= 3.7 THEN 'moderate common-mode risk'
        ELSE 'manageable common-mode risk'
    END AS common_mode_diagnostic
FROM redundancy_diversity_strategies;
