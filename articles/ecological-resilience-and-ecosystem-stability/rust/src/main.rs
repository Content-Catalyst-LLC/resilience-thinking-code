fn main() {
    let stability = 0.80;
    let resilience = 0.11*0.80 + 0.13*0.52 + 0.13*0.50 + 0.13*0.46 + 0.16*0.34 + 0.14*0.38 + 0.12*0.45 + 0.10*0.42 + 0.08*0.40 - 0.06*0.72 - 0.06*0.78;
    println!("ecosystem_type=Shallow Lake");
    println!("stability_score={:.4}", stability);
    println!("ecological_resilience_profile={:.4}", resilience);
    println!("stability_resilience_gap={:.4}", resilience - stability);
}
