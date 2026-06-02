-- Adaptive Cycles and Panarchy schema
-- Supports systems, adaptive cycles, phases, indicators, scale relationships, scenarios, model runs, and outputs.

CREATE TABLE IF NOT EXISTS systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_type TEXT NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cycle_states (
    state_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL REFERENCES systems(system_id),
    phase TEXT NOT NULL CHECK (phase IN ('r', 'K', 'Omega', 'alpha')),
    potential REAL NOT NULL CHECK (potential BETWEEN 0 AND 1),
    connectedness REAL NOT NULL CHECK (connectedness BETWEEN 0 AND 1),
    resilience REAL NOT NULL CHECK (resilience BETWEEN 0 AND 1),
    rigidity REAL NOT NULL CHECK (rigidity BETWEEN 0 AND 1),
    memory REAL NOT NULL CHECK (memory BETWEEN 0 AND 1),
    novelty REAL NOT NULL CHECK (novelty BETWEEN 0 AND 1),
    disturbance_exposure REAL NOT NULL CHECK (disturbance_exposure BETWEEN 0 AND 1)
);

CREATE TABLE IF NOT EXISTS panarchy_scales (
    scale_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL REFERENCES systems(system_id),
    scale_name TEXT NOT NULL,
    scale_speed TEXT NOT NULL CHECK (scale_speed IN ('fast', 'medium', 'slow')),
    potential REAL NOT NULL CHECK (potential BETWEEN 0 AND 1),
    connectedness REAL NOT NULL CHECK (connectedness BETWEEN 0 AND 1),
    resilience REAL NOT NULL CHECK (resilience BETWEEN 0 AND 1),
    rigidity REAL NOT NULL CHECK (rigidity BETWEEN 0 AND 1),
    memory REAL NOT NULL CHECK (memory BETWEEN 0 AND 1),
    innovation_capacity REAL NOT NULL CHECK (innovation_capacity BETWEEN 0 AND 1),
    disturbance_signal REAL NOT NULL CHECK (disturbance_signal BETWEEN 0 AND 1)
);

CREATE TABLE IF NOT EXISTS cycle_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    growth_rate REAL NOT NULL,
    connect_rate REAL NOT NULL,
    disturbance_pressure REAL NOT NULL,
    rigidity_threshold REAL NOT NULL,
    resilience_threshold REAL NOT NULL,
    memory_strength REAL NOT NULL,
    novelty_range_low REAL NOT NULL,
    novelty_range_high REAL NOT NULL,
    revolt_strength REAL NOT NULL,
    remember_strength REAL NOT NULL,
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

CREATE VIEW IF NOT EXISTS adaptive_cycle_risk_view AS
SELECT
    s.system_id,
    s.system_name,
    s.system_type,
    cs.phase,
    cs.potential,
    cs.connectedness,
    cs.resilience,
    cs.rigidity,
    cs.memory,
    cs.novelty,
    cs.disturbance_exposure,
    (
        0.30 * cs.rigidity +
        0.24 * cs.connectedness +
        0.20 * cs.disturbance_exposure +
        0.16 * (1 - cs.resilience) +
        0.10 * (1 - cs.novelty)
    ) AS release_risk_index,
    (
        0.26 * cs.memory +
        0.24 * cs.novelty +
        0.20 * cs.resilience +
        0.16 * (1 - cs.rigidity) +
        0.14 * cs.potential
    ) AS renewal_potential_index
FROM systems s
JOIN cycle_states cs ON s.system_id = cs.system_id;
