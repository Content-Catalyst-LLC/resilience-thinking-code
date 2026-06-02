fn adaptive_capacity(
    learning: f64,
    flexibility: f64,
    diversity: f64,
    governance: f64,
    slack: f64,
    trust: f64,
    rigidity: f64,
) -> f64 {
    0.18 * learning
        + 0.18 * flexibility
        + 0.17 * diversity
        + 0.17 * governance
        + 0.14 * slack
        + 0.16 * trust
        - 0.12 * rigidity
}

fn main() {
    let score = adaptive_capacity(0.60, 0.57, 0.64, 0.58, 0.50, 0.57, 0.55);
    println!("system_type=Regional Food System");
    println!("adaptive_capacity={:.4}", score);
}
