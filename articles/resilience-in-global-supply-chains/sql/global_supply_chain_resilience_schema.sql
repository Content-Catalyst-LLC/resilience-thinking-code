-- Global Supply Chain Resilience schema.

CREATE TABLE IF NOT EXISTS supply_chain_resilience_strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    redundancy REAL NOT NULL,
    flexibility REAL NOT NULL,
    visibility REAL NOT NULL,
    coordination REAL NOT NULL,
    adaptive_capacity REAL NOT NULL,
    equity_safeguards REAL NOT NULL,
    infrastructure_continuity REAL NOT NULL,
    systemic_exposure REAL NOT NULL,
    implementation_burden REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS supply_network_profiles (
    network_id TEXT PRIMARY KEY,
    network TEXT NOT NULL,
    network_context TEXT NOT NULL,
    baseline_flow_performance REAL NOT NULL,
    supplier_concentration REAL NOT NULL,
    route_chokepoint_exposure REAL NOT NULL,
    inventory_thinness REAL NOT NULL,
    climate_exposure REAL NOT NULL,
    cyber_dependency REAL NOT NULL,
    labor_vulnerability REAL NOT NULL,
    infrastructure_fragility REAL NOT NULL,
    coordination_capacity REAL NOT NULL,
    equity_sensitivity REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS supply_chain_stress_events (
    event_id TEXT PRIMARY KEY,
    event_name TEXT NOT NULL,
    primary_stress TEXT NOT NULL,
    shock_intensity REAL NOT NULL,
    supplier_failure REAL NOT NULL,
    logistics_disruption REAL NOT NULL,
    demand_surge REAL NOT NULL,
    inventory_depletion REAL NOT NULL,
    cyber_disruption REAL NOT NULL,
    climate_pressure REAL NOT NULL,
    labor_disruption REAL NOT NULL,
    coordination_stress REAL NOT NULL,
    equity_burden REAL NOT NULL,
    affected_functions TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS supply_chain_resilience_scenarios (
    scenario TEXT PRIMARY KEY,
    redundancy_weight REAL NOT NULL,
    flexibility_weight REAL NOT NULL,
    visibility_weight REAL NOT NULL,
    coordination_weight REAL NOT NULL,
    adaptive_capacity_weight REAL NOT NULL,
    equity_safeguards_weight REAL NOT NULL,
    infrastructure_continuity_weight REAL NOT NULL,
    systemic_exposure_weight REAL NOT NULL,
    implementation_burden_weight REAL NOT NULL,
    description TEXT
);

CREATE VIEW IF NOT EXISTS supply_chain_resilience_value_view AS
SELECT
    strategy_id,
    strategy,
    system_domain,
    critical_function,
    redundancy,
    flexibility,
    visibility,
    coordination,
    adaptive_capacity,
    equity_safeguards,
    infrastructure_continuity,
    systemic_exposure,
    implementation_burden,
    (
        0.13 * redundancy +
        0.13 * flexibility +
        0.13 * visibility +
        0.13 * coordination +
        0.13 * adaptive_capacity +
        0.13 * equity_safeguards +
        0.13 * infrastructure_continuity -
        0.06 * systemic_exposure -
        0.03 * implementation_burden
    ) AS supply_chain_resilience_value,
    CASE
        WHEN equity_safeguards < 8.0
        THEN 8.0 - equity_safeguards
        ELSE 0
    END AS equity_gap
FROM supply_chain_resilience_strategies;
