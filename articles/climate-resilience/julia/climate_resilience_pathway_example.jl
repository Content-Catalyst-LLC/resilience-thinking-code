# Climate resilience pathway example
#
# Run:
#   julia julia/climate_resilience_pathway_example.jl

using Printf

strategies = [
    ("Heat-Resilient Urban Redesign", 8.2, 7.9, 8.0, 7.8, 8.1, 8.0, 3.5),
    ("Coastal Ecosystem-Based Adaptation Program", 8.5, 8.3, 7.9, 7.6, 8.4, 7.8, 3.0),
    ("Community-Led Floodplain Adaptation", 8.3, 8.5, 8.2, 7.9, 8.4, 8.8, 2.8)
]

function resilience_value(exposure, vulnerability, adaptive, recovery, transformation, justice, maladaptation)
    return 0.16 * exposure +
           0.16 * vulnerability +
           0.16 * adaptive +
           0.15 * recovery +
           0.15 * transformation +
           0.14 * justice -
           0.08 * maladaptation
end

println("strategy,resilience_value,justice_weighted_value,maladaptation_risk")

for s in strategies
    name, exposure, vulnerability, adaptive, recovery, transformation, justice, maladaptation = s
    value = resilience_value(exposure, vulnerability, adaptive, recovery, transformation, justice, maladaptation)
    justice_weighted = value * (0.72 + 0.028 * justice)
    @printf("%s,%.5f,%.5f,%.2f\n", name, value, justice_weighted, maladaptation)
end
