fn viability_value(
    resilience: f64,
    ecology: f64,
    inclusion: f64,
    economy: f64,
    governance: f64,
    adaptive: f64,
    pressure: f64,
    burden: f64,
) -> f64 {
    0.18 * resilience
        + 0.17 * ecology
        + 0.16 * inclusion
        + 0.14 * economy
        + 0.14 * governance
        + 0.15 * adaptive
        - 0.04 * pressure
        - 0.02 * burden
}

fn main() {
    let score = viability_value(8.4, 9.0, 8.2, 7.9, 8.0, 8.7, 3.5, 3.2);
    println!("pathway=Ecosystem Restoration and Livelihood Diversification");
    println!("viability_value={:.5}", score);
}
