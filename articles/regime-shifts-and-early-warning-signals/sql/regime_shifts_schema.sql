-- Regime Shifts and Early Warning Signals schema
-- Supports systems, regimes, thresholds, warning signals, scenarios, model runs, and outputs.

CREATE TABLE IF NOT EXISTS systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_type TEXT NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS regime_profiles (
    profile_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL REFERENCES systems(system_id),
    pressure REAL NOT NULL CHECK (pressure BETWEEN 0 AND 1),
    feedback_strength REAL NOT NULL CHECK (feedback_strength BETWEEN 0 AND 1),
    variance_signal REAL NOT NULL CHECK (variance_signal BETWEEN 0 AND 1),
    autocorr_signal REAL NOT NULL CHECK (autocorr_signal BETWEEN 0 AND 1),
    recovery_speed REAL NOT NULL CHECK (recovery_speed BETWEEN 0 AND 1),
    adaptive_capacity REAL NOT NULL CHECK (adaptive_capacity BETWEEN 0 AND 1),
    system_memory REAL NOT NULL CHECK (system_memory BETWEEN 0 AND 1),
    monitoring_quality REAL NOT NULL CHECK (monitoring_quality BETWEEN 0 AND 1),
    justice_visibility REAL NOT NULL CHECK (justice_visibility BETWEEN 0 AND 1),
    exposure REAL NOT NULL CHECK (exposure BETWEEN 0 AND 1)
);

CREATE TABLE IF NOT EXISTS regimes (
    regime_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL REFERENCES systems(system_id),
    regime_name TEXT NOT NULL,
    regime_description TEXT,
    desirable BOOLEAN
);

CREATE TABLE IF NOT EXISTS warning_signals (
    signal_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL REFERENCES systems(system_id),
    time_step INTEGER NOT NULL,
    system_state REAL,
    rolling_variance REAL,
    rolling_autocorr REAL,
    recovery_speed_proxy REAL,
    threshold_proximity_score REAL,
    interpretation_note TEXT
);

CREATE TABLE IF NOT EXISTS regime_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    pressure_start REAL NOT NULL,
    pressure_end REAL NOT NULL,
    steps INTEGER NOT NULL,
    noise_level REAL NOT NULL,
    recovery_coefficient REAL NOT NULL,
    adaptive_intervention REAL NOT NULL,
    monitoring_quality REAL NOT NULL,
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

CREATE VIEW IF NOT EXISTS regime_risk_profile_view AS
SELECT
    s.system_id,
    s.system_name,
    s.system_type,
    s.critical_function,
    rp.pressure,
    rp.feedback_strength,
    rp.variance_signal,
    rp.autocorr_signal,
    rp.recovery_speed,
    rp.adaptive_capacity,
    rp.system_memory,
    rp.monitoring_quality,
    rp.justice_visibility,
    rp.exposure,
    (
        0.18 * rp.pressure +
        0.17 * rp.feedback_strength +
        0.15 * rp.variance_signal +
        0.15 * rp.autocorr_signal +
        0.12 * rp.exposure -
        0.08 * rp.recovery_speed -
        0.06 * rp.adaptive_capacity -
        0.04 * rp.system_memory -
        0.03 * rp.monitoring_quality -
        0.02 * rp.justice_visibility
    ) AS regime_risk_score,
    (
        0.22 * rp.recovery_speed +
        0.20 * rp.adaptive_capacity +
        0.18 * rp.system_memory +
        0.16 * rp.monitoring_quality +
        0.12 * rp.justice_visibility +
        0.12 * (1 - rp.feedback_strength)
    ) AS threshold_protection_score
FROM systems s
JOIN regime_profiles rp ON s.system_id = rp.system_id;
