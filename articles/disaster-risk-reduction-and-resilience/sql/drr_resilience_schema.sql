-- Disaster Risk Reduction and Resilience schema
-- Supports strategies, systems, stress events, scenarios,
-- criteria, model runs, and outputs.

CREATE TABLE IF NOT EXISTS drr_resilience_strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    hazard_reduction REAL NOT NULL,
    exposure_reduction REAL NOT NULL,
    vulnerability_reduction REAL NOT NULL,
    capacity_enhancement REAL NOT NULL,
    justice_protection REAL NOT NULL,
    maladaptation_risk REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS drr_resilience_systems (
    system_id TEXT PRIMARY KEY,
    system TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    baseline_function REAL NOT NULL,
    hazard_exposure REAL NOT NULL,
    vulnerability REAL NOT NULL,
    preparedness_capacity REAL NOT NULL,
    recovery_capacity REAL NOT NULL,
    justice_sensitivity REAL NOT NULL,
    dependency_coupling REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS disaster_stress_events (
    event_id TEXT PRIMARY KEY,
    event_name TEXT NOT NULL,
    primary_hazard TEXT NOT NULL,
    shock_intensity REAL NOT NULL,
    slow_stress REAL NOT NULL,
    compound_risk REAL NOT NULL,
    cascading_dependency REAL NOT NULL,
    justice_burden REAL NOT NULL,
    affected_systems TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS drr_resilience_scenarios (
    scenario TEXT PRIMARY KEY,
    hazard_reduction_weight REAL NOT NULL,
    exposure_reduction_weight REAL NOT NULL,
    vulnerability_reduction_weight REAL NOT NULL,
    capacity_enhancement_weight REAL NOT NULL,
    justice_protection_weight REAL NOT NULL,
    maladaptation_risk_weight REAL NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS drr_resilience_criteria (
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

CREATE VIEW IF NOT EXISTS base_drr_resilience_value_view AS
SELECT
    strategy_id,
    strategy,
    system_domain,
    critical_function,
    hazard_reduction,
    exposure_reduction,
    vulnerability_reduction,
    capacity_enhancement,
    justice_protection,
    maladaptation_risk,
    (
        0.17 * hazard_reduction +
        0.18 * exposure_reduction +
        0.18 * vulnerability_reduction +
        0.17 * capacity_enhancement +
        0.18 * justice_protection -
        0.12 * maladaptation_risk
    ) AS base_drr_value
FROM drr_resilience_strategies;

CREATE VIEW IF NOT EXISTS disaster_event_stress_load_view AS
SELECT
    event_id,
    event_name,
    primary_hazard,
    shock_intensity,
    slow_stress,
    compound_risk,
    cascading_dependency,
    justice_burden,
    (
        0.38 * shock_intensity +
        0.20 * slow_stress +
        0.18 * compound_risk +
        0.16 * cascading_dependency
    ) AS event_stress_load
FROM disaster_stress_events;
