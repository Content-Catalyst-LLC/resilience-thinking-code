use std::env;

fn resilience_profile(adaptive: f64, threshold: f64, learning: f64, modularity: f64, redundancy: f64, exposure: f64, sensitivity: f64) -> f64 {
    0.24 * adaptive
        + 0.20 * threshold
        + 0.18 * learning
        + 0.14 * modularity
        + 0.14 * redundancy
        - 0.05 * exposure
        - 0.05 * sensitivity
}

fn flag_margin(margin: f64) -> &'static str {
    if margin < 0.15 {
        "high threshold risk"
    } else if margin < 0.30 {
        "moderate threshold risk"
    } else {
        "lower threshold risk"
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let adaptive = args.get(1).and_then(|x| x.parse().ok()).unwrap_or(0.70);
    let threshold = args.get(2).and_then(|x| x.parse().ok()).unwrap_or(0.60);
    let learning = args.get(3).and_then(|x| x.parse().ok()).unwrap_or(0.65);
    let modularity = args.get(4).and_then(|x| x.parse().ok()).unwrap_or(0.55);
    let redundancy = args.get(5).and_then(|x| x.parse().ok()).unwrap_or(0.60);
    let exposure = args.get(6).and_then(|x| x.parse().ok()).unwrap_or(0.58);
    let sensitivity = args.get(7).and_then(|x| x.parse().ok()).unwrap_or(0.52);

    let profile = resilience_profile(adaptive, threshold, learning, modularity, redundancy, exposure, sensitivity);
    let pressure = 0.55 * exposure + 0.45 * sensitivity;
    let margin = profile + threshold - pressure;

    println!("resilience_profile={:.4}", profile);
    println!("risk_pressure={:.4}", pressure);
    println!("viability_margin={:.4}", margin);
    println!("risk_flag={}", flag_margin(margin));
}
