# Economic resilience pathway example.
# Run: julia julia/economic_resilience_pathway_example.jl

using Printf

strategies = [
    ("Industrial Diversification and Local Production Program", 8.0, 8.0, 8.5, 8.4, 8.1, 8.2, 3.5),
    ("Countercyclical Stabilization and Public Investment Framework", 8.5, 8.8, 8.0, 8.0, 8.3, 8.8, 3.4),
    ("Community Finance and Small Business Continuity Fund", 8.1, 8.5, 8.1, 7.9, 8.7, 8.2, 2.9)
]

function resilience_value(resistance, recovery, adaptation, transformation, equity, institutions, burden)
    return 0.16 * resistance +
           0.16 * recovery +
           0.17 * adaptation +
           0.17 * transformation +
           0.17 * equity +
           0.17 * institutions -
           0.02 * burden
end

println("strategy,economic_resilience_value,equity_adjusted_value,implementation_burden")

for s in strategies
    name, resistance, recovery, adaptation, transformation, equity, institutions, burden = s
    value = resilience_value(resistance, recovery, adaptation, transformation, equity, institutions, burden)
    adjusted = value - 0.08 * max(0, 8.3 - equity) - 0.06 * max(0, 8.2 - institutions)
    @printf("%s,%.5f,%.5f,%.2f\n", name, value, adjusted, burden)
end
