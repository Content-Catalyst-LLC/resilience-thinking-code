-- Resilience Thinking SQL schema
-- Educational schema for systems, disturbances, resilience dimensions, scenarios, and model runs.

CREATE TABLE IF NOT EXISTS resilience_systems (
    system_id INTEGER PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_type TEXT NOT NULL,
    description TEXT NOT NULL,
    boundary_note TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS resilience_dimensions (
    dimension_id INTEGER PRIMARY KEY,
    dimension_name TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS system_resilience_scores (
    score_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    dimension_id INTEGER NOT NULL,
    score_value REAL NOT NULL,
    evidence_note TEXT,
    FOREIGN KEY (system_id) REFERENCES resilience_systems(system_id),
    FOREIGN KEY (dimension_id) REFERENCES resilience_dimensions(dimension_id)
);

CREATE TABLE IF NOT EXISTS disturbances (
    disturbance_id INTEGER PRIMARY KEY,
    disturbance_name TEXT NOT NULL,
    disturbance_type TEXT NOT NULL,
    intensity REAL NOT NULL,
    frequency REAL NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS resilience_scenarios (
    scenario_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    disturbance_id INTEGER NOT NULL,
    scenario_name TEXT NOT NULL,
    assumptions TEXT NOT NULL,
    FOREIGN KEY (system_id) REFERENCES resilience_systems(system_id),
    FOREIGN KEY (disturbance_id) REFERENCES disturbances(disturbance_id)
);

CREATE TABLE IF NOT EXISTS model_runs (
    model_run_id INTEGER PRIMARY KEY,
    scenario_id INTEGER NOT NULL,
    model_name TEXT NOT NULL,
    run_timestamp TEXT NOT NULL,
    output_path TEXT NOT NULL,
    interpretation_note TEXT,
    FOREIGN KEY (scenario_id) REFERENCES resilience_scenarios(scenario_id)
);

INSERT INTO resilience_dimensions
(dimension_id, dimension_name, description)
VALUES
(1, 'Adaptive Capacity', 'Ability to adjust behavior, structure, or function under disturbance.'),
(2, 'Threshold Distance', 'Distance from critical boundaries or regime-shift risk.'),
(3, 'Learning Capacity', 'Ability to update action based on feedback and experience.'),
(4, 'Redundancy', 'Overlapping capacity that protects function when components fail.'),
(5, 'Diversity', 'Variation in pathways, actors, functions, or resources.'),
(6, 'Governance Capacity', 'Ability to coordinate, decide, and remain legitimate under stress.'),
(7, 'Equity Capacity', 'Ability to protect vulnerable populations and distribute risk fairly.');
