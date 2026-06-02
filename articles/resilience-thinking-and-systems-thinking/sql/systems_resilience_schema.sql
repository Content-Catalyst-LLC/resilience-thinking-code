-- Systems Thinking and Resilience Thinking schema
-- Supports systems, feedback loops, stocks, flows, disturbances, thresholds, leverage points, and model runs.

CREATE TABLE IF NOT EXISTS systems (
    system_id TEXT PRIMARY KEY,
    system_type TEXT NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS systems_thinking_indicators (
    systems_indicator_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL REFERENCES systems(system_id),
    feedback_visibility REAL NOT NULL CHECK (feedback_visibility BETWEEN 0 AND 1),
    boundary_clarity REAL NOT NULL CHECK (boundary_clarity BETWEEN 0 AND 1),
    leverage_capacity REAL NOT NULL CHECK (leverage_capacity BETWEEN 0 AND 1),
    delay_management REAL NOT NULL CHECK (delay_management BETWEEN 0 AND 1)
);

CREATE TABLE IF NOT EXISTS resilience_thinking_indicators (
    resilience_indicator_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL REFERENCES systems(system_id),
    adaptive_capacity REAL NOT NULL CHECK (adaptive_capacity BETWEEN 0 AND 1),
    redundancy REAL NOT NULL CHECK (redundancy BETWEEN 0 AND 1),
    threshold_distance REAL NOT NULL CHECK (threshold_distance BETWEEN 0 AND 1),
    buffer_capacity REAL NOT NULL CHECK (buffer_capacity BETWEEN 0 AND 1),
    vulnerability_pressure REAL NOT NULL CHECK (vulnerability_pressure BETWEEN 0 AND 1),
    disturbance_exposure REAL NOT NULL CHECK (disturbance_exposure BETWEEN 0 AND 1)
);

CREATE TABLE IF NOT EXISTS feedback_loops (
    feedback_loop_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL REFERENCES systems(system_id),
    loop_name TEXT NOT NULL,
    loop_type TEXT NOT NULL CHECK (loop_type IN ('reinforcing', 'balancing', 'adaptive', 'maladaptive')),
    description TEXT
);

CREATE TABLE IF NOT EXISTS stocks_and_flows (
    stock_flow_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL REFERENCES systems(system_id),
    stock_name TEXT NOT NULL,
    inflow_name TEXT,
    outflow_name TEXT,
    resilience_significance TEXT
);

CREATE TABLE IF NOT EXISTS leverage_points (
    leverage_id TEXT PRIMARY KEY,
    leverage_level TEXT NOT NULL,
    relative_depth REAL NOT NULL,
    systems_thinking_description TEXT NOT NULL,
    resilience_contribution TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS disturbance_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    disturbance_load REAL NOT NULL,
    shock_intensity REAL NOT NULL,
    shock_frequency INTEGER NOT NULL,
    delay_penalty REAL NOT NULL,
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

CREATE VIEW IF NOT EXISTS systems_resilience_profile_view AS
SELECT
    s.system_id,
    s.system_type,
    s.critical_function,
    (
        0.28 * sti.feedback_visibility +
        0.24 * sti.boundary_clarity +
        0.24 * sti.leverage_capacity +
        0.24 * sti.delay_management
    ) AS systems_thinking_score,
    (
        0.24 * rti.adaptive_capacity +
        0.20 * rti.redundancy +
        0.22 * rti.threshold_distance +
        0.18 * rti.buffer_capacity -
        0.08 * rti.vulnerability_pressure -
        0.08 * rti.disturbance_exposure
    ) AS resilience_thinking_score
FROM systems s
JOIN systems_thinking_indicators sti ON s.system_id = sti.system_id
JOIN resilience_thinking_indicators rti ON s.system_id = rti.system_id;
