-- Social-Ecological Systems schema
-- Supports resource systems, resource units, governance systems, users, interactions, outcomes, scenarios, and model outputs.

CREATE TABLE IF NOT EXISTS resource_systems (
    resource_system_id TEXT PRIMARY KEY,
    system_type TEXT NOT NULL,
    ecological_condition REAL NOT NULL CHECK (ecological_condition BETWEEN 0 AND 1),
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS resource_units (
    resource_unit_id TEXT PRIMARY KEY,
    resource_system_id TEXT NOT NULL REFERENCES resource_systems(resource_system_id),
    unit_name TEXT NOT NULL,
    renewal_rate REAL,
    extraction_sensitivity REAL
);

CREATE TABLE IF NOT EXISTS governance_systems (
    governance_system_id TEXT PRIMARY KEY,
    resource_system_id TEXT NOT NULL REFERENCES resource_systems(resource_system_id),
    governance_quality REAL NOT NULL CHECK (governance_quality BETWEEN 0 AND 1),
    monitoring_capacity REAL CHECK (monitoring_capacity BETWEEN 0 AND 1),
    participation_quality REAL CHECK (participation_quality BETWEEN 0 AND 1),
    accountability REAL CHECK (accountability BETWEEN 0 AND 1)
);

CREATE TABLE IF NOT EXISTS user_groups (
    user_group_id TEXT PRIMARY KEY,
    resource_system_id TEXT NOT NULL REFERENCES resource_systems(resource_system_id),
    group_name TEXT NOT NULL,
    livelihood_diversity REAL CHECK (livelihood_diversity BETWEEN 0 AND 1),
    resource_dependency REAL CHECK (resource_dependency BETWEEN 0 AND 1),
    social_trust REAL CHECK (social_trust BETWEEN 0 AND 1)
);

CREATE TABLE IF NOT EXISTS ses_profiles (
    profile_id TEXT PRIMARY KEY,
    resource_system_id TEXT NOT NULL REFERENCES resource_systems(resource_system_id),
    infrastructure_support REAL NOT NULL CHECK (infrastructure_support BETWEEN 0 AND 1),
    knowledge_integration REAL NOT NULL CHECK (knowledge_integration BETWEEN 0 AND 1),
    market_pressure REAL NOT NULL CHECK (market_pressure BETWEEN 0 AND 1),
    climate_exposure REAL NOT NULL CHECK (climate_exposure BETWEEN 0 AND 1),
    adaptive_capacity REAL NOT NULL CHECK (adaptive_capacity BETWEEN 0 AND 1)
);

CREATE TABLE IF NOT EXISTS interactions (
    interaction_id TEXT PRIMARY KEY,
    resource_system_id TEXT NOT NULL REFERENCES resource_systems(resource_system_id),
    interaction_type TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS outcomes (
    outcome_id TEXT PRIMARY KEY,
    resource_system_id TEXT NOT NULL REFERENCES resource_systems(resource_system_id),
    ecological_outcome TEXT,
    social_outcome TEXT,
    governance_outcome TEXT,
    equity_note TEXT
);

CREATE TABLE IF NOT EXISTS coupled_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    initial_ecology REAL NOT NULL CHECK (initial_ecology BETWEEN 0 AND 1.2),
    initial_social_pressure REAL NOT NULL CHECK (initial_social_pressure BETWEEN 0 AND 1.2),
    governance_effectiveness REAL NOT NULL CHECK (governance_effectiveness BETWEEN 0 AND 1),
    livelihood_pressure REAL NOT NULL CHECK (livelihood_pressure BETWEEN 0 AND 1),
    climate_pressure REAL NOT NULL CHECK (climate_pressure BETWEEN 0 AND 1),
    market_shock REAL NOT NULL CHECK (market_shock BETWEEN 0 AND 1),
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

CREATE VIEW IF NOT EXISTS ses_resilience_profile_view AS
SELECT
    rs.resource_system_id,
    rs.system_type,
    rs.critical_function,
    rs.ecological_condition,
    gs.governance_quality,
    ug.livelihood_diversity,
    sp.infrastructure_support,
    sp.knowledge_integration,
    ug.social_trust,
    sp.market_pressure,
    sp.climate_exposure,
    sp.adaptive_capacity,
    ug.resource_dependency,
    (
        0.18 * rs.ecological_condition +
        0.16 * gs.governance_quality +
        0.12 * ug.livelihood_diversity +
        0.12 * sp.infrastructure_support +
        0.13 * sp.knowledge_integration +
        0.11 * ug.social_trust +
        0.10 * sp.adaptive_capacity -
        0.09 * sp.market_pressure -
        0.07 * sp.climate_exposure -
        0.02 * ug.resource_dependency
    ) AS ses_resilience_profile
FROM resource_systems rs
JOIN governance_systems gs ON rs.resource_system_id = gs.resource_system_id
JOIN user_groups ug ON rs.resource_system_id = ug.resource_system_id
JOIN ses_profiles sp ON rs.resource_system_id = sp.resource_system_id;
