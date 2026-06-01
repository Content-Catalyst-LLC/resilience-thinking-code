fn influence_score(conceptual_scope: f64, governance_relevance: f64, system_complexity: f64, justice_relevance: f64) -> f64 {
    0.35 * conceptual_scope
        + 0.25 * governance_relevance
        + 0.25 * system_complexity
        + 0.15 * justice_relevance
}

fn main() {
    let score = influence_score(0.96, 0.96, 0.96, 0.94);
    println!("phase=Critical Resilience and Justice");
    println!("stylized_influence_score={:.4}", score);
}
