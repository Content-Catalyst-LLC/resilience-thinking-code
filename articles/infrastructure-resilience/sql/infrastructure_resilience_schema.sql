-- Infrastructure Resilience schema
-- Supports strategies, systems, stress events, criteria, scenarios,
-- model runs, dependencies, and outputs.

CREATE TABLE IF NOT EXISTS infrastructure_resilience_strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    service_continuity REAL NOT NULL,
    redundancy REAL NOT NULL,
    recovery_speed REAL NOT NULL,
    adaptive_capacity REAL NOT NULL,
    equity_protection REAL NOT NULL,
    cascading_exposure REAL NOT NULL,
    critical_service TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS infrastructure_systems (
    system_id TEXT PRIMARY KEY,
    system TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    baseline_service REAL NOT NULL,
    shock_exposure REAL NOT NULL,
    chronic_stress REAL NOT NULL,
    redundancy_capacity REAL NOT NULL,
    recovery_capacity REAL NOT NULL,
    adaptive_capacity REAL NOT NULL,
    equity_sensitivity REAL NOT NULL,
    interdependence_coupling REAL NOT NULL,
    critical_service TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS infrastructure_stress_events (
    event_id TEXT PRIMARY KEY,
    event_name TEXT NOT NULL,
    primary_hazard TEXT NOT NULL,
    shock_intensity REAL NOT NULL,
    chronic_stress REAL NOT NULL,
    compound_risk REAL NOT NULL,
    cascading_dependency REAL NOT NULL,
    equity_burden REAL NOT NULL,
    affected_services TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS infrastructure_resilience_scenarios (
    scenario TEXT PRIMARY KEY,
    service_continuity_weight REAL NOT NULL,
    redundancy_weight REAL NOT NULL,
    recovery_speed_weight REAL NOT NULL,
    adaptive_capacity_weight REAL NOT NULL,
    equity_protection_weight REAL NOT NULL,
    cascading_exposure_weight REAL NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS infrastructure_resilience_criteria (
    criterion TEXT PRIMARY KEY,
    definition TEXT NOT NULL,
    measurement_note TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS infrastructure_dependencies (
    dependency_id TEXT PRIMARY KEY,
    source_system_id TEXT NOT NULL REFERENCES infrastructure_systems(system_id),
    target_system_id TEXT NOT NULL REFERENCES infrastructure_systems(system_id),
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

CREATE VIEW IF NOT EXISTS base_infrastructure_resilience_value_view AS
SELECT
    strategy_id,
    strategy,
    system_domain,
    critical_service,
    service_continuity,
    redundancy,
    recovery_speed,
    adaptive_capacity,
    equity_protection,
    cascading_exposure,
    (
        0.22 * service_continuity +
        0.20 * redundancy +
        0.18 * recovery_speed +
        0.16 * adaptive_capacity +
        0.16 * equity_protection -
        0.08 * cascading_exposure
    ) AS base_resilience_value
FROM infrastructure_resilience_strategies;

CREATE VIEW IF NOT EXISTS infrastructure_event_stress_load_view AS
SELECT
    event_id,
    event_name,
    primary_hazard,
    shock_intensity,
    chronic_stress,
    compound_risk,
    cascading_dependency,
    equity_burden,
    (
        0.34 * shock_intensity +
        0.18 * chronic_stress +
        0.18 * compound_risk +
        0.18 * cascading_dependency
    ) AS event_stress_load
FROM infrastructure_stress_events;
