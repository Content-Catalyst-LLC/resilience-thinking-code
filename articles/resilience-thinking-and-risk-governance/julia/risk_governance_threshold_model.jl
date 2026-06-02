# Risk-governance threshold model
#
# Run:
#   julia julia/risk_governance_threshold_model.jl

using Printf

function risk_pressure(hazard, exposure, vulnerability, adaptive)
    return hazard * exposure * vulnerability * (1.0 - 0.55 * adaptive)
end

function governance_capacity(trust, participation, knowledge, coordination, transparency, accountability)
    return 0.18*trust + 0.17*participation + 0.17*knowledge + 0.18*coordination + 0.15*transparency + 0.15*accountability
end

function resilience_margin(buffer, adaptive, learning, governance, risk, vulnerability)
    return buffer + adaptive + learning + governance - risk - vulnerability
end

systems = [
    ("Coastal City", 0.74, 0.78, 0.64, 0.55, 0.58, 0.52, 0.46, 0.42, 0.50, 0.48, 0.44, 0.46),
    ("Watershed Governance", 0.58, 0.60, 0.52, 0.68, 0.70, 0.72, 0.64, 0.70, 0.74, 0.68, 0.66, 0.64),
    ("Community Adaptation Network", 0.55, 0.57, 0.48, 0.70, 0.78, 0.80, 0.76, 0.82, 0.78, 0.74, 0.70, 0.76)
]

println("system_type,risk_pressure,governance_capacity,resilience_margin")
for s in systems
    name, hazard, exposure, vulnerability, buffer, adaptive, learning, trust, participation, knowledge, coordination, transparency, accountability = s
    rp = risk_pressure(hazard, exposure, vulnerability, adaptive)
    gc = governance_capacity(trust, participation, knowledge, coordination, transparency, accountability)
    rm = resilience_margin(buffer, adaptive, learning, gc, rp, vulnerability)
    @printf("%s,%.5f,%.5f,%.5f\n", name, rp, gc, rm)
end
