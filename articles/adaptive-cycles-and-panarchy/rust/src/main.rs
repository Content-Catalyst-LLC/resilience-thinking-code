fn release_risk_index(
    rigidity: f64,
    connectedness: f64,
    disturbance_exposure: f64,
    resilience: f64,
    novelty: f64,
) -> f64 {
    0.30 * rigidity
        + 0.24 * connectedness
        + 0.20 * disturbance_exposure
        + 0.16 * (1.0 - resilience)
        + 0.10 * (1.0 - novelty)
}

fn main() {
    let risk = release_risk_index(0.66, 0.78, 0.78, 0.38, 0.12);
    println!("system=Urban Stormwater System");
    println!("release_risk_index={:.4}", risk);
}
