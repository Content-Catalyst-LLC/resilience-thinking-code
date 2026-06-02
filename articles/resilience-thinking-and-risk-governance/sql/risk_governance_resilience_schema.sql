-- Resilience Thinking and Risk Governance schema
-- Supports hazards, exposure, vulnerability, capacity, governance indicators, scenarios, model runs, and outputs.

CREATE TABLE IF NOT EXISTS systems (
    system_id TEXT PRIMARY KEY,
    system_type TEXT NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS risk_profile_indicators (
    risk_profile_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL REFERENCES systems(system_id),
    hazard_intensity REAL NOT NULL CHECK (hazard_intensity BETWEEN 0 AND 1),
    exposure REAL NOT NULL CHECK (exposure BETWEEN 0 AND 1),
    vulnerability REAL NOT NULL CHECK (vulnerability BETWEEN 0 AND 1),
    buffer_capacity REAL NOT NULL CHECK (buffer_capacity BETWEEN 0 AND 1),
    adaptive_capacity REAL NOT NULL CHECK (adaptive_capacity BETWEEN 0 AND 1),
    learning_capacity REAL NOT NULL CHECK (learning_capacity BETWEEN 0 AND 1)
);

CREATE TABLE IF NOT EXISTS governance_indicators (
    governance_indicator_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL REFERENCES systems(system_id),
    trust REAL NOT NULL CHECK (trust BETWEEN 0 AND 1),
    participation_quality REAL NOT NULL CHECK (participation_quality BETWEEN 0 AND 1),
    knowledge_integration REAL NOT NULL CHECK (knowledge_integration BETWEEN 0 AND 1),
    coordination_quality REAL NOT NULL CHECK (coordination_quality BETWEEN 0 AND 1),
    transparency REAL NOT NULL CHECK (transparency BETWEEN 0 AND 1),
    accountability REAL NOT NULL CHECK (accountability BETWEEN 0 AND 1)
);

CREATE TABLE IF NOT EXISTS disturbance_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    disturbance_load REAL NOT NULL CHECK (disturbance_load BETWEEN 0 AND 1),
    shock_intensity REAL NOT NULL CHECK (shock_intensity BETWEEN 0 AND 1),
    shock_frequency INTEGER NOT NULL,
    governance_stress REAL NOT NULL CHECK (governance_stress BETWEEN 0 AND 1),
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

CREATE VIEW IF NOT EXISTS risk_governance_resilience_view AS
SELECT
    s.system_id,
    s.system_type,
    s.critical_function,
    (
        r.hazard_intensity * r.exposure * r.vulnerability * (1 - 0.55 * r.adaptive_capacity)
    ) AS risk_pressure,
    (
        0.18 * g.trust +
        0.17 * g.participation_quality +
        0.17 * g.knowledge_integration +
        0.18 * g.coordination_quality +
        0.15 * g.transparency +
        0.15 * g.accountability
    ) AS governance_capacity,
    (
        r.buffer_capacity +
        r.adaptive_capacity +
        r.learning_capacity +
        (
            0.18 * g.trust +
            0.17 * g.participation_quality +
            0.17 * g.knowledge_integration +
            0.18 * g.coordination_quality +
            0.15 * g.transparency +
            0.15 * g.accountability
        ) -
        (
            r.hazard_intensity * r.exposure * r.vulnerability * (1 - 0.55 * r.adaptive_capacity)
        ) -
        r.vulnerability
    ) AS resilience_margin
FROM systems s
JOIN risk_profile_indicators r ON s.system_id = r.system_id
JOIN governance_indicators g ON s.system_id = g.system_id;
