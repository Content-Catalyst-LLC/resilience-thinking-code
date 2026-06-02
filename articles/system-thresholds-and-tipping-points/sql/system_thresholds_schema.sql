-- System Thresholds and Tipping Points schema
-- Supports systems, thresholds, pressures, regime states, warning signals, scenarios, model runs, and outputs.

CREATE TABLE IF NOT EXISTS systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_type TEXT NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS threshold_profiles (
    profile_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL REFERENCES systems(system_id),
    pressure REAL NOT NULL CHECK (pressure BETWEEN 0 AND 1),
    feedback_strength REAL NOT NULL CHECK (feedback_strength BETWEEN 0 AND 1),
    disturbance_load REAL NOT NULL CHECK (disturbance_load BETWEEN 0 AND 1),
    adaptive_capacity REAL NOT NULL CHECK (adaptive_capacity BETWEEN 0 AND 1),
    system_memory REAL NOT NULL CHECK (system_memory BETWEEN 0 AND 1),
    recovery_speed REAL NOT NULL CHECK (recovery_speed BETWEEN 0 AND 1),
    exposure REAL NOT NULL CHECK (exposure BETWEEN 0 AND 1)
);

CREATE TABLE IF NOT EXISTS regime_states (
    state_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL REFERENCES systems(system_id),
    regime_name TEXT NOT NULL,
    state_value REAL NOT NULL,
    pressure_value REAL NOT NULL,
    observed_at TEXT
);

CREATE TABLE IF NOT EXISTS warning_signals (
    signal_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL REFERENCES systems(system_id),
    time_step INTEGER NOT NULL,
    rolling_variance REAL,
    rolling_autocorr REAL,
    recovery_speed_proxy REAL,
    threshold_proximity_score REAL,
    interpretation_note TEXT
);

CREATE TABLE IF NOT EXISTS threshold_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    pressure_start REAL NOT NULL,
    pressure_end REAL NOT NULL,
    steps INTEGER NOT NULL,
    noise_level REAL NOT NULL,
    recovery_coefficient REAL NOT NULL,
    adaptive_capacity_gain REAL NOT NULL,
    feedback_growth REAL NOT NULL,
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

CREATE VIEW IF NOT EXISTS threshold_risk_profile_view AS
SELECT
    s.system_id,
    s.system_name,
    s.system_type,
    s.critical_function,
    tp.pressure,
    tp.feedback_strength,
    tp.disturbance_load,
    tp.adaptive_capacity,
    tp.system_memory,
    tp.recovery_speed,
    tp.exposure,
    (
        0.24 * tp.pressure +
        0.22 * tp.feedback_strength +
        0.18 * tp.disturbance_load +
        0.14 * tp.exposure -
        0.10 * tp.adaptive_capacity -
        0.07 * tp.system_memory -
        0.05 * tp.recovery_speed
    ) AS threshold_risk_score,
    (
        0.30 * tp.adaptive_capacity +
        0.24 * tp.system_memory +
        0.22 * tp.recovery_speed +
        0.14 * (1 - tp.feedback_strength) +
        0.10 * (1 - tp.pressure)
    ) AS threshold_protection_score
FROM systems s
JOIN threshold_profiles tp ON s.system_id = tp.system_id;
