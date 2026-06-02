fn feedback_risk_score(
    reinforcing_gain: f64,
    disturbance_load: f64,
    delay_steps_scaled: f64,
    balancing_strength: f64,
    adaptive_capacity: f64,
    signal_quality: f64,
    system_memory: f64,
    justice_visibility: f64,
) -> f64 {
    0.24 * reinforcing_gain
        + 0.20 * disturbance_load
        + 0.18 * delay_steps_scaled
        - 0.16 * balancing_strength
        - 0.10 * adaptive_capacity
        - 0.07 * signal_quality
        - 0.03 * system_memory
        - 0.02 * justice_visibility
}

fn main() {
    let score = feedback_risk_score(0.090, 0.72, 0.90, 0.090, 0.44, 0.46, 0.50, 0.44);
    println!("system=Fire Suppression Fuel Loop");
    println!("feedback_risk_score={:.5}", score);
}
