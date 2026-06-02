fn resilience_value(
    exposure: f64,
    vulnerability: f64,
    service: f64,
    adaptive: f64,
    ecology: f64,
    equity: f64,
    maladaptation: f64,
) -> f64 {
    0.16 * exposure
        + 0.17 * vulnerability
        + 0.17 * service
        + 0.15 * adaptive
        + 0.14 * ecology
        + 0.15 * equity
        - 0.06 * maladaptation
}

fn main() {
    let score = resilience_value(7.5, 8.9, 7.7, 8.4, 7.5, 9.1, 2.5);
    println!("strategy=Anti-Displacement Climate Adaptation Framework");
    println!("resilience_value={:.5}", score);
}
