-- Resilience Thinking companion schema
-- Synthetic schema for indicators, disturbances, scenarios, and model runs.

CREATE TABLE IF NOT EXISTS systems (
    system_id TEXT PRIMARY KEY,
    system_type TEXT NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS resilience_indicators (
    indicator_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL REFERENCES systems(system_id),
    adaptive_capacity REAL NOT NULL CHECK (adaptive_capacity BETWEEN 0 AND 1),
    threshold_distance REAL NOT NULL CHECK (threshold_distance BETWEEN 0 AND 1),
    learning_capacity REAL NOT NULL CHECK (learning_capacity BETWEEN 0 AND 1),
    modularity REAL NOT NULL CHECK (modularity BETWEEN 0 AND 1),
    redundancy REAL NOT NULL CHECK (redundancy BETWEEN 0 AND 1),
    exposure REAL NOT NULL CHECK (exposure BETWEEN 0 AND 1),
    sensitivity REAL NOT NULL CHECK (sensitivity BETWEEN 0 AND 1),
    measurement_note TEXT
);

CREATE TABLE IF NOT EXISTS disturbance_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    baseline_disturbance REAL NOT NULL,
    shock_intensity REAL NOT NULL,
    shock_frequency INTEGER NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS model_runs (
    run_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL REFERENCES systems(system_id),
    scenario_id TEXT NOT NULL REFERENCES disturbance_scenarios(scenario_id),
    run_label TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS model_run_results (
    result_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL REFERENCES model_runs(run_id),
    time_step INTEGER NOT NULL,
    disturbance REAL NOT NULL,
    viability REAL NOT NULL,
    viability_margin REAL NOT NULL,
    threshold_flag TEXT NOT NULL
);

CREATE VIEW IF NOT EXISTS resilience_profile_view AS
SELECT
    s.system_id,
    s.system_type,
    s.critical_function,
    i.adaptive_capacity,
    i.threshold_distance,
    i.learning_capacity,
    i.modularity,
    i.redundancy,
    i.exposure,
    i.sensitivity,
    (
        0.24 * i.adaptive_capacity +
        0.20 * i.threshold_distance +
        0.18 * i.learning_capacity +
        0.14 * i.modularity +
        0.14 * i.redundancy -
        0.05 * i.exposure -
        0.05 * i.sensitivity
    ) AS resilience_profile,
    (0.55 * i.exposure + 0.45 * i.sensitivity) AS risk_pressure
FROM systems s
JOIN resilience_indicators i ON s.system_id = i.system_id;
