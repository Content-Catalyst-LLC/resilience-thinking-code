fn local_value(
    liquidity: f64,
    workforce: f64,
    supply: f64,
    digital: f64,
    public_capacity: f64,
    community: f64,
    equity: f64,
    inequality: f64,
    implementation: f64,
) -> f64 {
    0.14 * liquidity
        + 0.14 * workforce
        + 0.12 * supply
        + 0.12 * digital
        + 0.14 * public_capacity
        + 0.15 * community
        + 0.16 * equity
        - 0.07 * inequality
        - 0.06 * implementation
}

fn main() {
    let score = local_value(9.2, 7.4, 7.2, 7.4, 8.3, 7.5, 8.6, 2.8, 3.0);
    println!("strategy=Emergency Microgrant and Liquidity Fund");
    println!("local_resilience_value={:.5}", score);
}
