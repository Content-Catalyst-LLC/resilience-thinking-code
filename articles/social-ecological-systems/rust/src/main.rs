fn ses_resilience_profile(
    ecological: f64,
    governance: f64,
    livelihood: f64,
    infrastructure: f64,
    knowledge: f64,
    trust: f64,
    adaptive: f64,
    market: f64,
    climate: f64,
    dependency: f64,
) -> f64 {
    0.18 * ecological
        + 0.16 * governance
        + 0.12 * livelihood
        + 0.12 * infrastructure
        + 0.13 * knowledge
        + 0.11 * trust
        + 0.10 * adaptive
        - 0.09 * market
        - 0.07 * climate
        - 0.02 * dependency
}

fn main() {
    let profile = ses_resilience_profile(0.68, 0.61, 0.48, 0.46, 0.57, 0.54, 0.55, 0.78, 0.62, 0.82);
    println!("system_type=Fishery");
    println!("ses_resilience_profile={:.4}", profile);
}
