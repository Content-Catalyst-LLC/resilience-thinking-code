fn regime_risk_score(
    pressure: f64,
    feedback_strength: f64,
    variance_signal: f64,
    autocorr_signal: f64,
    exposure: f64,
    recovery_speed: f64,
    adaptive_capacity: f64,
    system_memory: f64,
    monitoring_quality: f64,
    justice_visibility: f64,
) -> f64 {
    0.18 * pressure
        + 0.17 * feedback_strength
        + 0.15 * variance_signal
        + 0.15 * autocorr_signal
        + 0.12 * exposure
        - 0.08 * recovery_speed
        - 0.06 * adaptive_capacity
        - 0.04 * system_memory
        - 0.03 * monitoring_quality
        - 0.02 * justice_visibility
}

fn main() {
    let score = regime_risk_score(0.74, 0.66, 0.62, 0.64, 0.78, 0.36, 0.44, 0.46, 0.52, 0.46);
    println!("system=Urban Stormwater Service Regime");
    println!("regime_risk_score={:.5}", score);
}
