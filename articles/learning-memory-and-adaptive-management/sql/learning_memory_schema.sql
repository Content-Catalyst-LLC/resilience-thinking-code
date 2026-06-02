-- Learning, Memory, and Adaptive Management schema
-- Supports strategies, memory assets, learning events, adaptive decisions,
-- scenarios, model runs, and outputs.

CREATE TABLE IF NOT EXISTS adaptive_management_strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    monitoring_quality REAL NOT NULL,
    memory_retention REAL NOT NULL,
    feedback_use REAL NOT NULL,
    governance_flexibility REAL NOT NULL,
    community_knowledge REAL NOT NULL,
    justice_protection REAL NOT NULL,
    implementation_reliability REAL NOT NULL,
    forgetting_pressure REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS memory_assets (
    memory_asset_id TEXT PRIMARY KEY,
    asset_name TEXT NOT NULL,
    memory_type TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    retention_quality REAL NOT NULL,
    loss_risk REAL NOT NULL,
    stewardship_note TEXT
);

CREATE TABLE IF NOT EXISTS learning_events (
    event_id TEXT PRIMARY KEY,
    event_name TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    disturbance_intensity REAL NOT NULL,
    monitoring_signal REAL NOT NULL,
    lesson_capture REAL NOT NULL,
    implementation_followthrough REAL NOT NULL,
    community_input REAL NOT NULL,
    justice_visibility REAL NOT NULL,
    memory_loss_risk REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS adaptive_decisions (
    decision_id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL REFERENCES learning_events(event_id),
    decision_name TEXT NOT NULL,
    decision_trigger TEXT NOT NULL,
    implementation_status TEXT NOT NULL,
    accountable_actor TEXT
);

CREATE TABLE IF NOT EXISTS adaptive_management_scenarios (
    scenario TEXT PRIMARY KEY,
    monitoring_quality_weight REAL NOT NULL,
    memory_retention_weight REAL NOT NULL,
    feedback_use_weight REAL NOT NULL,
    governance_flexibility_weight REAL NOT NULL,
    community_knowledge_weight REAL NOT NULL,
    justice_protection_weight REAL NOT NULL,
    implementation_reliability_weight REAL NOT NULL,
    forgetting_pressure_weight REAL NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS model_runs (
    run_id TEXT PRIMARY KEY,
    model_name TEXT NOT NULL,
    model_purpose TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS model_outputs (
    output_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL REFERENCES model_runs(run_id),
    output_name TEXT NOT NULL,
    output_path TEXT NOT NULL,
    interpretation_note TEXT
);

CREATE VIEW IF NOT EXISTS base_adaptive_learning_value_view AS
SELECT
    strategy_id,
    strategy,
    system_domain,
    critical_function,
    monitoring_quality,
    memory_retention,
    feedback_use,
    governance_flexibility,
    community_knowledge,
    justice_protection,
    implementation_reliability,
    forgetting_pressure,
    (
        0.15 * monitoring_quality +
        0.15 * memory_retention +
        0.17 * feedback_use +
        0.14 * governance_flexibility +
        0.12 * community_knowledge +
        0.11 * justice_protection +
        0.09 * implementation_reliability -
        0.07 * forgetting_pressure
    ) AS base_adaptive_learning_value
FROM adaptive_management_strategies;

CREATE VIEW IF NOT EXISTS learning_event_diagnostic_view AS
SELECT
    event_id,
    event_name,
    system_domain,
    disturbance_intensity,
    (
        0.20 * monitoring_signal +
        0.22 * lesson_capture +
        0.20 * implementation_followthrough +
        0.18 * community_input +
        0.14 * justice_visibility -
        0.06 * memory_loss_risk
    ) AS lesson_score
FROM learning_events;
