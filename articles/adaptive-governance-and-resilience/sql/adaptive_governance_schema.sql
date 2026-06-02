-- Adaptive Governance and Resilience schema.

CREATE TABLE IF NOT EXISTS adaptive_governance_strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    learning_capacity REAL NOT NULL,
    flexibility REAL NOT NULL,
    coordination REAL NOT NULL,
    knowledge_integration REAL NOT NULL,
    legitimacy REAL NOT NULL,
    accountability REAL NOT NULL,
    equity_protection REAL NOT NULL,
    implementation_burden REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS governance_systems (
    system_id TEXT PRIMARY KEY,
    system TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    baseline_function REAL NOT NULL,
    uncertainty_exposure REAL NOT NULL,
    chronic_governance_stress REAL NOT NULL,
    learning_capacity REAL NOT NULL,
    flexibility REAL NOT NULL,
    coordination REAL NOT NULL,
    knowledge_integration REAL NOT NULL,
    legitimacy REAL NOT NULL,
    accountability REAL NOT NULL,
    equity_sensitivity REAL NOT NULL,
    dependency_coupling REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS governance_stress_events (
    event_id TEXT PRIMARY KEY,
    event_name TEXT NOT NULL,
    primary_stress TEXT NOT NULL,
    shock_intensity REAL NOT NULL,
    uncertainty_pressure REAL NOT NULL,
    coordination_stress REAL NOT NULL,
    legitimacy_pressure REAL NOT NULL,
    information_stress REAL NOT NULL,
    legal_accountability_stress REAL NOT NULL,
    equity_burden REAL NOT NULL,
    dependency_amplification REAL NOT NULL,
    affected_functions TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS adaptive_governance_scenarios (
    scenario TEXT PRIMARY KEY,
    learning_capacity_weight REAL NOT NULL,
    flexibility_weight REAL NOT NULL,
    coordination_weight REAL NOT NULL,
    knowledge_integration_weight REAL NOT NULL,
    legitimacy_weight REAL NOT NULL,
    accountability_weight REAL NOT NULL,
    equity_protection_weight REAL NOT NULL,
    implementation_burden_weight REAL NOT NULL,
    description TEXT
);

CREATE VIEW IF NOT EXISTS adaptive_governance_value_view AS
SELECT
    strategy_id,
    strategy,
    system_domain,
    critical_function,
    learning_capacity,
    flexibility,
    coordination,
    knowledge_integration,
    legitimacy,
    accountability,
    equity_protection,
    implementation_burden,
    (
        0.15 * learning_capacity +
        0.14 * flexibility +
        0.14 * coordination +
        0.14 * knowledge_integration +
        0.14 * legitimacy +
        0.14 * accountability +
        0.15 * equity_protection -
        0.02 * implementation_burden
    ) AS adaptive_governance_value,
    CASE
        WHEN flexibility > accountability
        THEN flexibility - accountability
        ELSE 0
    END AS accountability_gap
FROM adaptive_governance_strategies;
