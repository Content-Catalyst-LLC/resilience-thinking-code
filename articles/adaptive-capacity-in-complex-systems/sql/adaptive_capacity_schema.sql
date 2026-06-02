-- Adaptive Capacity in Complex Systems schema
-- Supports systems, indicators, disturbances, scenarios, model runs, outputs, and threshold-risk diagnostics.

CREATE TABLE IF NOT EXISTS systems (
    system_id TEXT PRIMARY KEY,
    system_type TEXT NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS adaptive_capacity_indicators (
    indicator_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL REFERENCES systems(system_id),
    learning REAL NOT NULL CHECK (learning BETWEEN 0 AND 1),
    flexibility REAL NOT NULL CHECK (flexibility BETWEEN 0 AND 1),
    diversity REAL NOT NULL CHECK (diversity BETWEEN 0 AND 1),
    governance_capacity REAL NOT NULL CHECK (governance_capacity BETWEEN 0 AND 1),
    slack REAL NOT NULL CHECK (slack BETWEEN 0 AND 1),
    trust_legitimacy REAL NOT NULL CHECK (trust_legitimacy BETWEEN 0 AND 1),
    rigidity REAL NOT NULL CHECK (rigidity BETWEEN 0 AND 1),
    exposure REAL NOT NULL CHECK (exposure BETWEEN 0 AND 1)
);

CREATE TABLE IF NOT EXISTS disturbance_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    disturbance_load REAL NOT NULL CHECK (disturbance_load BETWEEN 0 AND 1),
    shock_intensity REAL NOT NULL CHECK (shock_intensity BETWEEN 0 AND 1),
    shock_frequency INTEGER NOT NULL,
    learning_gain REAL NOT NULL CHECK (learning_gain BETWEEN 0 AND 1),
    rigidity_growth REAL NOT NULL CHECK (rigidity_growth BETWEEN 0 AND 1),
    governance_response REAL NOT NULL CHECK (governance_response BETWEEN 0 AND 1),
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

CREATE VIEW IF NOT EXISTS adaptive_capacity_profile_view AS
SELECT
    s.system_id,
    s.system_type,
    s.critical_function,
    aci.learning,
    aci.flexibility,
    aci.diversity,
    aci.governance_capacity,
    aci.slack,
    aci.trust_legitimacy,
    aci.rigidity,
    aci.exposure,
    (
        0.18 * aci.learning +
        0.18 * aci.flexibility +
        0.17 * aci.diversity +
        0.17 * aci.governance_capacity +
        0.14 * aci.slack +
        0.16 * aci.trust_legitimacy -
        0.12 * aci.rigidity
    ) AS adaptive_capacity,
    (
        0.34 * aci.exposure +
        0.24 * aci.rigidity +
        0.16 * (1 - aci.slack) +
        0.14 * (1 - aci.trust_legitimacy) +
        0.12 * (1 - aci.governance_capacity)
    ) AS adaptive_vulnerability
FROM systems s
JOIN adaptive_capacity_indicators aci ON s.system_id = aci.system_id;
