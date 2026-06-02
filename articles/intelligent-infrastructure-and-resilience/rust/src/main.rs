fn infrastructure_value(
    monitoring: f64,
    maintenance: f64,
    cyber: f64,
    twin: f64,
    redundancy: f64,
    climate: f64,
    governance: f64,
    equity: f64,
    ecology: f64,
    fragility: f64,
    implementation: f64,
) -> f64 {
    0.10 * monitoring
        + 0.11 * maintenance
        + 0.11 * cyber
        + 0.10 * twin
        + 0.11 * redundancy
        + 0.11 * climate
        + 0.12 * governance
        + 0.12 * equity
        + 0.10 * ecology
        - 0.04 * fragility
        - 0.04 * implementation
}

fn main() {
    let score = infrastructure_value(8.5, 9.3, 8.2, 8.6, 8.4, 8.4, 8.4, 8.2, 8.0, 2.8, 3.8);
    println!("strategy=Predictive Maintenance and Asset Renewal");
    println!("infrastructure_resilience_value={:.5}", score);
}
