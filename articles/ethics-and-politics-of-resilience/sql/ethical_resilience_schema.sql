CREATE TABLE IF NOT EXISTS ethical_resilience_strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    protection_effectiveness REAL NOT NULL,
    equity REAL NOT NULL,
    governance_legitimacy REAL NOT NULL,
    recognition REAL NOT NULL,
    accountability REAL NOT NULL,
    burden_shift REAL NOT NULL,
    implementation_burden REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ethical_resilience_priority_scenarios (
    scenario TEXT PRIMARY KEY,
    protection_effectiveness_weight REAL NOT NULL,
    equity_weight REAL NOT NULL,
    governance_legitimacy_weight REAL NOT NULL,
    recognition_weight REAL NOT NULL,
    accountability_weight REAL NOT NULL,
    burden_shift_weight REAL NOT NULL,
    implementation_burden_weight REAL NOT NULL,
    description TEXT
);

CREATE VIEW IF NOT EXISTS ethical_resilience_balanced_value_view AS
SELECT
    strategy_id,
    strategy,
    critical_function,
    (
      0.24 * protection_effectiveness +
      0.22 * equity +
      0.18 * governance_legitimacy +
      0.14 * recognition +
      0.14 * accountability -
      0.05 * burden_shift -
      0.03 * implementation_burden
    ) AS ethical_resilience_value
FROM ethical_resilience_strategies;
