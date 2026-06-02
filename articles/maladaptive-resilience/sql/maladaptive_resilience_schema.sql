CREATE TABLE IF NOT EXISTS maladaptive_resilience_strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    persistence_capacity REAL NOT NULL,
    harm_reduction REAL NOT NULL,
    lock_in_reduction REAL NOT NULL,
    equity REAL NOT NULL,
    transformation_capacity REAL NOT NULL,
    ecological_integrity REAL NOT NULL,
    burden_shift REAL NOT NULL,
    implementation_burden REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS maladaptive_pathways (
    pathway_id TEXT PRIMARY KEY,
    pathway TEXT NOT NULL,
    initial_persistence REAL NOT NULL,
    initial_harm REAL NOT NULL,
    initial_lock_in REAL NOT NULL,
    burden_shift REAL NOT NULL,
    transformation_capacity REAL NOT NULL,
    ecological_integrity REAL NOT NULL,
    equity REAL NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS maladaptive_priority_scenarios (
    scenario TEXT PRIMARY KEY,
    persistence_capacity_weight REAL NOT NULL,
    harm_reduction_weight REAL NOT NULL,
    lock_in_reduction_weight REAL NOT NULL,
    equity_weight REAL NOT NULL,
    transformation_capacity_weight REAL NOT NULL,
    ecological_integrity_weight REAL NOT NULL,
    burden_shift_weight REAL NOT NULL,
    implementation_burden_weight REAL NOT NULL,
    description TEXT
);

CREATE VIEW IF NOT EXISTS maladaptive_balanced_value_view AS
SELECT
    strategy_id,
    strategy,
    critical_function,
    (
      0.12 * persistence_capacity +
      0.20 * harm_reduction +
      0.16 * lock_in_reduction +
      0.16 * equity +
      0.18 * transformation_capacity +
      0.14 * ecological_integrity -
      0.03 * burden_shift -
      0.01 * implementation_burden
    ) AS adaptive_resilience_value
FROM maladaptive_resilience_strategies;
