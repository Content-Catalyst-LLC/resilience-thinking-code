fn adaptive_learning_value(
    monitoring_quality: f64,
    memory_retention: f64,
    feedback_use: f64,
    governance_flexibility: f64,
    community_knowledge: f64,
    justice_protection: f64,
    implementation_reliability: f64,
    forgetting_pressure: f64,
) -> f64 {
    0.15 * monitoring_quality
        + 0.15 * memory_retention
        + 0.17 * feedback_use
        + 0.14 * governance_flexibility
        + 0.12 * community_knowledge
        + 0.11 * justice_protection
        + 0.09 * implementation_reliability
        - 0.07 * forgetting_pressure
}

fn main() {
    let score = adaptive_learning_value(8.1, 7.9, 8.8, 8.7, 7.9, 8.0, 8.0, 3.1);
    println!("strategy=Adaptive Governance Decision-Trigger Framework");
    println!("adaptive_learning_value={:.5}", score);
}
