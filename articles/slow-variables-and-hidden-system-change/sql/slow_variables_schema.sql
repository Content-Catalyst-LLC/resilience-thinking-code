-- Slow Variables and Hidden System Change schema
-- Supports systems, slow variables, monitoring indicators, thresholds, scenarios, model runs, and outputs.

CREATE TABLE IF NOT EXISTS systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_type TEXT NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS slow_variable_profiles (
    profile_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL REFERENCES systems(system_id),
    maintenance_backlog REAL NOT NULL CHECK (maintenance_backlog BETWEEN 0 AND 1),
    public_trust REAL NOT NULL CHECK (public_trust BETWEEN 0 AND 1),
    ecological_memory REAL NOT NULL CHECK (ecological_memory BETWEEN 0 AND 1),
    climate_pressure REAL NOT NULL CHECK (climate_pressure BETWEEN 0 AND 1),
    adaptive_capacity REAL NOT NULL CHECK (adaptive_capacity BETWEEN 0 AND 1),
    system_memory REAL NOT NULL CHECK (system_memory BETWEEN 0 AND 1),
    monitoring_quality REAL NOT NULL CHECK (monitoring_quality BETWEEN 0 AND 1),
    justice_visibility REAL NOT NULL CHECK (justice_visibility BETWEEN 0 AND 1),
    exposure REAL NOT NULL CHECK (exposure BETWEEN 0 AND 1)
);

CREATE TABLE IF NOT EXISTS monitoring_indicators (
    indicator_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL REFERENCES systems(system_id),
    indicator_name TEXT NOT NULL,
    indicator_value REAL,
    measurement_date TEXT,
    measurement_note TEXT
);

CREATE TABLE IF NOT EXISTS slow_variable_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    maintenance_growth REAL NOT NULL,
    trust_decline REAL NOT NULL,
    memory_decline REAL NOT NULL,
    climate_growth REAL NOT NULL,
    adaptive_investment REAL NOT NULL,
    monitoring_improvement REAL NOT NULL,
    justice_improvement REAL NOT NULL,
    shock_time_1 INTEGER NOT NULL,
    shock_time_2 INTEGER NOT NULL,
    shock_magnitude REAL NOT NULL,
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

CREATE VIEW IF NOT EXISTS hidden_risk_profile_view AS
SELECT
    s.system_id,
    s.system_name,
    s.system_type,
    s.critical_function,
    svp.maintenance_backlog,
    svp.public_trust,
    svp.ecological_memory,
    svp.climate_pressure,
    svp.adaptive_capacity,
    svp.system_memory,
    svp.monitoring_quality,
    svp.justice_visibility,
    svp.exposure,
    (
        0.20 * svp.maintenance_backlog +
        0.18 * svp.climate_pressure +
        0.16 * svp.exposure +
        0.12 * (1 - svp.public_trust) +
        0.12 * (1 - svp.ecological_memory) +
        0.10 * (1 - svp.adaptive_capacity) +
        0.07 * (1 - svp.monitoring_quality) +
        0.05 * (1 - svp.justice_visibility)
    ) AS hidden_risk_score,
    (
        1 -
        0.26 * svp.maintenance_backlog -
        0.24 * svp.climate_pressure -
        0.16 * svp.exposure -
        0.12 * (1 - svp.public_trust) -
        0.12 * (1 - svp.ecological_memory) -
        0.10 * (1 - svp.adaptive_capacity)
    ) AS threshold_distance
FROM systems s
JOIN slow_variable_profiles svp ON s.system_id = svp.system_id;
