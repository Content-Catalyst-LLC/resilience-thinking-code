-- Small Business and Local Economic Resilience schema.

CREATE TABLE IF NOT EXISTS local_economic_resilience_strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    liquidity_support REAL NOT NULL,
    workforce_capacity REAL NOT NULL,
    supply_resilience REAL NOT NULL,
    digital_readiness REAL NOT NULL,
    public_capacity REAL NOT NULL,
    community_wealth REAL NOT NULL,
    equity_access REAL NOT NULL,
    inequality_risk REAL NOT NULL,
    implementation_burden REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS small_business_profiles (
    business_id TEXT PRIMARY KEY,
    business TEXT NOT NULL,
    business_context TEXT NOT NULL,
    initial_function REAL NOT NULL,
    cash_runway REAL NOT NULL,
    workforce_capacity REAL NOT NULL,
    supplier_resilience REAL NOT NULL,
    digital_readiness REAL NOT NULL,
    community_embeddedness REAL NOT NULL,
    public_support_access REAL NOT NULL,
    equity_access REAL NOT NULL,
    initial_owner_strain REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS local_disruption_events (
    event_id TEXT PRIMARY KEY,
    event_name TEXT NOT NULL,
    primary_stress TEXT NOT NULL,
    shock_intensity REAL NOT NULL,
    demand_loss REAL NOT NULL,
    supplier_disruption REAL NOT NULL,
    digital_disruption REAL NOT NULL,
    rent_debt_pressure REAL NOT NULL,
    workforce_stress REAL NOT NULL,
    insurance_gap REAL NOT NULL,
    public_support_delay REAL NOT NULL,
    inequality_pressure REAL NOT NULL,
    affected_functions TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS local_resilience_scenarios (
    scenario TEXT PRIMARY KEY,
    liquidity_support_weight REAL NOT NULL,
    workforce_capacity_weight REAL NOT NULL,
    supply_resilience_weight REAL NOT NULL,
    digital_readiness_weight REAL NOT NULL,
    public_capacity_weight REAL NOT NULL,
    community_wealth_weight REAL NOT NULL,
    equity_access_weight REAL NOT NULL,
    inequality_risk_weight REAL NOT NULL,
    implementation_burden_weight REAL NOT NULL,
    description TEXT
);

CREATE VIEW IF NOT EXISTS local_resilience_value_view AS
SELECT
    strategy_id,
    strategy,
    system_domain,
    critical_function,
    liquidity_support,
    workforce_capacity,
    supply_resilience,
    digital_readiness,
    public_capacity,
    community_wealth,
    equity_access,
    inequality_risk,
    implementation_burden,
    (
        0.14 * liquidity_support +
        0.14 * workforce_capacity +
        0.12 * supply_resilience +
        0.12 * digital_readiness +
        0.14 * public_capacity +
        0.15 * community_wealth +
        0.16 * equity_access -
        0.07 * inequality_risk -
        0.06 * implementation_burden
    ) AS local_resilience_value
FROM local_economic_resilience_strategies;
