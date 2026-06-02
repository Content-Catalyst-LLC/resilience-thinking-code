fn resilience_value(
    service_continuity: f64,
    redundancy: f64,
    recovery_speed: f64,
    adaptive_capacity: f64,
    equity_protection: f64,
    cascading_exposure: f64,
) -> f64 {
    0.22 * service_continuity
        + 0.20 * redundancy
        + 0.18 * recovery_speed
        + 0.16 * adaptive_capacity
        + 0.16 * equity_protection
        - 0.08 * cascading_exposure
}

fn main() {
    let score = resilience_value(8.4, 8.0, 8.6, 8.1, 8.9, 3.4);
    println!("strategy=Equitable Critical Service Restoration Program");
    println!("resilience_value={:.5}", score);
}
