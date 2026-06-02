fn governance_value(
    learning: f64,
    flexibility: f64,
    coordination: f64,
    knowledge: f64,
    legitimacy: f64,
    accountability: f64,
    equity: f64,
    burden: f64,
) -> f64 {
    0.15 * learning
        + 0.14 * flexibility
        + 0.14 * coordination
        + 0.14 * knowledge
        + 0.14 * legitimacy
        + 0.14 * accountability
        + 0.15 * equity
        - 0.02 * burden
}

fn main() {
    let score = governance_value(8.3, 7.6, 8.0, 9.1, 8.8, 8.3, 8.7, 3.1);
    println!("strategy=Community Knowledge Co-Production Platform");
    println!("adaptive_governance_value={:.5}", score);
}
