fn sigmoid(z: f64) -> f64 {
    1.0 / (1.0 + (-z).exp())
}

fn predict_failure(adaptive: f64, threshold: f64, learning: f64, redundancy: f64, modularity: f64, exposure: f64, sensitivity: f64, shock: f64) -> f64 {
    let protective = 0.24 * adaptive + 0.22 * threshold + 0.18 * learning + 0.18 * redundancy + 0.18 * modularity;
    let pressure = 0.32 * exposure + 0.28 * sensitivity + 0.40 * shock;
    sigmoid(-2.0 + 4.2 * pressure - 3.8 * protective)
}

fn main() {
    let p = predict_failure(0.38, 0.46, 0.33, 0.60, 0.43, 0.70, 0.58, 0.52);
    println!("predicted_failure_probability={:.4}", p);
    if p >= 0.65 {
        println!("band=high predicted resilience failure risk");
    } else if p >= 0.35 {
        println!("band=moderate predicted resilience failure risk");
    } else {
        println!("band=lower predicted resilience failure risk");
    }
}
