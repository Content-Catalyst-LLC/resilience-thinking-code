fn functional_resilience_profile(
    species_richness: f64,
    functional_diversity: f64,
    functional_redundancy: f64,
    response_diversity: f64,
    connectivity: f64,
    ecological_memory: f64,
    disturbance_exposure: f64,
) -> f64 {
    0.12 * species_richness
        + 0.19 * functional_diversity
        + 0.17 * functional_redundancy
        + 0.20 * response_diversity
        + 0.13 * connectivity
        + 0.16 * ecological_memory
        - 0.12 * disturbance_exposure
}

fn main() {
    let profile = functional_resilience_profile(0.72, 0.60, 0.52, 0.49, 0.54, 0.50, 0.72);
    println!("ecosystem_function=Pollination");
    println!("functional_resilience_profile={:.4}", profile);
}
