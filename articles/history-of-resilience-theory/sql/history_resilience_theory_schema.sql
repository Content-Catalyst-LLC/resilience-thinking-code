-- History of Resilience Theory schema
-- Supports historical phases, concepts, sources, model runs, and outputs.

CREATE TABLE IF NOT EXISTS historical_phases (
    phase_id TEXT PRIMARY KEY,
    period TEXT NOT NULL,
    start_year INTEGER NOT NULL,
    domain TEXT NOT NULL,
    conceptual_scope REAL NOT NULL CHECK (conceptual_scope BETWEEN 0 AND 1),
    governance_relevance REAL NOT NULL CHECK (governance_relevance BETWEEN 0 AND 1),
    system_complexity REAL NOT NULL CHECK (system_complexity BETWEEN 0 AND 1),
    justice_relevance REAL NOT NULL CHECK (justice_relevance BETWEEN 0 AND 1),
    core_contribution TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS resilience_concepts (
    concept_id TEXT PRIMARY KEY,
    concept TEXT NOT NULL,
    associated_phase TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS source_notes (
    source_id TEXT PRIMARY KEY,
    author_year TEXT NOT NULL,
    source_title TEXT NOT NULL,
    concept_area TEXT NOT NULL,
    note TEXT
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

CREATE VIEW IF NOT EXISTS historical_phase_influence_view AS
SELECT
    phase_id,
    period,
    start_year,
    domain,
    conceptual_scope,
    governance_relevance,
    system_complexity,
    justice_relevance,
    (
        0.35 * conceptual_scope +
        0.25 * governance_relevance +
        0.25 * system_complexity +
        0.15 * justice_relevance
    ) AS influence_score,
    core_contribution
FROM historical_phases;
