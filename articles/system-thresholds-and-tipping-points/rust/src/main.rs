fn threshold_risk_score(
    pressure: f64,
    feedback_strength: f64,
    disturbance_load: f64,
    exposure: f64,
    adaptive_capacity: f64,
    system_memory: f64,
    recovery_speed: f64,
) -> f64 {
    0.24 * pressure
        + 0.22 * feedback_strength
        + 0.18 * disturbance_load
        + 0.14 * exposure
        - 0.10 * adaptive_capacity
        - 0.07 * system_memory
        - 0.05 * recovery_speed
}

fn main() {
    let risk = threshold_risk_score(0.74, 0.66, 0.62, 0.78, 0.44, 0.46, 0.36);
    println!("system=Urban Stormwater Network");
    println!("threshold_risk_score={:.4}", risk);
}
