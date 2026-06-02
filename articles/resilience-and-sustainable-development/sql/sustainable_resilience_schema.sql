-- Resilience and Sustainable Development schema.

CREATE TABLE IF NOT EXISTS sustainable_resilience_pathways (
    pathway_id TEXT PRIMARY KEY,
    pathway TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    resilience REAL NOT NULL,
    ecological_integrity REAL NOT NULL,
    social_inclusion REAL NOT NULL,
    economic_sufficiency REAL NOT NULL,
    governance_capacity REAL NOT NULL,
    adaptive_capacity REAL NOT NULL,
    resource_pressure REAL NOT NULL,
    implementation_burden REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS development_systems (
    system_id TEXT PRIMARY KEY,
    system TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    baseline_development_quality REAL NOT NULL,
    climate_exposure REAL NOT NULL,
    ecological_stress REAL NOT NULL,
    social_vulnerability REAL NOT NULL,
    economic_fragility REAL NOT NULL,
    infrastructure_exposure REAL NOT NULL,
    governance_constraint REAL NOT NULL,
    adaptive_capacity REAL NOT NULL,
    equity_sensitivity REAL NOT NULL,
    resource_pressure REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS development_stress_events (
    event_id TEXT PRIMARY KEY,
    event_name TEXT NOT NULL,
    primary_stress TEXT NOT NULL,
    shock_intensity REAL NOT NULL,
    climate_stress REAL NOT NULL,
    ecological_overshoot REAL NOT NULL,
    economic_shock REAL NOT NULL,
    infrastructure_disruption REAL NOT NULL,
    governance_stress REAL NOT NULL,
    equity_burden REAL NOT NULL,
    resource_pressure_spike REAL NOT NULL,
    affected_functions TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sustainable_resilience_scenarios (
    scenario TEXT PRIMARY KEY,
    resilience_weight REAL NOT NULL,
    ecological_integrity_weight REAL NOT NULL,
    social_inclusion_weight REAL NOT NULL,
    economic_sufficiency_weight REAL NOT NULL,
    governance_capacity_weight REAL NOT NULL,
    adaptive_capacity_weight REAL NOT NULL,
    resource_pressure_weight REAL NOT NULL,
    implementation_burden_weight REAL NOT NULL,
    description TEXT
);

CREATE VIEW IF NOT EXISTS sustainable_resilience_value_view AS
SELECT
    pathway_id,
    pathway,
    system_domain,
    critical_function,
    resilience,
    ecological_integrity,
    social_inclusion,
    economic_sufficiency,
    governance_capacity,
    adaptive_capacity,
    resource_pressure,
    implementation_burden,
    (
        0.18 * resilience +
        0.17 * ecological_integrity +
        0.16 * social_inclusion +
        0.14 * economic_sufficiency +
        0.14 * governance_capacity +
        0.15 * adaptive_capacity -
        0.04 * resource_pressure -
        0.02 * implementation_burden
    ) AS viability_value
FROM sustainable_resilience_pathways;
