fn climate_resilience_value(
    exposure_reduction: f64,
    vulnerability_reduction: f64,
    adaptive_capacity: f64,
    recovery_capacity: f64,
    transformative_capacity: f64,
    justice_protection: f64,
    maladaptation_risk: f64,
) -> f64 {
    0.16 * exposure_reduction
        + 0.16 * vulnerability_reduction
        + 0.16 * adaptive_capacity
        + 0.15 * recovery_capacity
        + 0.15 * transformative_capacity
        + 0.14 * justice_protection
        - 0.08 * maladaptation_risk
}

fn main() {
    let score = climate_resilience_value(8.3, 8.5, 8.2, 7.9, 8.4, 8.8, 2.8);
    println!("strategy=Community-Led Floodplain Adaptation");
    println!("climate_resilience_value={:.5}", score);
}
