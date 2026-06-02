fn resilience_value(
    legitimacy: f64,
    capacity: f64,
    flexibility: f64,
    coordination: f64,
    learning: f64,
    accountability: f64,
    equity: f64,
    burden: f64,
) -> f64 {
    0.14 * legitimacy
        + 0.14 * capacity
        + 0.13 * flexibility
        + 0.14 * coordination
        + 0.14 * learning
        + 0.14 * accountability
        + 0.15 * equity
        - 0.02 * burden
}

fn main() {
    let score = resilience_value(8.3, 7.5, 7.8, 7.6, 7.9, 8.9, 9.1, 3.0);
    println!("strategy=Equity and Access Accountability Review");
    println!("resilience_value={:.5}", score);
}
