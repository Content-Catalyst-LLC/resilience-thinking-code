-- Landscape Resilience and Disturbance Regimes schema
-- Supports landscapes, patches, disturbance regimes, refugia, connectivity, social vulnerability, scenarios, model runs, and outputs.

CREATE TABLE IF NOT EXISTS landscapes (
    landscape_id TEXT PRIMARY KEY,
    landscape_type TEXT NOT NULL,
    dominant_disturbance TEXT NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS landscape_profiles (
    profile_id TEXT PRIMARY KEY,
    landscape_id TEXT NOT NULL REFERENCES landscapes(landscape_id),
    spatial_heterogeneity REAL NOT NULL CHECK (spatial_heterogeneity BETWEEN 0 AND 1),
    viable_connectivity REAL NOT NULL CHECK (viable_connectivity BETWEEN 0 AND 1),
    refugia_capacity REAL NOT NULL CHECK (refugia_capacity BETWEEN 0 AND 1),
    ecological_memory REAL NOT NULL CHECK (ecological_memory BETWEEN 0 AND 1),
    disturbance_pressure REAL NOT NULL CHECK (disturbance_pressure BETWEEN 0 AND 1),
    fragmentation REAL NOT NULL CHECK (fragmentation BETWEEN 0 AND 1),
    governance_capacity REAL NOT NULL CHECK (governance_capacity BETWEEN 0 AND 1),
    social_vulnerability REAL NOT NULL CHECK (social_vulnerability BETWEEN 0 AND 1)
);

CREATE TABLE IF NOT EXISTS patches (
    patch_id TEXT PRIMARY KEY,
    landscape_id TEXT NOT NULL REFERENCES landscapes(landscape_id),
    patch_type TEXT NOT NULL,
    condition REAL NOT NULL CHECK (condition BETWEEN 0 AND 1),
    exposure REAL NOT NULL CHECK (exposure BETWEEN 0 AND 1),
    buffer_capacity REAL NOT NULL CHECK (buffer_capacity BETWEEN 0 AND 1),
    ecological_memory REAL NOT NULL CHECK (ecological_memory BETWEEN 0 AND 1),
    recovery_capacity REAL NOT NULL CHECK (recovery_capacity BETWEEN 0 AND 1),
    refugia INTEGER NOT NULL CHECK (refugia IN (0, 1)),
    connectivity_weight REAL NOT NULL CHECK (connectivity_weight BETWEEN 0 AND 1),
    social_exposure REAL NOT NULL CHECK (social_exposure BETWEEN 0 AND 1)
);

CREATE TABLE IF NOT EXISTS disturbance_regimes (
    regime_id TEXT PRIMARY KEY,
    landscape_id TEXT NOT NULL REFERENCES landscapes(landscape_id),
    disturbance_type TEXT NOT NULL,
    frequency_score REAL CHECK (frequency_score BETWEEN 0 AND 1),
    intensity_score REAL CHECK (intensity_score BETWEEN 0 AND 1),
    severity_score REAL CHECK (severity_score BETWEEN 0 AND 1),
    extent_score REAL CHECK (extent_score BETWEEN 0 AND 1),
    timing_sensitivity REAL CHECK (timing_sensitivity BETWEEN 0 AND 1)
);

CREATE TABLE IF NOT EXISTS scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    disturbance_load REAL NOT NULL CHECK (disturbance_load BETWEEN 0 AND 1),
    spread_amplifier REAL NOT NULL CHECK (spread_amplifier BETWEEN 0 AND 1),
    climate_pressure REAL NOT NULL CHECK (climate_pressure BETWEEN 0 AND 1),
    governance_response REAL NOT NULL CHECK (governance_response BETWEEN 0 AND 1),
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

CREATE VIEW IF NOT EXISTS landscape_resilience_profile_view AS
SELECT
    l.landscape_id,
    l.landscape_type,
    l.dominant_disturbance,
    l.critical_function,
    lp.spatial_heterogeneity,
    lp.viable_connectivity,
    lp.refugia_capacity,
    lp.ecological_memory,
    lp.disturbance_pressure,
    lp.fragmentation,
    lp.governance_capacity,
    lp.social_vulnerability,
    (
        0.17 * lp.spatial_heterogeneity +
        0.15 * lp.viable_connectivity +
        0.17 * lp.refugia_capacity +
        0.17 * lp.ecological_memory +
        0.14 * lp.governance_capacity -
        0.11 * lp.disturbance_pressure -
        0.06 * lp.fragmentation -
        0.06 * lp.social_vulnerability
    ) AS landscape_resilience_profile,
    (
        0.28 * lp.disturbance_pressure +
        0.20 * lp.fragmentation +
        0.18 * lp.social_vulnerability +
        0.14 * (1 - lp.refugia_capacity) +
        0.10 * (1 - lp.ecological_memory) +
        0.10 * (1 - lp.governance_capacity)
    ) AS disturbance_risk_index
FROM landscapes l
JOIN landscape_profiles lp ON l.landscape_id = lp.landscape_id;
