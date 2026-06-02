fn slack_value(
    financial: f64,
    workforce: f64,
    operational: f64,
    knowledge: f64,
    network: f64,
    governance: f64,
    ethics: f64,
    burden: f64,
    implementation: f64,
) -> f64 {
    0.13 * financial
        + 0.14 * workforce
        + 0.13 * operational
        + 0.13 * knowledge
        + 0.13 * network
        + 0.14 * governance
        + 0.13 * ethics
        - 0.04 * burden
        - 0.03 * implementation
}

fn main() {
    let score = slack_value(7.8, 8.1, 8.0, 8.4, 8.1, 9.1, 8.4, 2.8, 3.2);
    println!("portfolio=Adaptive Governance and Emergency Decision Space");
    println!("slack_resilience_value={:.5}", score);
}
