-- Public Health System Resilience schema.

CREATE TABLE IF NOT EXISTS public_health_resilience_strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    prevention REAL NOT NULL,
    detection REAL NOT NULL,
    service_continuity REAL NOT NULL,
    workforce_capacity REAL NOT NULL,
    adaptive_governance REAL NOT NULL,
    trust REAL NOT NULL,
    equity_protection REAL NOT NULL,
    implementation_burden REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS public_health_systems (
    system_id TEXT PRIMARY KEY,
    system TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    baseline_function REAL NOT NULL,
    hazard_exposure REAL NOT NULL,
    chronic_stress REAL NOT NULL,
    prevention_capacity REAL NOT NULL,
    detection_capacity REAL NOT NULL,
    service_continuity REAL NOT NULL,
    workforce_capacity REAL NOT NULL,
    community_trust REAL NOT NULL,
    adaptive_capacity REAL NOT NULL,
    equity_sensitivity REAL NOT NULL,
    dependency_coupling REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS public_health_stress_events (
    event_id TEXT PRIMARY KEY,
    event_name TEXT NOT NULL,
    primary_stress TEXT NOT NULL,
    hazard_intensity REAL NOT NULL,
    surge_demand REAL NOT NULL,
    service_disruption REAL NOT NULL,
    workforce_burden REAL NOT NULL,
    trust_pressure REAL NOT NULL,
    supply_chain_stress REAL NOT NULL,
    equity_burden REAL NOT NULL,
    dependency_amplification REAL NOT NULL,
    affected_functions TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS public_health_resilience_scenarios (
    scenario TEXT PRIMARY KEY,
    prevention_weight REAL NOT NULL,
    detection_weight REAL NOT NULL,
    service_continuity_weight REAL NOT NULL,
    workforce_capacity_weight REAL NOT NULL,
    adaptive_governance_weight REAL NOT NULL,
    trust_weight REAL NOT NULL,
    equity_protection_weight REAL NOT NULL,
    implementation_burden_weight REAL NOT NULL,
    description TEXT
);

CREATE VIEW IF NOT EXISTS base_public_health_resilience_value_view AS
SELECT
    strategy_id,
    strategy,
    system_domain,
    critical_function,
    prevention,
    detection,
    service_continuity,
    workforce_capacity,
    adaptive_governance,
    trust,
    equity_protection,
    implementation_burden,
    (
        0.14 * prevention +
        0.15 * detection +
        0.15 * service_continuity +
        0.14 * workforce_capacity +
        0.14 * adaptive_governance +
        0.13 * trust +
        0.13 * equity_protection -
        0.02 * implementation_burden
    ) AS base_resilience_value
FROM public_health_resilience_strategies;
