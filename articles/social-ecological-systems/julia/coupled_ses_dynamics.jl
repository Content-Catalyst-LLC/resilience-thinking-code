# Coupled social-ecological systems dynamics
#
# Run:
#   julia julia/coupled_ses_dynamics.jl

using Printf

function simulate_ses(; steps=90, initial_ecology=0.75, initial_social_pressure=0.55,
    governance=0.60, livelihood_pressure=0.55, climate_pressure=0.58, market_shock=0.38)

    ecology = initial_ecology
    social_pressure = initial_social_pressure

    r = 0.08
    k = 1.0
    q = 0.10

    println("time,ecology,social_pressure,extraction,resilience_margin,threshold_flag")

    for t in 1:steps
        extraction = q * social_pressure * ecology
        ecological_growth = r * ecology * (1 - ecology / k)
        climate_effect = 0.022 * climate_pressure
        governance_repair = 0.017 * governance

        ecology = ecology + ecological_growth - extraction - climate_effect + governance_repair
        ecology = max(0.01, min(1.20, ecology))

        market_pulse = (t in [20, 42, 68]) ? 0.035 * market_shock : 0.0
        social_pressure = social_pressure + 0.050 * livelihood_pressure + 0.028 * (1 - governance) + market_pulse - 0.043 * ecology
        social_pressure = max(0.05, min(1.20, social_pressure))

        margin = ecology + governance + 0.35 * (1 - livelihood_pressure) - social_pressure - 0.35 * climate_pressure
        flag = margin < 0.20 ? "threshold risk" : "viable margin"

        @printf("%d,%.5f,%.5f,%.5f,%.5f,%s\n", t, ecology, social_pressure, extraction, margin, flag)
    end
end

simulate_ses()
