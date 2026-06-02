-- Community Resilience schema.

CREATE TABLE IF NOT EXISTS community_resilience_strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    social_capital REAL NOT NULL,
    institutional_capacity REAL NOT NULL,
    infrastructure_access REAL NOT NULL,
    economic_security REAL NOT NULL,
    information_quality REAL NOT NULL,
    adaptive_capacity REAL NOT NULL,
    equity_protection REAL NOT NULL,
    implementation_burden REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS community_systems (
    system_id TEXT PRIMARY KEY,
    system TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    baseline_function REAL NOT NULL,
    hazard_exposure REAL NOT NULL,
    chronic_stress REAL NOT NULL,
    social_capital REAL NOT NULL,
    institutional_capacity REAL NOT NULL,
    infrastructure_access REAL NOT NULL,
    economic_security REAL NOT NULL,
    information_quality REAL NOT NULL,
    adaptive_capacity REAL NOT NULL,
    equity_sensitivity REAL NOT NULL,
    dependency_coupling REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS community_stress_events (
    event_id TEXT PRIMARY KEY,
    event_name TEXT NOT NULL,
    primary_stress TEXT NOT NULL,
    hazard_intensity REAL NOT NULL,
    service_disruption REAL NOT NULL,
    institutional_pressure REAL NOT NULL,
    communication_stress REAL NOT NULL,
    economic_shock REAL NOT NULL,
    care_burden REAL NOT NULL,
    equity_burden REAL NOT NULL,
    dependency_amplification REAL NOT NULL,
    affected_functions TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS community_resilience_scenarios (
    scenario TEXT PRIMARY KEY,
    social_capital_weight REAL NOT NULL,
    institutional_capacity_weight REAL NOT NULL,
    infrastructure_access_weight REAL NOT NULL,
    economic_security_weight REAL NOT NULL,
    information_quality_weight REAL NOT NULL,
    adaptive_capacity_weight REAL NOT NULL,
    equity_protection_weight REAL NOT NULL,
    implementation_burden_weight REAL NOT NULL,
    description TEXT
);

CREATE VIEW IF NOT EXISTS base_community_resilience_value_view AS
SELECT
    strategy_id,
    strategy,
    system_domain,
    critical_function,
    social_capital,
    institutional_capacity,
    infrastructure_access,
    economic_security,
    information_quality,
    adaptive_capacity,
    equity_protection,
    implementation_burden,
    (
        0.14 * social_capital +
        0.14 * institutional_capacity +
        0.14 * infrastructure_access +
        0.13 * economic_security +
        0.13 * information_quality +
        0.15 * adaptive_capacity +
        0.15 * equity_protection -
        0.02 * implementation_burden
    ) AS base_resilience_value
FROM community_resilience_strategies;
