-- Financial System Resilience schema.

CREATE TABLE IF NOT EXISTS financial_resilience_strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    capital_strength REAL NOT NULL,
    liquidity_resilience REAL NOT NULL,
    infrastructure_robustness REAL NOT NULL,
    governance_capacity REAL NOT NULL,
    inclusive_resilience REAL NOT NULL,
    systemic_exposure REAL NOT NULL,
    implementation_burden REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS financial_system_profiles (
    system_id TEXT PRIMARY KEY,
    system TEXT NOT NULL,
    system_context TEXT NOT NULL,
    baseline_financial_function REAL NOT NULL,
    leverage_pressure REAL NOT NULL,
    liquidity_fragility REAL NOT NULL,
    common_asset_exposure REAL NOT NULL,
    operational_dependency REAL NOT NULL,
    climate_financial_exposure REAL NOT NULL,
    nonbank_exposure REAL NOT NULL,
    household_financial_fragility REAL NOT NULL,
    governance_capacity REAL NOT NULL,
    inclusion_sensitivity REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS financial_stress_events (
    event_id TEXT PRIMARY KEY,
    event_name TEXT NOT NULL,
    primary_stress TEXT NOT NULL,
    shock_intensity REAL NOT NULL,
    credit_loss REAL NOT NULL,
    liquidity_run REAL NOT NULL,
    market_fire_sale REAL NOT NULL,
    operational_disruption REAL NOT NULL,
    climate_repricing REAL NOT NULL,
    nonbank_stress REAL NOT NULL,
    household_default_pressure REAL NOT NULL,
    policy_coordination_stress REAL NOT NULL,
    inclusion_burden REAL NOT NULL,
    affected_functions TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS financial_resilience_scenarios (
    scenario TEXT PRIMARY KEY,
    capital_strength_weight REAL NOT NULL,
    liquidity_resilience_weight REAL NOT NULL,
    infrastructure_robustness_weight REAL NOT NULL,
    governance_capacity_weight REAL NOT NULL,
    inclusive_resilience_weight REAL NOT NULL,
    systemic_exposure_weight REAL NOT NULL,
    implementation_burden_weight REAL NOT NULL,
    description TEXT
);

CREATE VIEW IF NOT EXISTS financial_resilience_value_view AS
SELECT
    strategy_id,
    strategy,
    system_domain,
    critical_function,
    capital_strength,
    liquidity_resilience,
    infrastructure_robustness,
    governance_capacity,
    inclusive_resilience,
    systemic_exposure,
    implementation_burden,
    (
        0.16 * capital_strength +
        0.16 * liquidity_resilience +
        0.16 * infrastructure_robustness +
        0.16 * governance_capacity +
        0.16 * inclusive_resilience -
        0.12 * systemic_exposure -
        0.08 * implementation_burden
    ) AS financial_resilience_value,
    CASE
        WHEN inclusive_resilience < 8.0
        THEN 8.0 - inclusive_resilience
        ELSE 0
    END AS inclusion_gap
FROM financial_resilience_strategies;
