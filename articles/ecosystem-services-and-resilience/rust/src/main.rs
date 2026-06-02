fn service_resilience_profile(
    current_flow: f64,
    ecological_condition: f64,
    functional_diversity: f64,
    functional_redundancy: f64,
    threshold_distance: f64,
    governance_capacity: f64,
    access_equity: f64,
    ecological_memory: f64,
    disturbance_exposure: f64,
) -> f64 {
    0.10 * current_flow
        + 0.17 * ecological_condition
        + 0.15 * functional_diversity
        + 0.14 * functional_redundancy
        + 0.15 * threshold_distance
        + 0.12 * governance_capacity
        + 0.09 * access_equity
        + 0.12 * ecological_memory
        - 0.12 * disturbance_exposure
}

fn main() {
    let profile = service_resilience_profile(0.72, 0.58, 0.52, 0.46, 0.48, 0.55, 0.52, 0.52, 0.70);
    println!("service=Pollination");
    println!("service_resilience_profile={:.4}", profile);
}
