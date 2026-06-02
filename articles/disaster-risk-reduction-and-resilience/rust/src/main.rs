fn drr_value(
    hazard_reduction: f64,
    exposure_reduction: f64,
    vulnerability_reduction: f64,
    capacity_enhancement: f64,
    justice_protection: f64,
    maladaptation_risk: f64,
) -> f64 {
    0.17 * hazard_reduction
        + 0.18 * exposure_reduction
        + 0.18 * vulnerability_reduction
        + 0.17 * capacity_enhancement
        + 0.18 * justice_protection
        - 0.12 * maladaptation_risk
}

fn main() {
    let score = drr_value(6.7, 7.4, 8.9, 8.3, 9.0, 2.4);
    println!("strategy=Equitable Recovery and Housing Protection Program");
    println!("drr_value={:.5}", score);
}
