fn resilience_value(
    availability: f64,
    access: f64,
    stability: f64,
    quality: f64,
    adaptive_capacity: f64,
    equity_protection: f64,
    depletion_risk: f64,
) -> f64 {
    0.17 * availability
        + 0.17 * access
        + 0.16 * stability
        + 0.14 * quality
        + 0.16 * adaptive_capacity
        + 0.14 * equity_protection
        - 0.06 * depletion_risk
}

fn main() {
    let score = resilience_value(7.6, 8.8, 7.7, 8.1, 8.7, 8.9, 2.8);
    println!("strategy=Community Water Governance and Access Reform");
    println!("resilience_value={:.5}", score);
}
