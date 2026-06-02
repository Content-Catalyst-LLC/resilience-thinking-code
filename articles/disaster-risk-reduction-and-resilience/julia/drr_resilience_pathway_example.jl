# DRR and resilience pathway example
#
# Run:
#   julia julia/drr_resilience_pathway_example.jl

using Printf

strategies = [
    ("Floodplain Land-Use Restriction", 7.4, 8.6, 7.5, 6.9, 7.2, 3.4),
    ("Community Early Warning Network", 6.8, 7.1, 8.1, 8.7, 8.0, 2.6),
    ("Equitable Recovery and Housing Protection Program", 6.7, 7.4, 8.9, 8.3, 9.0, 2.4)
]

function drr_value(hazard, exposure, vulnerability, capacity, justice, maladaptation)
    return 0.17 * hazard +
           0.18 * exposure +
           0.18 * vulnerability +
           0.17 * capacity +
           0.18 * justice -
           0.12 * maladaptation
end

println("strategy,drr_value,justice_adjusted_value,maladaptation_risk")

for s in strategies
    name, hazard, exposure, vulnerability, capacity, justice, maladaptation = s
    value = drr_value(hazard, exposure, vulnerability, capacity, justice, maladaptation)
    justice_adjusted = value * (0.72 + 0.028 * justice)
    @printf("%s,%.5f,%.5f,%.2f\n", name, value, justice_adjusted, maladaptation)
end
