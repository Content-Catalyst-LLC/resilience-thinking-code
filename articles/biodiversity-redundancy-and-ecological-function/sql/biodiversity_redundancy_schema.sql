-- Biodiversity, Redundancy, and Ecological Function schema
-- Supports species, traits, functions, habitats, disturbances, scenarios, model runs, and outputs.

CREATE TABLE IF NOT EXISTS habitats (
    habitat_id TEXT PRIMARY KEY,
    habitat_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS ecological_functions (
    function_id TEXT PRIMARY KEY,
    function_name TEXT NOT NULL,
    critical_role TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS species (
    species_id TEXT PRIMARY KEY,
    species_name TEXT NOT NULL,
    functional_group TEXT NOT NULL,
    habitat_affinity TEXT
);

CREATE TABLE IF NOT EXISTS species_traits (
    trait_id TEXT PRIMARY KEY,
    species_id TEXT NOT NULL REFERENCES species(species_id),
    function_id TEXT REFERENCES ecological_functions(function_id),
    trait_contribution REAL NOT NULL CHECK (trait_contribution BETWEEN 0 AND 1.5),
    disturbance_sensitivity REAL NOT NULL CHECK (disturbance_sensitivity BETWEEN 0 AND 1),
    recovery_capacity REAL NOT NULL CHECK (recovery_capacity BETWEEN 0 AND 1),
    initial_abundance REAL NOT NULL CHECK (initial_abundance BETWEEN 0 AND 1.5)
);

CREATE TABLE IF NOT EXISTS function_profiles (
    profile_id TEXT PRIMARY KEY,
    function_id TEXT NOT NULL REFERENCES ecological_functions(function_id),
    species_richness REAL NOT NULL CHECK (species_richness BETWEEN 0 AND 1),
    functional_diversity REAL NOT NULL CHECK (functional_diversity BETWEEN 0 AND 1),
    functional_redundancy REAL NOT NULL CHECK (functional_redundancy BETWEEN 0 AND 1),
    response_diversity REAL NOT NULL CHECK (response_diversity BETWEEN 0 AND 1),
    connectivity REAL NOT NULL CHECK (connectivity BETWEEN 0 AND 1),
    ecological_memory REAL NOT NULL CHECK (ecological_memory BETWEEN 0 AND 1),
    disturbance_exposure REAL NOT NULL CHECK (disturbance_exposure BETWEEN 0 AND 1)
);

CREATE TABLE IF NOT EXISTS disturbance_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    disturbance_pressure REAL NOT NULL CHECK (disturbance_pressure BETWEEN 0 AND 1),
    shock_intensity REAL NOT NULL CHECK (shock_intensity BETWEEN 0 AND 1),
    shock_frequency INTEGER NOT NULL,
    recovery_support REAL NOT NULL CHECK (recovery_support BETWEEN 0 AND 1),
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

CREATE VIEW IF NOT EXISTS function_resilience_profile_view AS
SELECT
    ef.function_id,
    ef.function_name,
    ef.critical_role,
    fp.species_richness,
    fp.functional_diversity,
    fp.functional_redundancy,
    fp.response_diversity,
    fp.connectivity,
    fp.ecological_memory,
    fp.disturbance_exposure,
    (
        0.12 * fp.species_richness +
        0.19 * fp.functional_diversity +
        0.17 * fp.functional_redundancy +
        0.20 * fp.response_diversity +
        0.13 * fp.connectivity +
        0.16 * fp.ecological_memory -
        0.12 * fp.disturbance_exposure
    ) AS functional_resilience_profile,
    (
        0.24 * (1 - fp.response_diversity) +
        0.22 * (1 - fp.functional_redundancy) +
        0.18 * fp.disturbance_exposure +
        0.14 * (1 - fp.connectivity) +
        0.12 * (1 - fp.ecological_memory) +
        0.10 * (1 - fp.functional_diversity)
    ) AS function_threshold_risk_index
FROM ecological_functions ef
JOIN function_profiles fp ON ef.function_id = fp.function_id;
