fn knowledge_value(
    participation: f64,
    diversity: f64,
    influence: f64,
    trust: f64,
    protection: f64,
    reciprocity: f64,
    accountability: f64,
    burden: f64,
) -> f64 {
    0.14 * participation
        + 0.14 * diversity
        + 0.15 * influence
        + 0.14 * trust
        + 0.14 * protection
        + 0.14 * reciprocity
        + 0.15 * accountability
        - 0.02 * burden
}

fn main() {
    let score = knowledge_value(9.0, 8.7, 9.1, 8.8, 8.5, 8.9, 9.0, 3.3);
    println!("strategy=Funded Community Resilience Advisory Council");
    println!("knowledge_integration_value={:.5}", score);
}
