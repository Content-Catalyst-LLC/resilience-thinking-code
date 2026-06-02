-- Food and Water Resilience schema
-- Supports strategies, systems, stress events, criteria, scenarios,
-- model runs, dependencies, and outputs.

CREATE TABLE IF NOT EXISTS food_water_resilience_strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    availability REAL NOT NULL,
    access REAL NOT NULL,
    stability REAL NOT NULL,
    quality REAL NOT NULL,
    adaptive_capacity REAL NOT NULL,
    equity_protection REAL NOT NULL,
    resource_depletion_risk REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS food_water_systems (
    system_id TEXT PRIMARY KEY,
    system TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    baseline_performance REAL NOT NULL,
    climate_exposure REAL NOT NULL,
    market_exposure REAL NOT NULL,
    infrastructure_support REAL NOT NULL,
    ecosystem_condition REAL NOT NULL,
    adaptive_capacity REAL NOT NULL,
    equity_sensitivity REAL NOT NULL,
    resource_coupling REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS food_water_stress_events (
    event_id TEXT PRIMARY KEY,
    event_name TEXT NOT NULL,
    primary_stress TEXT NOT NULL,
    climate_stress REAL NOT NULL,
    market_volatility REAL NOT NULL,
    infrastructure_disruption REAL NOT NULL,
    ecosystem_stress REAL NOT NULL,
    equity_burden REAL NOT NULL,
    affected_functions TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS food_water_resilience_scenarios (
    scenario TEXT PRIMARY KEY,
    availability_weight REAL NOT NULL,
    access_weight REAL NOT NULL,
    stability_weight REAL NOT NULL,
    quality_weight REAL NOT NULL,
    adaptive_capacity_weight REAL NOT NULL,
    equity_protection_weight REAL NOT NULL,
    resource_depletion_risk_weight REAL NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS food_water_resilience_criteria (
    criterion TEXT PRIMARY KEY,
    definition TEXT NOT NULL,
    measurement_note TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS food_water_dependencies (
    dependency_id TEXT PRIMARY KEY,
    source_system_id TEXT NOT NULL REFERENCES food_water_systems(system_id),
    target_system_id TEXT NOT NULL REFERENCES food_water_systems(system_id),
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

CREATE VIEW IF NOT EXISTS base_food_water_resilience_value_view AS
SELECT
    strategy_id,
    strategy,
    system_domain,
    critical_function,
    availability,
    access,
    stability,
    quality,
    adaptive_capacity,
    equity_protection,
    resource_depletion_risk,
    (
        0.17 * availability +
        0.17 * access +
        0.16 * stability +
        0.14 * quality +
        0.16 * adaptive_capacity +
        0.14 * equity_protection -
        0.06 * resource_depletion_risk
    ) AS base_resilience_value
FROM food_water_resilience_strategies;

CREATE VIEW IF NOT EXISTS food_water_event_stress_load_view AS
SELECT
    event_id,
    event_name,
    primary_stress,
    climate_stress,
    market_volatility,
    infrastructure_disruption,
    ecosystem_stress,
    equity_burden,
    (
        0.30 * climate_stress +
        0.20 * market_volatility +
        0.18 * infrastructure_disruption +
        0.20 * ecosystem_stress
    ) AS event_stress_load
FROM food_water_stress_events;
