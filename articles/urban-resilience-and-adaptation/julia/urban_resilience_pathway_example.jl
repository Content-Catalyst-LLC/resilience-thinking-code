# Urban resilience pathway example
#
# Run:
#   julia julia/urban_resilience_pathway_example.jl

using Printf

strategies = [
    ("Heat-Resilient Housing Retrofit Program", 7.8, 8.8, 8.1, 8.0, 7.4, 8.6, 2.9),
    ("Community Resilience Hub Network", 7.2, 8.5, 8.0, 8.6, 7.6, 8.9, 2.6),
    ("Anti-Displacement Climate Adaptation Framework", 7.5, 8.9, 7.7, 8.4, 7.5, 9.1, 2.5)
]

function resilience_value(exposure, vulnerability, service, adaptive, ecology, equity, maladaptation)
    return 0.16 * exposure +
           0.17 * vulnerability +
           0.17 * service +
           0.15 * adaptive +
           0.14 * ecology +
           0.15 * equity -
           0.06 * maladaptation
end

println("strategy,resilience_value,equity_adjusted_value,maladaptation_risk")

for s in strategies
    name, exposure, vulnerability, service, adaptive, ecology, equity, maladaptation = s
    value = resilience_value(exposure, vulnerability, service, adaptive, ecology, equity, maladaptation)
    equity_adjusted = value * (0.72 + 0.028 * equity)
    @printf("%s,%.5f,%.5f,%.2f\n", name, value, equity_adjusted, maladaptation)
end
