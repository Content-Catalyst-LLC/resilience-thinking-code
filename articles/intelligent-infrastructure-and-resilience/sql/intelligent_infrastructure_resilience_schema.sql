-- Intelligent Infrastructure and Resilience schema.

CREATE TABLE IF NOT EXISTS intelligent_infrastructure_strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    monitoring_value REAL NOT NULL,
    predictive_maintenance REAL NOT NULL,
    cyber_physical_security REAL NOT NULL,
    digital_twin_capacity REAL NOT NULL,
    redundancy_and_fallback REAL NOT NULL,
    climate_adaptation REAL NOT NULL,
    governance_quality REAL NOT NULL,
    equity_performance REAL NOT NULL,
    ecological_integration REAL NOT NULL,
    fragility_risk REAL NOT NULL,
    implementation_burden REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS intelligent_infrastructure_systems (
    system_id TEXT PRIMARY KEY,
    system TEXT NOT NULL,
    system_context TEXT NOT NULL,
    initial_function REAL NOT NULL,
    physical_robustness REAL NOT NULL,
    monitoring_value REAL NOT NULL,
    predictive_maintenance REAL NOT NULL,
    cyber_physical_security REAL NOT NULL,
    redundancy REAL NOT NULL,
    governance REAL NOT NULL,
    equity_performance REAL NOT NULL,
    ecological_adaptation REAL NOT NULL,
    initial_backlog REAL NOT NULL,
    initial_operator_strain REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS intelligent_infrastructure_events (
    event_id TEXT PRIMARY KEY,
    event_name TEXT NOT NULL,
    primary_stress TEXT NOT NULL,
    shock_intensity REAL NOT NULL,
    climate_stress REAL NOT NULL,
    cyber_stress REAL NOT NULL,
    data_stress REAL NOT NULL,
    dependency_stress REAL NOT NULL,
    maintenance_stress REAL NOT NULL,
    operator_stress REAL NOT NULL,
    equity_pressure REAL NOT NULL,
    governance_pressure REAL NOT NULL,
    affected_functions TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS intelligent_infrastructure_scenarios (
    scenario TEXT PRIMARY KEY,
    monitoring_value_weight REAL NOT NULL,
    predictive_maintenance_weight REAL NOT NULL,
    cyber_physical_security_weight REAL NOT NULL,
    digital_twin_capacity_weight REAL NOT NULL,
    redundancy_and_fallback_weight REAL NOT NULL,
    climate_adaptation_weight REAL NOT NULL,
    governance_quality_weight REAL NOT NULL,
    equity_performance_weight REAL NOT NULL,
    ecological_integration_weight REAL NOT NULL,
    fragility_risk_weight REAL NOT NULL,
    implementation_burden_weight REAL NOT NULL,
    description TEXT
);

CREATE VIEW IF NOT EXISTS intelligent_infrastructure_value_view AS
SELECT
    strategy_id,
    strategy,
    system_domain,
    critical_function,
    monitoring_value,
    predictive_maintenance,
    cyber_physical_security,
    digital_twin_capacity,
    redundancy_and_fallback,
    climate_adaptation,
    governance_quality,
    equity_performance,
    ecological_integration,
    fragility_risk,
    implementation_burden,
    (
        0.10 * monitoring_value +
        0.11 * predictive_maintenance +
        0.11 * cyber_physical_security +
        0.10 * digital_twin_capacity +
        0.11 * redundancy_and_fallback +
        0.11 * climate_adaptation +
        0.12 * governance_quality +
        0.12 * equity_performance +
        0.10 * ecological_integration -
        0.04 * fragility_risk -
        0.04 * implementation_burden
    ) AS infrastructure_resilience_value
FROM intelligent_infrastructure_strategies;
