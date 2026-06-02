-- Feedback Loops in Resilient Systems schema
-- Supports systems, feedback loops, causal links, delays, scenarios, diagnostics, model runs, and outputs.

CREATE TABLE IF NOT EXISTS systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_type TEXT NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS feedback_profiles (
    profile_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL REFERENCES systems(system_id),
    reinforcing_gain REAL NOT NULL,
    balancing_strength REAL NOT NULL,
    delay_steps INTEGER NOT NULL,
    disturbance_load REAL NOT NULL,
    adaptive_capacity REAL NOT NULL,
    signal_quality REAL NOT NULL,
    system_memory REAL NOT NULL,
    justice_visibility REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS feedback_loops (
    loop_id TEXT PRIMARY KEY,
    system_id TEXT REFERENCES systems(system_id),
    loop_name TEXT NOT NULL,
    loop_type TEXT CHECK (loop_type IN ('reinforcing', 'balancing', 'mixed', 'unknown')),
    purpose_note TEXT
);

CREATE TABLE IF NOT EXISTS causal_links (
    link_id TEXT PRIMARY KEY,
    loop_id TEXT NOT NULL REFERENCES feedback_loops(loop_id),
    from_variable TEXT NOT NULL,
    to_variable TEXT NOT NULL,
    polarity TEXT NOT NULL CHECK (polarity IN ('+', '-')),
    delay_note TEXT
);

CREATE TABLE IF NOT EXISTS feedback_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    reinforcing_gain REAL NOT NULL,
    balancing_strength REAL NOT NULL,
    delay_steps INTEGER NOT NULL,
    target REAL NOT NULL,
    disturbance_shock REAL NOT NULL,
    adaptive_response REAL NOT NULL,
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
