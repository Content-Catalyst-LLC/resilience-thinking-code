-- Predictive resilience model schema
-- Supports model inputs, feature sets, scenarios, predictions, metrics, and audit notes.

CREATE TABLE IF NOT EXISTS resilience_observations (
    observation_id INTEGER PRIMARY KEY,
    system_type TEXT NOT NULL,
    equilibrium_return REAL NOT NULL CHECK (equilibrium_return BETWEEN 0 AND 1),
    stress_tolerance REAL NOT NULL CHECK (stress_tolerance BETWEEN 0 AND 1),
    adaptive_capacity REAL NOT NULL CHECK (adaptive_capacity BETWEEN 0 AND 1),
    threshold_distance REAL NOT NULL CHECK (threshold_distance BETWEEN 0 AND 1),
    learning_capacity REAL NOT NULL CHECK (learning_capacity BETWEEN 0 AND 1),
    redundancy REAL NOT NULL CHECK (redundancy BETWEEN 0 AND 1),
    modularity REAL NOT NULL CHECK (modularity BETWEEN 0 AND 1),
    exposure REAL NOT NULL CHECK (exposure BETWEEN 0 AND 1),
    sensitivity REAL NOT NULL CHECK (sensitivity BETWEEN 0 AND 1),
    dependency_concentration REAL NOT NULL CHECK (dependency_concentration BETWEEN 0 AND 1),
    shock_intensity REAL NOT NULL CHECK (shock_intensity BETWEEN 0 AND 1),
    shock_frequency INTEGER NOT NULL,
    compound_disturbance_index REAL NOT NULL CHECK (compound_disturbance_index BETWEEN 0 AND 1),
    resilience_failure_risk INTEGER NOT NULL CHECK (resilience_failure_risk IN (0, 1))
);

CREATE TABLE IF NOT EXISTS predictive_model_runs (
    model_run_id TEXT PRIMARY KEY,
    model_name TEXT NOT NULL,
    model_version TEXT NOT NULL,
    training_data_note TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS model_metrics (
    model_run_id TEXT NOT NULL REFERENCES predictive_model_runs(model_run_id),
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    PRIMARY KEY (model_run_id, metric_name)
);

CREATE TABLE IF NOT EXISTS scenario_predictions (
    prediction_id TEXT PRIMARY KEY,
    model_run_id TEXT NOT NULL REFERENCES predictive_model_runs(model_run_id),
    scenario_name TEXT NOT NULL,
    predicted_failure_probability REAL NOT NULL CHECK (predicted_failure_probability BETWEEN 0 AND 1),
    prediction_band TEXT NOT NULL,
    interpretation_note TEXT
);

CREATE VIEW IF NOT EXISTS resilience_feature_view AS
SELECT
    observation_id,
    system_type,
    equilibrium_return AS stability_score,
    0.65 * stress_tolerance + 0.35 * equilibrium_return AS robustness_score,
    (
        0.22 * adaptive_capacity +
        0.20 * threshold_distance +
        0.18 * learning_capacity +
        0.20 * redundancy +
        0.20 * modularity
    ) AS resilience_score,
    (
        0.22 * exposure +
        0.20 * sensitivity +
        0.20 * dependency_concentration +
        0.22 * shock_intensity +
        0.16 * (shock_frequency / 12.0)
    ) AS risk_pressure,
    resilience_failure_risk
FROM resilience_observations;
