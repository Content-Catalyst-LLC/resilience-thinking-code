fn transformation_readiness(
    adaptive_support: f64,
    transformability: f64,
    governance_readiness: f64,
    justice_contribution: f64,
    ecological_viability: f64,
    legitimacy: f64,
    resource_feasibility: f64,
    structural_risk: f64,
) -> f64 {
    0.18 * adaptive_support
        + 0.20 * transformability
        + 0.18 * governance_readiness
        + 0.16 * justice_contribution
        + 0.14 * ecological_viability
        + 0.08 * legitimacy
        + 0.06 * resource_feasibility
        - 0.10 * structural_risk
}

fn main() {
    let score = transformation_readiness(8.3, 8.5, 7.8, 8.4, 8.1, 7.8, 7.0, 4.0);
    println!("pathway=Climate-Resilient Urban Redesign");
    println!("transformation_readiness={:.5}", score);
}
