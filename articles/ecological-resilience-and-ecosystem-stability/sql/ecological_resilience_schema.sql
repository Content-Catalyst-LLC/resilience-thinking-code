CREATE TABLE IF NOT EXISTS ecosystems (
    ecosystem_id TEXT PRIMARY KEY,
    ecosystem_type TEXT NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS stability_indicators (
    stability_indicator_id TEXT PRIMARY KEY,
    ecosystem_id TEXT NOT NULL REFERENCES ecosystems(ecosystem_id),
    short_run_stability REAL NOT NULL CHECK (short_run_stability BETWEEN 0 AND 1)
);

CREATE TABLE IF NOT EXISTS resilience_indicators (
    resilience_indicator_id TEXT PRIMARY KEY,
    ecosystem_id TEXT NOT NULL REFERENCES ecosystems(ecosystem_id),
    biodiversity REAL NOT NULL CHECK (biodiversity BETWEEN 0 AND 1),
    functional_diversity REAL NOT NULL CHECK (functional_diversity BETWEEN 0 AND 1),
    response_diversity REAL NOT NULL CHECK (response_diversity BETWEEN 0 AND 1),
    threshold_distance REAL NOT NULL CHECK (threshold_distance BETWEEN 0 AND 1),
    basin_width REAL NOT NULL CHECK (basin_width BETWEEN 0 AND 1),
    regenerative_capacity REAL NOT NULL CHECK (regenerative_capacity BETWEEN 0 AND 1),
    ecological_memory REAL NOT NULL CHECK (ecological_memory BETWEEN 0 AND 1),
    connectivity REAL NOT NULL CHECK (connectivity BETWEEN 0 AND 1),
    disturbance_exposure REAL NOT NULL CHECK (disturbance_exposure BETWEEN 0 AND 1),
    slow_variable_pressure REAL NOT NULL CHECK (slow_variable_pressure BETWEEN 0 AND 1)
);

CREATE VIEW IF NOT EXISTS ecosystem_resilience_profile_view AS
SELECT
    e.ecosystem_id,
    e.ecosystem_type,
    e.critical_function,
    s.short_run_stability AS stability_score,
    (
        0.11 * s.short_run_stability +
        0.13 * r.biodiversity +
        0.13 * r.functional_diversity +
        0.13 * r.response_diversity +
        0.16 * r.threshold_distance +
        0.14 * r.basin_width +
        0.12 * r.regenerative_capacity +
        0.10 * r.ecological_memory +
        0.08 * r.connectivity -
        0.06 * r.disturbance_exposure -
        0.06 * r.slow_variable_pressure
    ) AS ecological_resilience_profile
FROM ecosystems e
JOIN stability_indicators s ON e.ecosystem_id = s.ecosystem_id
JOIN resilience_indicators r ON e.ecosystem_id = r.ecosystem_id;
