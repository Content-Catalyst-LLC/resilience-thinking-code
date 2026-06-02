-- Economic Resilience schema.

CREATE TABLE IF NOT EXISTS economic_resilience_strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    resistance REAL NOT NULL,
    recovery REAL NOT NULL,
    adaptability REAL NOT NULL,
    transformability REAL NOT NULL,
    equity_protection REAL NOT NULL,
    institutional_capacity REAL NOT NULL,
    implementation_burden REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS economic_system_profiles (
    system_id TEXT PRIMARY KEY,
    system TEXT NOT NULL,
    system_context TEXT NOT NULL,
    baseline_economic_function REAL NOT NULL,
    sector_concentration REAL NOT NULL,
    household_fragility REAL NOT NULL,
    firm_fragility REAL NOT NULL,
    financial_exposure REAL NOT NULL,
    labor_market_rigidity REAL NOT NULL,
    infrastructure_exposure REAL NOT NULL,
    climate_exposure REAL NOT NULL,
    institutional_capacity REAL NOT NULL,
    equity_sensitivity REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS economic_stress_events (
    event_id TEXT PRIMARY KEY,
    event_name TEXT NOT NULL,
    primary_stress TEXT NOT NULL,
    shock_intensity REAL NOT NULL,
    demand_shock REAL NOT NULL,
    supply_shock REAL NOT NULL,
    financial_stress REAL NOT NULL,
    labor_disruption REAL NOT NULL,
    infrastructure_stress REAL NOT NULL,
    climate_pressure REAL NOT NULL,
    fiscal_pressure REAL NOT NULL,
    equity_burden REAL NOT NULL,
    affected_functions TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS economic_resilience_scenarios (
    scenario TEXT PRIMARY KEY,
    resistance_weight REAL NOT NULL,
    recovery_weight REAL NOT NULL,
    adaptability_weight REAL NOT NULL,
    transformability_weight REAL NOT NULL,
    equity_protection_weight REAL NOT NULL,
    institutional_capacity_weight REAL NOT NULL,
    implementation_burden_weight REAL NOT NULL,
    description TEXT
);

CREATE VIEW IF NOT EXISTS economic_resilience_value_view AS
SELECT
    strategy_id,
    strategy,
    system_domain,
    critical_function,
    resistance,
    recovery,
    adaptability,
    transformability,
    equity_protection,
    institutional_capacity,
    implementation_burden,
    (
        0.16 * resistance +
        0.16 * recovery +
        0.17 * adaptability +
        0.17 * transformability +
        0.17 * equity_protection +
        0.17 * institutional_capacity -
        0.02 * implementation_burden
    ) AS economic_resilience_value,
    CASE
        WHEN equity_protection < 8.3
        THEN 8.3 - equity_protection
        ELSE 0
    END AS equity_gap
FROM economic_resilience_strategies;
