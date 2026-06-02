fn landscape_resilience_profile(
    heterogeneity: f64,
    connectivity: f64,
    refugia: f64,
    memory: f64,
    governance: f64,
    disturbance: f64,
    fragmentation: f64,
    social_vulnerability: f64,
) -> f64 {
    0.17 * heterogeneity
        + 0.15 * connectivity
        + 0.17 * refugia
        + 0.17 * memory
        + 0.14 * governance
        - 0.11 * disturbance
        - 0.06 * fragmentation
        - 0.06 * social_vulnerability
}

fn main() {
    let profile = landscape_resilience_profile(0.68, 0.60, 0.57, 0.62, 0.58, 0.78, 0.52, 0.54);
    println!("landscape_type=Fire-Prone Forest Mosaic");
    println!("landscape_resilience_profile={:.4}", profile);
}
