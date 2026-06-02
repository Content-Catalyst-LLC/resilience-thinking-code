CREATE TABLE IF NOT EXISTS resilience_or_abandonment_strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    protective_effectiveness REAL NOT NULL,
    material_support REAL NOT NULL,
    accessible_recovery REAL NOT NULL,
    governance_inclusion REAL NOT NULL,
    transformation_potential REAL NOT NULL,
    exposure_reduction REAL NOT NULL,
    burden_shift REAL NOT NULL,
    implementation_burden REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS abandonment_pathways (
    pathway_id TEXT PRIMARY KEY,
    pathway TEXT NOT NULL,
    initial_exposure REAL NOT NULL,
    material_support REAL NOT NULL,
    accessible_recovery REAL NOT NULL,
    governance_inclusion REAL NOT NULL,
    public_capacity REAL NOT NULL,
    burden_shift REAL NOT NULL,
    transformation REAL NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS abandonment_priority_scenarios (
    scenario TEXT PRIMARY KEY,
    protective_effectiveness_weight REAL NOT NULL,
    material_support_weight REAL NOT NULL,
    accessible_recovery_weight REAL NOT NULL,
    governance_inclusion_weight REAL NOT NULL,
    transformation_potential_weight REAL NOT NULL,
    exposure_reduction_weight REAL NOT NULL,
    burden_shift_weight REAL NOT NULL,
    implementation_burden_weight REAL NOT NULL,
    description TEXT
);

CREATE VIEW IF NOT EXISTS support_resilience_balanced_value_view AS
SELECT
    strategy_id,
    strategy,
    critical_function,
    (
      0.18 * protective_effectiveness +
      0.18 * material_support +
      0.16 * accessible_recovery +
      0.14 * governance_inclusion +
      0.13 * transformation_potential +
      0.16 * exposure_reduction -
      0.04 * burden_shift -
      0.01 * implementation_burden
    ) AS support_resilience_value
FROM resilience_or_abandonment_strategies;
