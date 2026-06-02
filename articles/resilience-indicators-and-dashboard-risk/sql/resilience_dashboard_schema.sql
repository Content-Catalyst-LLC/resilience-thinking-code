-- Resilience Indicators and Dashboard Risk schema
-- Supports dashboard designs, indicators, systems, scores, thresholds,
-- missingness, scenarios, model runs, and outputs.

CREATE TABLE IF NOT EXISTS dashboard_designs (
    dashboard_id TEXT PRIMARY KEY,
    dashboard TEXT NOT NULL,
    dashboard_type TEXT NOT NULL,
    indicator_coverage REAL NOT NULL,
    threshold_sensitivity REAL NOT NULL,
    justice_visibility REAL NOT NULL,
    uncertainty_transparency REAL NOT NULL,
    decision_trigger_clarity REAL NOT NULL,
    learning_integration REAL NOT NULL,
    dashboard_risk REAL NOT NULL,
    critical_use TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS resilience_systems (
    system_id TEXT PRIMARY KEY,
    system TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    exposure_reduction REAL NOT NULL,
    recovery_capacity REAL NOT NULL,
    adaptive_capacity REAL NOT NULL,
    buffer_capacity REAL NOT NULL,
    justice_visibility REAL NOT NULL,
    threshold_risk REAL NOT NULL,
    missingness REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS indicator_catalog (
    indicator_id TEXT PRIMARY KEY,
    indicator TEXT NOT NULL,
    domain TEXT NOT NULL,
    definition TEXT NOT NULL,
    measurement_note TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dashboard_red_flag_rules (
    rule_id TEXT PRIMARY KEY,
    rule_name TEXT NOT NULL,
    condition TEXT NOT NULL,
    meaning TEXT NOT NULL,
    recommended_response TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dashboard_scenarios (
    scenario TEXT PRIMARY KEY,
    indicator_coverage_weight REAL NOT NULL,
    threshold_sensitivity_weight REAL NOT NULL,
    justice_visibility_weight REAL NOT NULL,
    uncertainty_transparency_weight REAL NOT NULL,
    decision_trigger_clarity_weight REAL NOT NULL,
    learning_integration_weight REAL NOT NULL,
    dashboard_risk_weight REAL NOT NULL,
    description TEXT
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

CREATE VIEW IF NOT EXISTS base_dashboard_value_view AS
SELECT
    dashboard_id,
    dashboard,
    dashboard_type,
    critical_use,
    indicator_coverage,
    threshold_sensitivity,
    justice_visibility,
    uncertainty_transparency,
    decision_trigger_clarity,
    learning_integration,
    dashboard_risk,
    (
        0.15 * indicator_coverage +
        0.17 * threshold_sensitivity +
        0.16 * justice_visibility +
        0.14 * uncertainty_transparency +
        0.16 * decision_trigger_clarity +
        0.14 * learning_integration -
        0.08 * dashboard_risk
    ) AS base_dashboard_value
FROM dashboard_designs;

CREATE VIEW IF NOT EXISTS resilience_system_dashboard_scores_view AS
SELECT
    system_id,
    system,
    system_domain,
    critical_function,
    (
        0.17 * exposure_reduction +
        0.18 * recovery_capacity +
        0.19 * adaptive_capacity +
        0.16 * buffer_capacity +
        0.16 * justice_visibility
    ) AS naive_score,
    (
        0.17 * exposure_reduction +
        0.18 * recovery_capacity +
        0.19 * adaptive_capacity +
        0.16 * buffer_capacity +
        0.16 * justice_visibility -
        0.09 * threshold_risk
    ) AS threshold_adjusted_score,
    (
        0.17 * exposure_reduction +
        0.18 * recovery_capacity +
        0.19 * adaptive_capacity +
        0.16 * buffer_capacity +
        0.16 * justice_visibility -
        0.09 * threshold_risk -
        0.05 * missingness
    ) AS uncertainty_adjusted_score
FROM resilience_systems;
