fn metric_value(
    resistance: f64,
    recovery: f64,
    adaptive: f64,
    buffer: f64,
    justice: f64,
    data_quality: f64,
    threshold_blindness: f64,
) -> f64 {
    0.16 * resistance
        + 0.16 * recovery
        + 0.16 * adaptive
        + 0.15 * buffer
        + 0.13 * justice
        + 0.10 * data_quality
        - 0.14 * threshold_blindness
}

fn main() {
    let score = metric_value(8.5, 8.4, 8.7, 8.2, 8.1, 8.5, 3.2);
    println!("framework=Hybrid Structural and Dynamic Assessment");
    println!("metric_value={:.5}", score);
}
