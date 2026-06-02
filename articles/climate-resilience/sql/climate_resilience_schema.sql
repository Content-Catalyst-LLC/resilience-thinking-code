-- Climate Resilience schema
-- Supports strategies, systems, climate stress events, scenarios,
-- indicators, model runs, and outputs.

CREATE TABLE IF NOT EXISTS climate_resilience_strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    exposure_reduction REAL NOT NULL,
    vulnerability_reduction REAL NOT NULL,
    adaptive_capacity REAL NOT NULL,
    recovery_capacity REAL NOT NULL,
    transformative_capacity REAL NOT NULL,
    justice_protection REAL NOT NULL,
    maladaptation_risk REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS climate_resilience_systems (
    system_id TEXT PRIMARY KEY,
    system TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    baseline_function REAL NOT NULL,
    exposure REAL NOT NULL,
    vulnerability REAL NOT NULL,
    adaptive_capacity REAL NOT NULL,
    recovery_capacity REAL NOT NULL,
    justice_sensitivity REAL NOT NULL,
    threshold_proximity REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS climate_stress_events (
    event_id TEXT PRIMARY KEY,
    event_name TEXT NOT NULL,
    primary_hazard TEXT NOT NULL,
    shock_intensity REAL NOT NULL,
    slow_stress REAL NOT NULL,
    compound_risk REAL NOT NULL,
    affected_systems TEXT NOT NULL,
    justice_burden REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS climate_resilience_scenarios (
    scenario TEXT PRIMARY KEY,
    exposure_reduction_weight REAL NOT NULL,
    vulnerability_reduction_weight REAL NOT NULL,
    adaptive_capacity_weight REAL NOT NULL,
    recovery_capacity_weight REAL NOT NULL,
    transformative_capacity_weight REAL NOT NULL,
    justice_protection_weight REAL NOT NULL,
    maladaptation_risk_weight REAL NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS climate_resilience_indicators (
    indicator_id TEXT PRIMARY KEY,
    indicator TEXT NOT NULL,
    dimension TEXT NOT NULL,
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

CREATE VIEW IF NOT EXISTS base_climate_resilience_value_view AS
SELECT
    strategy_id,
    strategy,
    system_domain,
    critical_function,
    exposure_reduction,
    vulnerability_reduction,
    adaptive_capacity,
    recovery_capacity,
    transformative_capacity,
    justice_protection,
    maladaptation_risk,
    (
        0.16 * exposure_reduction +
        0.16 * vulnerability_reduction +
        0.16 * adaptive_capacity +
        0.15 * recovery_capacity +
        0.15 * transformative_capacity +
        0.14 * justice_protection -
        0.08 * maladaptation_risk
    ) AS base_resilience_value
FROM climate_resilience_strategies;

CREATE VIEW IF NOT EXISTS climate_system_stress_load_view AS
SELECT
    event_id,
    event_name,
    primary_hazard,
    shock_intensity,
    slow_stress,
    compound_risk,
    justice_burden,
    (
        0.45 * shock_intensity +
        0.24 * slow_stress +
        0.18 * compound_risk
    ) AS event_stress_load
FROM climate_stress_events;
