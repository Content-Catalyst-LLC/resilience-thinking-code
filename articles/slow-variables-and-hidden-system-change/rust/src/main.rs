fn hidden_risk_score(
    maintenance_backlog: f64,
    climate_pressure: f64,
    exposure: f64,
    public_trust: f64,
    ecological_memory: f64,
    adaptive_capacity: f64,
    monitoring_quality: f64,
    justice_visibility: f64,
) -> f64 {
    0.20 * maintenance_backlog
        + 0.18 * climate_pressure
        + 0.16 * exposure
        + 0.12 * (1.0 - public_trust)
        + 0.12 * (1.0 - ecological_memory)
        + 0.10 * (1.0 - adaptive_capacity)
        + 0.07 * (1.0 - monitoring_quality)
        + 0.05 * (1.0 - justice_visibility)
}

fn main() {
    let score = hidden_risk_score(0.58, 0.62, 0.74, 0.52, 0.40, 0.48, 0.54, 0.48);
    println!("system=Urban Stormwater System");
    println!("hidden_risk_score={:.5}", score);
}
