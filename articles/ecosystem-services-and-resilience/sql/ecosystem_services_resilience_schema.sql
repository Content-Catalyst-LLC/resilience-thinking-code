-- Ecosystem Services and Resilience schema
-- Supports services, ecosystems, service categories, functions, access metrics, disturbance scenarios, model runs, and outputs.

CREATE TABLE IF NOT EXISTS ecosystems (
    ecosystem_id TEXT PRIMARY KEY,
    ecosystem_type TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS service_categories (
    category_id TEXT PRIMARY KEY,
    category_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS ecosystem_services (
    service_id TEXT PRIMARY KEY,
    service_name TEXT NOT NULL,
    category_id TEXT NOT NULL REFERENCES service_categories(category_id),
    ecosystem_id TEXT NOT NULL REFERENCES ecosystems(ecosystem_id),
    critical_benefit TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS service_profile_indicators (
    profile_id TEXT PRIMARY KEY,
    service_id TEXT NOT NULL REFERENCES ecosystem_services(service_id),
    current_service_flow REAL NOT NULL CHECK (current_service_flow BETWEEN 0 AND 1),
    ecological_condition REAL NOT NULL CHECK (ecological_condition BETWEEN 0 AND 1),
    functional_diversity REAL NOT NULL CHECK (functional_diversity BETWEEN 0 AND 1),
    functional_redundancy REAL NOT NULL CHECK (functional_redundancy BETWEEN 0 AND 1),
    threshold_distance REAL NOT NULL CHECK (threshold_distance BETWEEN 0 AND 1),
    governance_capacity REAL NOT NULL CHECK (governance_capacity BETWEEN 0 AND 1),
    disturbance_exposure REAL NOT NULL CHECK (disturbance_exposure BETWEEN 0 AND 1),
    access_equity REAL NOT NULL CHECK (access_equity BETWEEN 0 AND 1),
    ecological_memory REAL NOT NULL CHECK (ecological_memory BETWEEN 0 AND 1)
);

CREATE TABLE IF NOT EXISTS service_bundles (
    bundle_id TEXT PRIMARY KEY,
    bundle_name TEXT NOT NULL,
    ecosystem_id TEXT NOT NULL REFERENCES ecosystems(ecosystem_id),
    services_in_bundle TEXT NOT NULL,
    primary_tradeoff TEXT,
    resilience_note TEXT
);

CREATE TABLE IF NOT EXISTS disturbance_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    disturbance_load REAL NOT NULL CHECK (disturbance_load BETWEEN 0 AND 1),
    shock_intensity REAL NOT NULL CHECK (shock_intensity BETWEEN 0 AND 1),
    shock_frequency INTEGER NOT NULL,
    governance_response REAL NOT NULL CHECK (governance_response BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE IF NOT EXISTS model_runs (
    run_id TEXT PRIMARY KEY,
    model_name TEXT NOT NULL,
    model_purpose TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS model_outputs (
    output_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL REFERENCES model_runs(run_id),
    output_name TEXT NOT NULL,
    output_path TEXT NOT NULL,
    interpretation_note TEXT
);

CREATE VIEW IF NOT EXISTS ecosystem_service_resilience_profile_view AS
SELECT
    es.service_id,
    es.service_name,
    sc.category_name,
    e.ecosystem_type,
    es.critical_benefit,
    spi.current_service_flow,
    (
        0.10 * spi.current_service_flow +
        0.17 * spi.ecological_condition +
        0.15 * spi.functional_diversity +
        0.14 * spi.functional_redundancy +
        0.15 * spi.threshold_distance +
        0.12 * spi.governance_capacity +
        0.09 * spi.access_equity +
        0.12 * spi.ecological_memory -
        0.12 * spi.disturbance_exposure
    ) AS service_resilience_profile,
    (
        0.26 * (1 - spi.threshold_distance) +
        0.22 * spi.disturbance_exposure +
        0.16 * (1 - spi.functional_redundancy) +
        0.14 * (1 - spi.functional_diversity) +
        0.12 * (1 - spi.governance_capacity) +
        0.10 * (1 - spi.ecological_memory) -
        0.08 * spi.access_equity
    ) AS service_threshold_risk_index
FROM ecosystem_services es
JOIN service_categories sc ON es.category_id = sc.category_id
JOIN ecosystems e ON es.ecosystem_id = e.ecosystem_id
JOIN service_profile_indicators spi ON es.service_id = spi.service_id;
