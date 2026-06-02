-- Resilience Metrics and Measurement schema
-- Supports systems, indicators, disturbance events, recovery performance,
-- threshold signals, scenarios, model runs, and outputs.

CREATE TABLE IF NOT EXISTS systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_type TEXT NOT NULL,
    scale_of_analysis TEXT NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS resilience_indicators (
    indicator_id TEXT PRIMARY KEY,
    indicator TEXT NOT NULL,
    domain TEXT NOT NULL,
    definition TEXT NOT NULL,
    measurement_note TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS measurement_frameworks (
    framework_id TEXT PRIMARY KEY,
    framework TEXT NOT NULL,
    framework_type TEXT NOT NULL,
    resistance_coverage REAL NOT NULL,
    recovery_insight REAL NOT NULL,
    adaptive_capacity_visibility REAL NOT NULL,
    buffer_visibility REAL NOT NULL,
    justice_visibility REAL NOT NULL,
    data_quality_transparency REAL NOT NULL,
    threshold_blindness REAL NOT NULL,
    critical_use TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS disturbance_events (
    event_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL REFERENCES systems(system_id),
    disturbance_type TEXT NOT NULL,
    shock_intensity REAL NOT NULL,
    baseline_function REAL NOT NULL,
    min_function REAL NOT NULL,
    recovered_function REAL NOT NULL,
    recovery_days REAL NOT NULL,
    affected_population_share REAL,
    justice_visibility REAL
);

CREATE TABLE IF NOT EXISTS threshold_signals (
    signal_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL REFERENCES systems(system_id),
    signal_type TEXT NOT NULL,
    signal_value REAL NOT NULL,
    interpretation_note TEXT
);

CREATE TABLE IF NOT EXISTS measurement_scenarios (
    scenario TEXT PRIMARY KEY,
    resistance_coverage_weight REAL NOT NULL,
    recovery_insight_weight REAL NOT NULL,
    adaptive_capacity_visibility_weight REAL NOT NULL,
    buffer_visibility_weight REAL NOT NULL,
    justice_visibility_weight REAL NOT NULL,
    data_quality_transparency_weight REAL NOT NULL,
    threshold_blindness_weight REAL NOT NULL,
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

CREATE VIEW IF NOT EXISTS base_metric_value_view AS
SELECT
    framework_id,
    framework,
    framework_type,
    critical_use,
    resistance_coverage,
    recovery_insight,
    adaptive_capacity_visibility,
    buffer_visibility,
    justice_visibility,
    data_quality_transparency,
    threshold_blindness,
    (
        0.16 * resistance_coverage +
        0.16 * recovery_insight +
        0.16 * adaptive_capacity_visibility +
        0.15 * buffer_visibility +
        0.13 * justice_visibility +
        0.10 * data_quality_transparency -
        0.14 * threshold_blindness
    ) AS base_metric_value
FROM measurement_frameworks;

CREATE VIEW IF NOT EXISTS event_recovery_metrics_view AS
SELECT
    event_id,
    system_id,
    disturbance_type,
    shock_intensity,
    baseline_function,
    min_function,
    recovered_function,
    recovery_days,
    (baseline_function - min_function) AS performance_loss,
    CASE
        WHEN shock_intensity > 0
        THEN 1.0 - ((baseline_function - min_function) / shock_intensity)
        ELSE NULL
    END AS resistance_score,
    CASE
        WHEN (baseline_function - min_function) > 0
        THEN (recovered_function - min_function) / (baseline_function - min_function)
        ELSE NULL
    END AS recovery_completeness,
    1.0 / (1.0 + recovery_days / 30.0) AS recovery_speed
FROM disturbance_events;
