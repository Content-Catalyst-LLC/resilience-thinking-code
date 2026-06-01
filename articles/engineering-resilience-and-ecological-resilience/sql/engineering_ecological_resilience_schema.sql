-- Engineering Resilience and Ecological Resilience schema
-- Supports systems, disturbances, recovery metrics, threshold metrics, scenarios, model runs, and outputs.

CREATE TABLE IF NOT EXISTS systems (
    system_id TEXT PRIMARY KEY,
    system_type TEXT NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS engineering_metrics (
    engineering_metric_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL REFERENCES systems(system_id),
    return_speed REAL NOT NULL CHECK (return_speed BETWEEN 0 AND 1),
    reliability REAL NOT NULL CHECK (reliability BETWEEN 0 AND 1),
    repair_capacity REAL NOT NULL CHECK (repair_capacity BETWEEN 0 AND 1),
    backup_capacity REAL NOT NULL CHECK (backup_capacity BETWEEN 0 AND 1),
    service_continuity REAL NOT NULL CHECK (service_continuity BETWEEN 0 AND 1)
);

CREATE TABLE IF NOT EXISTS ecological_metrics (
    ecological_metric_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL REFERENCES systems(system_id),
    threshold_distance REAL NOT NULL CHECK (threshold_distance BETWEEN 0 AND 1),
    basin_width REAL NOT NULL CHECK (basin_width BETWEEN 0 AND 1),
    adaptive_capacity REAL NOT NULL CHECK (adaptive_capacity BETWEEN 0 AND 1),
    functional_diversity REAL NOT NULL CHECK (functional_diversity BETWEEN 0 AND 1),
    redundancy REAL NOT NULL CHECK (redundancy BETWEEN 0 AND 1),
    modularity REAL NOT NULL CHECK (modularity BETWEEN 0 AND 1),
    disturbance_exposure REAL NOT NULL CHECK (disturbance_exposure BETWEEN 0 AND 1),
    regime_shift_sensitivity REAL NOT NULL CHECK (regime_shift_sensitivity BETWEEN 0 AND 1)
);

CREATE TABLE IF NOT EXISTS disturbance_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    disturbance_load REAL NOT NULL,
    shock_intensity REAL NOT NULL,
    shock_duration INTEGER NOT NULL,
    compound_risk REAL NOT NULL,
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

CREATE VIEW IF NOT EXISTS engineering_ecological_profile_view AS
SELECT
    s.system_id,
    s.system_type,
    s.critical_function,
    (
        0.28 * em.return_speed +
        0.24 * em.reliability +
        0.18 * em.repair_capacity +
        0.15 * em.backup_capacity +
        0.15 * em.service_continuity
    ) AS engineering_resilience,
    (
        0.20 * eco.threshold_distance +
        0.18 * eco.basin_width +
        0.18 * eco.adaptive_capacity +
        0.15 * eco.functional_diversity +
        0.13 * eco.redundancy +
        0.10 * eco.modularity -
        0.08 * eco.disturbance_exposure -
        0.08 * eco.regime_shift_sensitivity
    ) AS ecological_resilience
FROM systems s
JOIN engineering_metrics em ON s.system_id = em.system_id
JOIN ecological_metrics eco ON s.system_id = eco.system_id;
