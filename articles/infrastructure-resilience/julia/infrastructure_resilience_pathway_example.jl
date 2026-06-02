# Infrastructure resilience pathway example
#
# Run:
#   julia julia/infrastructure_resilience_pathway_example.jl

using Printf

strategies = [
    ("Grid Redundancy and Microgrid Expansion", 8.7, 8.9, 8.0, 8.2, 7.8, 3.9),
    ("Hybrid Wetland and Stormwater Infrastructure", 8.0, 7.8, 7.6, 8.4, 8.1, 3.6),
    ("Equitable Critical Service Restoration Program", 8.4, 8.0, 8.6, 8.1, 8.9, 3.4)
]

function resilience_value(service, redundancy, recovery, adaptive, equity, cascade)
    return 0.22 * service +
           0.20 * redundancy +
           0.18 * recovery +
           0.16 * adaptive +
           0.16 * equity -
           0.08 * cascade
end

println("strategy,resilience_value,equity_adjusted_value,cascading_exposure")

for s in strategies
    name, service, redundancy, recovery, adaptive, equity, cascade = s
    value = resilience_value(service, redundancy, recovery, adaptive, equity, cascade)
    equity_adjusted = value * (0.72 + 0.028 * equity)
    @printf("%s,%.5f,%.5f,%.2f\n", name, value, equity_adjusted, cascade)
end
