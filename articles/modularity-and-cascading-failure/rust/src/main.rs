fn containment_value(
    modularity: f64,
    redundancy: f64,
    dependency_mapping: f64,
    isolation_capacity: f64,
    coordination_readiness: f64,
    justice_protection: f64,
    common_mode_risk: f64,
) -> f64 {
    0.18 * modularity
        + 0.16 * redundancy
        + 0.16 * dependency_mapping
        + 0.18 * isolation_capacity
        + 0.14 * coordination_readiness
        + 0.10 * justice_protection
        - 0.08 * common_mode_risk
}

fn main() {
    let score = containment_value(8.7, 8.4, 7.6, 8.8, 7.6, 7.3, 3.5);
    println!("strategy=Microgrid and Critical Service Islanding");
    println!("containment_value={:.5}", score);
}
