fn systems_thinking_score(feedback: f64, boundary: f64, leverage: f64, delay: f64) -> f64 {
    0.28 * feedback + 0.24 * boundary + 0.24 * leverage + 0.24 * delay
}

fn resilience_thinking_score(adaptive: f64, redundancy: f64, threshold: f64, buffer: f64, vulnerability: f64, exposure: f64) -> f64 {
    0.24 * adaptive + 0.20 * redundancy + 0.22 * threshold + 0.18 * buffer - 0.08 * vulnerability - 0.08 * exposure
}

fn main() {
    let systems = systems_thinking_score(0.72, 0.68, 0.64, 0.58);
    let resilience = resilience_thinking_score(0.70, 0.66, 0.74, 0.68, 0.52, 0.55);
    let combined = 0.5 * systems + 0.5 * resilience;

    println!("systems_thinking_score={:.4}", systems);
    println!("resilience_thinking_score={:.4}", resilience);
    println!("combined_system_resilience={:.4}", combined);
}
