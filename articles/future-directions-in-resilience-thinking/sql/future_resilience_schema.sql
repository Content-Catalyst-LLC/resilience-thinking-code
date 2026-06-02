CREATE TABLE IF NOT EXISTS future_resilience_strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    adaptive_capacity REAL NOT NULL,
    buffering_capacity REAL NOT NULL,
    transformability REAL NOT NULL,
    governance_quality REAL NOT NULL,
    equity_performance REAL NOT NULL,
    digital_resilience REAL NOT NULL,
    climate_readiness REAL NOT NULL,
    systemic_exposure REAL NOT NULL,
    implementation_burden REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS future_resilience_priority_scenarios (
    scenario TEXT PRIMARY KEY,
    adaptive_capacity_weight REAL NOT NULL,
    buffering_capacity_weight REAL NOT NULL,
    transformability_weight REAL NOT NULL,
    governance_quality_weight REAL NOT NULL,
    equity_performance_weight REAL NOT NULL,
    digital_resilience_weight REAL NOT NULL,
    climate_readiness_weight REAL NOT NULL,
    systemic_exposure_weight REAL NOT NULL,
    implementation_burden_weight REAL NOT NULL,
    description TEXT
);

CREATE VIEW IF NOT EXISTS future_resilience_balanced_value_view AS
SELECT
    strategy_id,
    strategy,
    critical_function,
    (
      0.16 * adaptive_capacity +
      0.14 * buffering_capacity +
      0.16 * transformability +
      0.14 * governance_quality +
      0.14 * equity_performance +
      0.12 * digital_resilience +
      0.14 * climate_readiness -
      0.05 * systemic_exposure -
      0.05 * implementation_burden
    ) AS resilience_value
FROM future_resilience_strategies;
