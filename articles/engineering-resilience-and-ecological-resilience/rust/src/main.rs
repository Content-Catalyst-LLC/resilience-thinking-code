fn engineering_resilience(return_speed: f64, reliability: f64, repair: f64, backup: f64, continuity: f64) -> f64 {
    0.28 * return_speed + 0.24 * reliability + 0.18 * repair + 0.15 * backup + 0.15 * continuity
}

fn ecological_resilience(threshold: f64, basin: f64, adaptive: f64, diversity: f64, redundancy: f64, modularity: f64, exposure: f64, sensitivity: f64) -> f64 {
    0.20 * threshold + 0.18 * basin + 0.18 * adaptive + 0.15 * diversity + 0.13 * redundancy + 0.10 * modularity - 0.08 * exposure - 0.08 * sensitivity
}

fn main() {
    let eng = engineering_resilience(0.88, 0.84, 0.78, 0.74, 0.86);
    let eco = ecological_resilience(0.48, 0.50, 0.44, 0.38, 0.64, 0.55, 0.62, 0.58);
    println!("engineering_resilience={:.4}", eng);
    println!("ecological_resilience={:.4}", eco);
    println!("resilience_gap={:.4}", eco - eng);
}
