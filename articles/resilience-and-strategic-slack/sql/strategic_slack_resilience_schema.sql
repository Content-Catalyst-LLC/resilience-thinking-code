-- Strategic Slack and Resilience schema.

CREATE TABLE IF NOT EXISTS strategic_slack_portfolios (
    portfolio_id TEXT PRIMARY KEY,
    portfolio TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    financial_slack REAL NOT NULL,
    workforce_slack REAL NOT NULL,
    operational_slack REAL NOT NULL,
    knowledge_slack REAL NOT NULL,
    network_slack REAL NOT NULL,
    governance_slack REAL NOT NULL,
    ethical_safeguards REAL NOT NULL,
    ethical_burden REAL NOT NULL,
    implementation_burden REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS slack_system_profiles (
    system_id TEXT PRIMARY KEY,
    system TEXT NOT NULL,
    system_context TEXT NOT NULL,
    initial_function REAL NOT NULL,
    financial_slack REAL NOT NULL,
    workforce_slack REAL NOT NULL,
    operational_slack REAL NOT NULL,
    knowledge_slack REAL NOT NULL,
    network_slack REAL NOT NULL,
    governance_slack REAL NOT NULL,
    ethical_safeguards REAL NOT NULL,
    initial_strain REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS slack_disruption_events (
    event_id TEXT PRIMARY KEY,
    event_name TEXT NOT NULL,
    primary_stress TEXT NOT NULL,
    shock_intensity REAL NOT NULL,
    financial_stress REAL NOT NULL,
    workforce_stress REAL NOT NULL,
    operational_stress REAL NOT NULL,
    knowledge_stress REAL NOT NULL,
    network_stress REAL NOT NULL,
    governance_stress REAL NOT NULL,
    ethical_burden REAL NOT NULL,
    slack_consumption_pressure REAL NOT NULL,
    affected_functions TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS strategic_slack_scenarios (
    scenario TEXT PRIMARY KEY,
    financial_slack_weight REAL NOT NULL,
    workforce_slack_weight REAL NOT NULL,
    operational_slack_weight REAL NOT NULL,
    knowledge_slack_weight REAL NOT NULL,
    network_slack_weight REAL NOT NULL,
    governance_slack_weight REAL NOT NULL,
    ethical_safeguards_weight REAL NOT NULL,
    ethical_burden_weight REAL NOT NULL,
    implementation_burden_weight REAL NOT NULL,
    description TEXT
);

CREATE VIEW IF NOT EXISTS strategic_slack_value_view AS
SELECT
    portfolio_id,
    portfolio,
    system_domain,
    critical_function,
    financial_slack,
    workforce_slack,
    operational_slack,
    knowledge_slack,
    network_slack,
    governance_slack,
    ethical_safeguards,
    ethical_burden,
    implementation_burden,
    (
        0.13 * financial_slack +
        0.14 * workforce_slack +
        0.13 * operational_slack +
        0.13 * knowledge_slack +
        0.13 * network_slack +
        0.14 * governance_slack +
        0.13 * ethical_safeguards -
        0.04 * ethical_burden -
        0.03 * implementation_burden
    ) AS slack_resilience_value
FROM strategic_slack_portfolios;
