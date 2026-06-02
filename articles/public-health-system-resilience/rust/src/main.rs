fn resilience_value(
    prevention: f64,
    detection: f64,
    continuity: f64,
    workforce: f64,
    governance: f64,
    trust: f64,
    equity: f64,
    burden: f64,
) -> f64 {
    0.14 * prevention
        + 0.15 * detection
        + 0.15 * continuity
        + 0.14 * workforce
        + 0.14 * governance
        + 0.13 * trust
        + 0.13 * equity
        - 0.02 * burden
}

fn main() {
    let score = resilience_value(8.1, 8.0, 8.2, 8.3, 8.8, 8.7, 9.1, 3.0);
    println!("strategy=Equity-Centered Emergency Preparedness Framework");
    println!("resilience_value={:.5}", score);
}
