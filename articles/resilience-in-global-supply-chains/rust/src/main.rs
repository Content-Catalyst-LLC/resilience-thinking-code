fn supply_chain_value(
    redundancy: f64,
    flexibility: f64,
    visibility: f64,
    coordination: f64,
    adaptation: f64,
    equity: f64,
    infrastructure: f64,
    exposure: f64,
    burden: f64,
) -> f64 {
    0.13 * redundancy
        + 0.13 * flexibility
        + 0.13 * visibility
        + 0.13 * coordination
        + 0.13 * adaptation
        + 0.13 * equity
        + 0.13 * infrastructure
        - 0.06 * exposure
        - 0.03 * burden
}

fn main() {
    let score = supply_chain_value(8.1, 8.8, 8.0, 8.2, 8.5, 7.8, 8.5, 4.0, 3.4);
    println!("strategy=Multi-Route Logistics and Chokepoint Redesign");
    println!("supply_chain_resilience_value={:.5}", score);
}
