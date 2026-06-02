fn resilience_value(
    social: f64,
    institution: f64,
    access: f64,
    economy: f64,
    information: f64,
    adaptive: f64,
    equity: f64,
    burden: f64,
) -> f64 {
    0.14 * social
        + 0.14 * institution
        + 0.14 * access
        + 0.13 * economy
        + 0.13 * information
        + 0.15 * adaptive
        + 0.15 * equity
        - 0.02 * burden
}

fn main() {
    let score = resilience_value(8.4, 8.3, 7.4, 7.8, 7.8, 8.6, 8.8, 3.1);
    println!("strategy=Inclusive Community Governance and Adaptation Forum");
    println!("resilience_value={:.5}", score);
}
