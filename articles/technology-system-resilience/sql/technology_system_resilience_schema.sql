-- Technology System Resilience schema.

CREATE TABLE IF NOT EXISTS technology_resilience_strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    architecture REAL NOT NULL,
    redundancy REAL NOT NULL,
    observability REAL NOT NULL,
    cybersecurity REAL NOT NULL,
    data_integrity REAL NOT NULL,
    maintainability REAL NOT NULL,
    governance REAL NOT NULL,
    human_safeguards REAL NOT NULL,
    vendor_contingency REAL NOT NULL,
    technical_debt_risk REAL NOT NULL,
    implementation_burden REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS technology_system_profiles (
    system_id TEXT PRIMARY KEY,
    system TEXT NOT NULL,
    system_context TEXT NOT NULL,
    initial_function REAL NOT NULL,
    architecture REAL NOT NULL,
    redundancy REAL NOT NULL,
    observability REAL NOT NULL,
    cybersecurity REAL NOT NULL,
    data_integrity REAL NOT NULL,
    maintainability REAL NOT NULL,
    governance REAL NOT NULL,
    human_safeguards REAL NOT NULL,
    vendor_contingency REAL NOT NULL,
    technical_debt REAL NOT NULL,
    initial_human_strain REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS technology_disruption_events (
    event_id TEXT PRIMARY KEY,
    event_name TEXT NOT NULL,
    primary_stress TEXT NOT NULL,
    shock_intensity REAL NOT NULL,
    architecture_stress REAL NOT NULL,
    cloud_vendor_stress REAL NOT NULL,
    cyber_stress REAL NOT NULL,
    data_integrity_stress REAL NOT NULL,
    maintenance_stress REAL NOT NULL,
    human_operator_stress REAL NOT NULL,
    governance_stress REAL NOT NULL,
    model_drift_stress REAL NOT NULL,
    critical_function_pressure REAL NOT NULL,
    affected_functions TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS technology_resilience_scenarios (
    scenario TEXT PRIMARY KEY,
    architecture_weight REAL NOT NULL,
    redundancy_weight REAL NOT NULL,
    observability_weight REAL NOT NULL,
    cybersecurity_weight REAL NOT NULL,
    data_integrity_weight REAL NOT NULL,
    maintainability_weight REAL NOT NULL,
    governance_weight REAL NOT NULL,
    human_safeguards_weight REAL NOT NULL,
    vendor_contingency_weight REAL NOT NULL,
    technical_debt_risk_weight REAL NOT NULL,
    implementation_burden_weight REAL NOT NULL,
    description TEXT
);

CREATE VIEW IF NOT EXISTS technology_resilience_value_view AS
SELECT
    strategy_id,
    strategy,
    system_domain,
    critical_function,
    architecture,
    redundancy,
    observability,
    cybersecurity,
    data_integrity,
    maintainability,
    governance,
    human_safeguards,
    vendor_contingency,
    technical_debt_risk,
    implementation_burden,
    (
        0.10 * architecture +
        0.10 * redundancy +
        0.10 * observability +
        0.11 * cybersecurity +
        0.11 * data_integrity +
        0.11 * maintainability +
        0.11 * governance +
        0.11 * human_safeguards +
        0.10 * vendor_contingency -
        0.03 * technical_debt_risk -
        0.02 * implementation_burden
    ) AS technology_resilience_value
FROM technology_resilience_strategies;
