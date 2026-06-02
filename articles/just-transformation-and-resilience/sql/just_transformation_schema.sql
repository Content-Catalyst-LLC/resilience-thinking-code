CREATE TABLE IF NOT EXISTS just_transformation_pathways (
    pathway_id TEXT PRIMARY KEY,
    pathway TEXT NOT NULL,
    resilience_capacity REAL NOT NULL,
    transformation_capacity REAL NOT NULL,
    equity REAL NOT NULL,
    ecological_repair REAL NOT NULL,
    governance_legitimacy REAL NOT NULL,
    livelihood_protection REAL NOT NULL,
    exposure_reduction REAL NOT NULL,
    burden_shift REAL NOT NULL,
    lock_in_risk REAL NOT NULL,
    implementation_burden REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS just_transformation_dynamic_pathways (
    dynamic_id TEXT PRIMARY KEY,
    pathway TEXT NOT NULL,
    initial_exposure REAL NOT NULL,
    institutional_capacity REAL NOT NULL,
    transformation_investment REAL NOT NULL,
    social_protection REAL NOT NULL,
    ecological_repair REAL NOT NULL,
    governance_legitimacy REAL NOT NULL,
    burden_shift REAL NOT NULL,
    lock_in_risk REAL NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS just_transformation_priority_scenarios (
    scenario TEXT PRIMARY KEY,
    resilience_capacity_weight REAL NOT NULL,
    transformation_capacity_weight REAL NOT NULL,
    equity_weight REAL NOT NULL,
    ecological_repair_weight REAL NOT NULL,
    governance_legitimacy_weight REAL NOT NULL,
    livelihood_protection_weight REAL NOT NULL,
    exposure_reduction_weight REAL NOT NULL,
    burden_shift_weight REAL NOT NULL,
    lock_in_risk_weight REAL NOT NULL,
    implementation_burden_weight REAL NOT NULL,
    description TEXT
);

CREATE VIEW IF NOT EXISTS just_transformation_balanced_value_view AS
SELECT
    pathway_id,
    pathway,
    critical_function,
    (
      0.13 * resilience_capacity +
      0.16 * transformation_capacity +
      0.16 * equity +
      0.13 * ecological_repair +
      0.14 * governance_legitimacy +
      0.13 * livelihood_protection +
      0.13 * exposure_reduction -
      0.03 * burden_shift -
      0.02 * lock_in_risk -
      0.01 * implementation_burden
    ) AS just_transformation_value
FROM just_transformation_pathways;
