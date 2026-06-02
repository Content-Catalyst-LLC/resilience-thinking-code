-- Local Knowledge and Resilience Practice schema.

CREATE TABLE IF NOT EXISTS local_knowledge_strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    participation_access REAL NOT NULL,
    knowledge_diversity REAL NOT NULL,
    decision_influence REAL NOT NULL,
    trust_building REAL NOT NULL,
    knowledge_protection REAL NOT NULL,
    reciprocity REAL NOT NULL,
    implementation_accountability REAL NOT NULL,
    implementation_burden REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS knowledge_systems (
    system_id TEXT PRIMARY KEY,
    system TEXT NOT NULL,
    knowledge_context TEXT NOT NULL,
    baseline_knowledge_function REAL NOT NULL,
    institutional_trust REAL NOT NULL,
    participation_capacity REAL NOT NULL,
    knowledge_diversity REAL NOT NULL,
    decision_access REAL NOT NULL,
    privacy_risk REAL NOT NULL,
    community_control REAL NOT NULL,
    institutional_followthrough REAL NOT NULL,
    equity_sensitivity REAL NOT NULL,
    extraction_risk REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS knowledge_stress_events (
    event_id TEXT PRIMARY KEY,
    event_name TEXT NOT NULL,
    primary_stress TEXT NOT NULL,
    shock_intensity REAL NOT NULL,
    participation_burden REAL NOT NULL,
    trust_pressure REAL NOT NULL,
    information_stress REAL NOT NULL,
    privacy_exposure REAL NOT NULL,
    decision_delay REAL NOT NULL,
    reciprocity_gap REAL NOT NULL,
    accountability_gap REAL NOT NULL,
    extraction_pressure REAL NOT NULL,
    affected_functions TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS local_knowledge_scenarios (
    scenario TEXT PRIMARY KEY,
    participation_access_weight REAL NOT NULL,
    knowledge_diversity_weight REAL NOT NULL,
    decision_influence_weight REAL NOT NULL,
    trust_building_weight REAL NOT NULL,
    knowledge_protection_weight REAL NOT NULL,
    reciprocity_weight REAL NOT NULL,
    implementation_accountability_weight REAL NOT NULL,
    implementation_burden_weight REAL NOT NULL,
    description TEXT
);

CREATE VIEW IF NOT EXISTS local_knowledge_value_view AS
SELECT
    strategy_id,
    strategy,
    system_domain,
    critical_function,
    participation_access,
    knowledge_diversity,
    decision_influence,
    trust_building,
    knowledge_protection,
    reciprocity,
    implementation_accountability,
    implementation_burden,
    (
        0.14 * participation_access +
        0.14 * knowledge_diversity +
        0.15 * decision_influence +
        0.14 * trust_building +
        0.14 * knowledge_protection +
        0.14 * reciprocity +
        0.15 * implementation_accountability -
        0.02 * implementation_burden
    ) AS knowledge_integration_value,
    CASE
        WHEN decision_influence > implementation_accountability
        THEN decision_influence - implementation_accountability
        ELSE 0
    END AS extraction_risk_gap
FROM local_knowledge_strategies;
