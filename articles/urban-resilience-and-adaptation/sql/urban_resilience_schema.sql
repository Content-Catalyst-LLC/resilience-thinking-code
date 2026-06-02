-- Urban Resilience and Adaptation schema
-- Supports strategies, urban systems, stress events, criteria, scenarios,
-- dependencies, model runs, and outputs.

CREATE TABLE IF NOT EXISTS urban_resilience_strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    exposure_reduction REAL NOT NULL,
    vulnerability_reduction REAL NOT NULL,
    service_continuity REAL NOT NULL,
    adaptive_capacity REAL NOT NULL,
    ecological_buffering REAL NOT NULL,
    equity_protection REAL NOT NULL,
    maladaptation_risk REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS urban_systems (
    system_id TEXT PRIMARY KEY,
    system TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    baseline_function REAL NOT NULL,
    hazard_exposure REAL NOT NULL,
    chronic_stress REAL NOT NULL,
    infrastructure_support REAL NOT NULL,
    community_capacity REAL NOT NULL,
    ecological_condition REAL NOT NULL,
    adaptive_capacity REAL NOT NULL,
    equity_sensitivity REAL NOT NULL,
    dependency_coupling REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS urban_stress_events (
    event_id TEXT PRIMARY KEY,
    event_name TEXT NOT NULL,
    primary_stress TEXT NOT NULL,
    hazard_intensity REAL NOT NULL,
    infrastructure_disruption REAL NOT NULL,
    health_burden REAL NOT NULL,
    housing_stress REAL NOT NULL,
    market_stress REAL NOT NULL,
    equity_burden REAL NOT NULL,
    dependency_amplification REAL NOT NULL,
    affected_functions TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS urban_resilience_scenarios (
    scenario TEXT PRIMARY KEY,
    exposure_reduction_weight REAL NOT NULL,
    vulnerability_reduction_weight REAL NOT NULL,
    service_continuity_weight REAL NOT NULL,
    adaptive_capacity_weight REAL NOT NULL,
    ecological_buffering_weight REAL NOT NULL,
    equity_protection_weight REAL NOT NULL,
    maladaptation_risk_weight REAL NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS urban_resilience_criteria (
    criterion TEXT PRIMARY KEY,
    definition TEXT NOT NULL,
    measurement_note TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS urban_dependencies (
    dependency_id TEXT PRIMARY KEY,
    source_system_id TEXT NOT NULL REFERENCES urban_systems(system_id),
    target_system_id TEXT NOT NULL REFERENCES urban_systems(system_id),
    dependency_type TEXT NOT NULL,
    coupling_strength REAL NOT NULL,
    failure_consequence TEXT NOT NULL
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

CREATE VIEW IF NOT EXISTS base_urban_resilience_value_view AS
SELECT
    strategy_id,
    strategy,
    system_domain,
    critical_function,
    exposure_reduction,
    vulnerability_reduction,
    service_continuity,
    adaptive_capacity,
    ecological_buffering,
    equity_protection,
    maladaptation_risk,
    (
        0.16 * exposure_reduction +
        0.17 * vulnerability_reduction +
        0.17 * service_continuity +
        0.15 * adaptive_capacity +
        0.14 * ecological_buffering +
        0.15 * equity_protection -
        0.06 * maladaptation_risk
    ) AS base_resilience_value
FROM urban_resilience_strategies;

CREATE VIEW IF NOT EXISTS urban_event_stress_load_view AS
SELECT
    event_id,
    event_name,
    primary_stress,
    hazard_intensity,
    infrastructure_disruption,
    health_burden,
    housing_stress,
    market_stress,
    equity_burden,
    dependency_amplification,
    (
        0.25 * hazard_intensity +
        0.19 * infrastructure_disruption +
        0.17 * health_burden +
        0.17 * housing_stress +
        0.10 * market_stress +
        0.12 * dependency_amplification
    ) AS event_stress_load
FROM urban_stress_events;
