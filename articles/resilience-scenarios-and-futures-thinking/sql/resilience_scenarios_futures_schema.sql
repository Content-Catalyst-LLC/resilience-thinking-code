CREATE TABLE IF NOT EXISTS resilience_scenario_strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    horizon_scanning REAL NOT NULL,
    weak_signal_detection REAL NOT NULL,
    stress_testing REAL NOT NULL,
    adaptive_pathways REAL NOT NULL,
    participation REAL NOT NULL,
    data_modeling REAL NOT NULL,
    governance_integration REAL NOT NULL,
    equity_sensitivity REAL NOT NULL,
    transformation_potential REAL NOT NULL,
    scenario_design_risk REAL NOT NULL,
    implementation_burden REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS resilience_future_pathways (
    pathway_id TEXT PRIMARY KEY,
    scenario TEXT NOT NULL,
    climate_stress_growth REAL NOT NULL,
    infrastructure_stress_growth REAL NOT NULL,
    social_vulnerability_growth REAL NOT NULL,
    governance_capacity REAL NOT NULL,
    adaptive_capacity REAL NOT NULL,
    participation REAL NOT NULL,
    equity_focus REAL NOT NULL,
    transformation_investment REAL NOT NULL,
    redundancy_and_slack REAL NOT NULL,
    initial_function REAL NOT NULL,
    initial_vulnerability REAL NOT NULL,
    initial_trust REAL NOT NULL
);

CREATE VIEW IF NOT EXISTS resilience_scenario_value_view AS
SELECT
    strategy_id,
    strategy,
    (
      0.10 * horizon_scanning +
      0.10 * weak_signal_detection +
      0.11 * stress_testing +
      0.12 * adaptive_pathways +
      0.11 * participation +
      0.10 * data_modeling +
      0.12 * governance_integration +
      0.12 * equity_sensitivity +
      0.12 * transformation_potential -
      0.04 * scenario_design_risk -
      0.04 * implementation_burden
    ) AS scenario_resilience_value
FROM resilience_scenario_strategies;
