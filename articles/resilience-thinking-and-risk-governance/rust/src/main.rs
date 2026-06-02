fn risk_pressure(hazard: f64, exposure: f64, vulnerability: f64, adaptive: f64) -> f64 {
    hazard * exposure * vulnerability * (1.0 - 0.55 * adaptive)
}

fn governance_capacity(trust: f64, participation: f64, knowledge: f64, coordination: f64, transparency: f64, accountability: f64) -> f64 {
    0.18 * trust + 0.17 * participation + 0.17 * knowledge + 0.18 * coordination + 0.15 * transparency + 0.15 * accountability
}

fn main() {
    let rp = risk_pressure(0.74, 0.78, 0.64, 0.58);
    let gc = governance_capacity(0.46, 0.42, 0.50, 0.48, 0.44, 0.46);
    let margin = 0.55 + 0.58 + 0.52 + gc - rp - 0.64;

    println!("risk_pressure={:.4}", rp);
    println!("governance_capacity={:.4}", gc);
    println!("resilience_margin={:.4}", margin);
}
