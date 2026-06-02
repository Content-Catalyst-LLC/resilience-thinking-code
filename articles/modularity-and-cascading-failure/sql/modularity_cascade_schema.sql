-- Modularity and Cascading Failure schema
-- Supports nodes, dependencies, containment strategies, cascade events,
-- scenarios, model runs, and outputs.

CREATE TABLE IF NOT EXISTS cascade_nodes (
    node_id TEXT PRIMARY KEY,
    node TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    redundancy REAL NOT NULL,
    isolation_capacity REAL NOT NULL,
    common_mode_exposure REAL NOT NULL,
    justice_sensitivity REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cascade_edges (
    edge_id TEXT PRIMARY KEY,
    source_node TEXT NOT NULL,
    target_node TEXT NOT NULL,
    coupling_strength REAL NOT NULL,
    dependency_type TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS containment_strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    modularity REAL NOT NULL,
    redundancy REAL NOT NULL,
    dependency_mapping REAL NOT NULL,
    isolation_capacity REAL NOT NULL,
    coordination_readiness REAL NOT NULL,
    justice_protection REAL NOT NULL,
    common_mode_risk REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cascade_events (
    event_id TEXT PRIMARY KEY,
    initial_failure_node TEXT NOT NULL,
    final_failures INTEGER NOT NULL,
    cascade_steps INTEGER NOT NULL,
    justice_weighted_impact REAL NOT NULL,
    interpretation_note TEXT
);

CREATE TABLE IF NOT EXISTS containment_scenarios (
    scenario TEXT PRIMARY KEY,
    modularity_weight REAL NOT NULL,
    redundancy_weight REAL NOT NULL,
    dependency_mapping_weight REAL NOT NULL,
    isolation_capacity_weight REAL NOT NULL,
    coordination_readiness_weight REAL NOT NULL,
    justice_protection_weight REAL NOT NULL,
    common_mode_risk_weight REAL NOT NULL,
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

CREATE VIEW IF NOT EXISTS base_containment_value_view AS
SELECT
    strategy_id,
    strategy,
    system_domain,
    critical_function,
    modularity,
    redundancy,
    dependency_mapping,
    isolation_capacity,
    coordination_readiness,
    justice_protection,
    common_mode_risk,
    (
        0.18 * modularity +
        0.16 * redundancy +
        0.16 * dependency_mapping +
        0.18 * isolation_capacity +
        0.14 * coordination_readiness +
        0.10 * justice_protection -
        0.08 * common_mode_risk
    ) AS base_containment_value
FROM containment_strategies;

CREATE VIEW IF NOT EXISTS cascade_pressure_view AS
SELECT
    e.edge_id,
    e.source_node,
    e.target_node,
    e.dependency_type,
    e.coupling_strength,
    n.redundancy,
    n.isolation_capacity,
    n.common_mode_exposure,
    (
        e.coupling_strength +
        0.35 * n.common_mode_exposure -
        0.30 * n.redundancy -
        0.25 * n.isolation_capacity
    ) AS estimated_cascade_pressure
FROM cascade_edges e
JOIN cascade_nodes n ON e.target_node = n.node;
