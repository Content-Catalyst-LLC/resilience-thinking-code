-- AI and Resilience Thinking schema.

CREATE TABLE IF NOT EXISTS ai_resilience_strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    monitoring_value REAL NOT NULL,
    forecasting_value REAL NOT NULL,
    scenario_value REAL NOT NULL,
    decision_support REAL NOT NULL,
    governance_quality REAL NOT NULL,
    equity_safeguards REAL NOT NULL,
    human_oversight REAL NOT NULL,
    local_knowledge REAL NOT NULL,
    security_resilience REAL NOT NULL,
    ai_risk REAL NOT NULL,
    implementation_burden REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ai_enabled_resilience_systems (
    system_id TEXT PRIMARY KEY,
    system TEXT NOT NULL,
    system_context TEXT NOT NULL,
    initial_function REAL NOT NULL,
    baseline_resilience REAL NOT NULL,
    ai_monitoring REAL NOT NULL,
    ai_forecasting REAL NOT NULL,
    scenario_capacity REAL NOT NULL,
    decision_support REAL NOT NULL,
    governance REAL NOT NULL,
    equity_safeguards REAL NOT NULL,
    human_oversight REAL NOT NULL,
    local_knowledge REAL NOT NULL,
    security_resilience REAL NOT NULL,
    initial_ai_risk REAL NOT NULL,
    initial_model_drift REAL NOT NULL,
    initial_human_strain REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ai_resilience_disruption_events (
    event_id TEXT PRIMARY KEY,
    event_name TEXT NOT NULL,
    primary_stress TEXT NOT NULL,
    shock_intensity REAL NOT NULL,
    climate_infrastructure_stress REAL NOT NULL,
    data_shift_stress REAL NOT NULL,
    public_trust_stress REAL NOT NULL,
    cyber_adversarial_stress REAL NOT NULL,
    resource_constraint_stress REAL NOT NULL,
    institutional_learning_stress REAL NOT NULL,
    equity_pressure REAL NOT NULL,
    model_drift_pressure REAL NOT NULL,
    affected_functions TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ai_resilience_scenarios (
    scenario TEXT PRIMARY KEY,
    monitoring_value_weight REAL NOT NULL,
    forecasting_value_weight REAL NOT NULL,
    scenario_value_weight REAL NOT NULL,
    decision_support_weight REAL NOT NULL,
    governance_quality_weight REAL NOT NULL,
    equity_safeguards_weight REAL NOT NULL,
    human_oversight_weight REAL NOT NULL,
    local_knowledge_weight REAL NOT NULL,
    security_resilience_weight REAL NOT NULL,
    ai_risk_weight REAL NOT NULL,
    implementation_burden_weight REAL NOT NULL,
    description TEXT
);

CREATE VIEW IF NOT EXISTS ai_resilience_value_view AS
SELECT
    strategy_id,
    strategy,
    system_domain,
    critical_function,
    monitoring_value,
    forecasting_value,
    scenario_value,
    decision_support,
    governance_quality,
    equity_safeguards,
    human_oversight,
    local_knowledge,
    security_resilience,
    ai_risk,
    implementation_burden,
    (
        0.11 * monitoring_value +
        0.10 * forecasting_value +
        0.11 * scenario_value +
        0.11 * decision_support +
        0.12 * governance_quality +
        0.12 * equity_safeguards +
        0.12 * human_oversight +
        0.10 * local_knowledge +
        0.10 * security_resilience -
        0.05 * ai_risk -
        0.04 * implementation_burden
    ) AS ai_resilience_value
FROM ai_resilience_strategies;
