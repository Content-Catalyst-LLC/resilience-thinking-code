fn financial_value(
    capital: f64,
    liquidity: f64,
    infrastructure: f64,
    governance: f64,
    inclusion: f64,
    exposure: f64,
    burden: f64,
) -> f64 {
    0.16 * capital
        + 0.16 * liquidity
        + 0.16 * infrastructure
        + 0.16 * governance
        + 0.16 * inclusion
        - 0.12 * exposure
        - 0.08 * burden
}

fn main() {
    let score = financial_value(8.9, 8.8, 7.6, 8.3, 7.4, 3.9, 3.2);
    println!("strategy=Higher Capital and Liquidity Buffers");
    println!("financial_resilience_value={:.5}", score);
}
