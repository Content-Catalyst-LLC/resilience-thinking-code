fn resilience_value(
    redundancy: f64,
    diversity: f64,
    response_diversity: f64,
    coordination_capacity: f64,
    justice_contribution: f64,
    maintenance_reliability: f64,
    common_mode_risk: f64,
) -> f64 {
    0.22 * redundancy
        + 0.18 * diversity
        + 0.22 * response_diversity
        + 0.13 * coordination_capacity
        + 0.10 * justice_contribution
        + 0.07 * maintenance_reliability
        - 0.08 * common_mode_risk
}

fn main() {
    let score = resilience_value(8.8, 7.4, 7.8, 7.6, 7.2, 7.5, 3.8);
    println!("strategy=Distributed Backup Infrastructure Network");
    println!("resilience_value={:.5}", score);
}
