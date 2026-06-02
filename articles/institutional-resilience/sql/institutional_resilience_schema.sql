-- Institutional Resilience schema.

CREATE TABLE IF NOT EXISTS institutional_resilience_strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    legitimacy REAL NOT NULL,
    capacity REAL NOT NULL,
    flexibility REAL NOT NULL,
    coordination REAL NOT NULL,
    learning REAL NOT NULL,
    accountability REAL NOT NULL,
    equity_protection REAL NOT NULL,
    implementation_burden REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS institutional_systems (
    system_id TEXT PRIMARY KEY,
    system TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    baseline_function REAL NOT NULL,
    stress_exposure REAL NOT NULL,
    chronic_stress REAL NOT NULL,
    legitimacy REAL NOT NULL,
    capacity REAL NOT NULL,
    flexibility REAL NOT NULL,
    coordination REAL NOT NULL,
    learning REAL NOT NULL,
    accountability REAL NOT NULL,
    equity_sensitivity REAL NOT NULL,
    dependency_coupling REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS institutional_stress_events (
    event_id TEXT PRIMARY KEY,
    event_name TEXT NOT NULL,
    primary_stress TEXT NOT NULL,
    shock_intensity REAL NOT NULL,
    legitimacy_pressure REAL NOT NULL,
    capacity_burden REAL NOT NULL,
    coordination_stress REAL NOT NULL,
    information_stress REAL NOT NULL,
    legal_accountability_stress REAL NOT NULL,
    equity_burden REAL NOT NULL,
    dependency_amplification REAL NOT NULL,
    affected_functions TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS institutional_resilience_scenarios (
    scenario TEXT PRIMARY KEY,
    legitimacy_weight REAL NOT NULL,
    capacity_weight REAL NOT NULL,
    flexibility_weight REAL NOT NULL,
    coordination_weight REAL NOT NULL,
    learning_weight REAL NOT NULL,
    accountability_weight REAL NOT NULL,
    equity_protection_weight REAL NOT NULL,
    implementation_burden_weight REAL NOT NULL,
    description TEXT
);

CREATE VIEW IF NOT EXISTS base_institutional_resilience_value_view AS
SELECT
    strategy_id,
    strategy,
    system_domain,
    critical_function,
    legitimacy,
    capacity,
    flexibility,
    coordination,
    learning,
    accountability,
    equity_protection,
    implementation_burden,
    (
        0.14 * legitimacy +
        0.14 * capacity +
        0.13 * flexibility +
        0.14 * coordination +
        0.14 * learning +
        0.14 * accountability +
        0.15 * equity_protection -
        0.02 * implementation_burden
    ) AS base_resilience_value,
    CASE
        WHEN MIN(legitimacy, capacity, coordination, accountability, equity_protection) < 8.0
        THEN 8.0 - MIN(legitimacy, capacity, coordination, accountability, equity_protection)
        ELSE 0
    END AS threshold_risk
FROM institutional_resilience_strategies;
