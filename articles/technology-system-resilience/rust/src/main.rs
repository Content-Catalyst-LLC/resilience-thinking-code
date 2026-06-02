fn technology_value(
    architecture: f64,
    redundancy: f64,
    observability: f64,
    cybersecurity: f64,
    data_integrity: f64,
    maintainability: f64,
    governance: f64,
    human: f64,
    vendor: f64,
    debt: f64,
    implementation: f64,
) -> f64 {
    0.10 * architecture
        + 0.10 * redundancy
        + 0.10 * observability
        + 0.11 * cybersecurity
        + 0.11 * data_integrity
        + 0.11 * maintainability
        + 0.11 * governance
        + 0.11 * human
        + 0.10 * vendor
        - 0.03 * debt
        - 0.02 * implementation
}

fn main() {
    let score = technology_value(8.0, 8.9, 8.5, 9.2, 8.4, 8.1, 8.6, 8.0, 7.9, 3.2, 3.5);
    println!("strategy=Cyber Recovery and Tested Backup Program");
    println!("technology_resilience_value={:.5}", score);
}
