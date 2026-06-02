fn resilience_value(
    resistance: f64,
    recovery: f64,
    adaptation: f64,
    transformation: f64,
    equity: f64,
    institutions: f64,
    burden: f64,
) -> f64 {
    0.16 * resistance
        + 0.16 * recovery
        + 0.17 * adaptation
        + 0.17 * transformation
        + 0.17 * equity
        + 0.17 * institutions
        - 0.02 * burden
}

fn main() {
    let score = resilience_value(8.1, 8.5, 8.1, 7.9, 8.7, 8.2, 2.9);
    println!("strategy=Community Finance and Small Business Continuity Fund");
    println!("economic_resilience_value={:.5}", score);
}
