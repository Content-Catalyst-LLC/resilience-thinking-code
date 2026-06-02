-- Transformation in Complex Systems schema
-- Supports transformation pathways, criteria, scenarios, model runs, and outputs.

CREATE TABLE IF NOT EXISTS transformation_pathways (
    pathway_id TEXT PRIMARY KEY,
    pathway TEXT NOT NULL,
    system_domain TEXT NOT NULL,
    adaptive_support REAL NOT NULL,
    transformability REAL NOT NULL,
    governance_readiness REAL NOT NULL,
    justice_contribution REAL NOT NULL,
    ecological_viability REAL NOT NULL,
    legitimacy REAL NOT NULL,
    resource_feasibility REAL NOT NULL,
    structural_risk REAL NOT NULL,
    critical_function TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS transformation_scenarios (
    scenario TEXT PRIMARY KEY,
    adaptive_support_weight REAL NOT NULL,
    transformability_weight REAL NOT NULL,
    governance_readiness_weight REAL NOT NULL,
    justice_contribution_weight REAL NOT NULL,
    ecological_viability_weight REAL NOT NULL,
    legitimacy_weight REAL NOT NULL,
    resource_feasibility_weight REAL NOT NULL,
    structural_risk_weight REAL NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS transformation_criteria (
    criterion TEXT PRIMARY KEY,
    definition TEXT NOT NULL,
    measurement_note TEXT NOT NULL
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

CREATE VIEW IF NOT EXISTS transformation_readiness_view AS
SELECT
    pathway_id,
    pathway,
    system_domain,
    critical_function,
    adaptive_support,
    transformability,
    governance_readiness,
    justice_contribution,
    ecological_viability,
    legitimacy,
    resource_feasibility,
    structural_risk,
    (
        0.18 * adaptive_support +
        0.20 * transformability +
        0.18 * governance_readiness +
        0.16 * justice_contribution +
        0.14 * ecological_viability +
        0.08 * legitimacy +
        0.06 * resource_feasibility -
        0.10 * structural_risk
    ) AS transformation_readiness
FROM transformation_pathways;

CREATE VIEW IF NOT EXISTS balanced_pathway_value_view AS
SELECT
    p.pathway_id,
    p.pathway,
    p.system_domain,
    p.critical_function,
    (
        0.16 * p.adaptive_support +
        0.22 * p.transformability +
        0.16 * p.governance_readiness +
        0.15 * p.justice_contribution +
        0.13 * p.ecological_viability +
        0.08 * p.legitimacy +
        0.05 * p.resource_feasibility -
        0.05 * p.structural_risk
    ) AS balanced_transformation_value
FROM transformation_pathways p;
