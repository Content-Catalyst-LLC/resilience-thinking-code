fn dashboard_value(
    indicator_coverage: f64,
    threshold_sensitivity: f64,
    justice_visibility: f64,
    uncertainty_transparency: f64,
    decision_trigger_clarity: f64,
    learning_integration: f64,
    dashboard_risk: f64,
) -> f64 {
    0.15 * indicator_coverage
        + 0.17 * threshold_sensitivity
        + 0.16 * justice_visibility
        + 0.14 * uncertainty_transparency
        + 0.16 * decision_trigger_clarity
        + 0.14 * learning_integration
        - 0.08 * dashboard_risk
}

fn main() {
    let score = dashboard_value(8.4, 8.5, 8.1, 8.5, 9.0, 8.9, 3.6);
    println!("dashboard=Adaptive Learning and Decision-Trigger Dashboard");
    println!("dashboard_value={:.5}", score);
}
