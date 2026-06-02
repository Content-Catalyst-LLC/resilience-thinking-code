# Food and water resilience pathway example
#
# Run:
#   julia julia/food_water_resilience_pathway_example.jl

using Printf

strategies = [
    ("Watershed Restoration and Recharge Program", 8.3, 7.4, 7.9, 8.6, 8.5, 7.7, 2.7),
    ("Community Water Governance and Access Reform", 7.6, 8.8, 7.7, 8.1, 8.7, 8.9, 2.8),
    ("Safe Water Treatment and Sanitation Resilience Plan", 7.8, 8.5, 8.1, 8.9, 8.0, 8.6, 3.0)
]

function resilience_value(availability, access, stability, quality, adaptive, equity, depletion)
    return 0.17 * availability +
           0.17 * access +
           0.16 * stability +
           0.14 * quality +
           0.16 * adaptive +
           0.14 * equity -
           0.06 * depletion
end

println("strategy,resilience_value,equity_adjusted_value,resource_depletion_risk")

for s in strategies
    name, availability, access, stability, quality, adaptive, equity, depletion = s
    value = resilience_value(availability, access, stability, quality, adaptive, equity, depletion)
    equity_adjusted = value * (0.72 + 0.028 * equity)
    @printf("%s,%.5f,%.5f,%.2f\n", name, value, equity_adjusted, depletion)
end
