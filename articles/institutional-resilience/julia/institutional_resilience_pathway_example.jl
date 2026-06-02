# Institutional resilience pathway example.
# Run: julia julia/institutional_resilience_pathway_example.jl

using Printf

strategies = [
    ("Public Trust and Transparency Initiative", 8.9, 7.1, 7.0, 7.2, 7.4, 8.5, 8.2, 2.8),
    ("Equity and Access Accountability Review", 8.3, 7.5, 7.8, 7.6, 7.9, 8.9, 9.1, 3.0),
    ("Institutional Learning and After-Action Implementation System", 7.8, 8.0, 8.2, 8.4, 9.0, 8.4, 8.1, 3.3)
]

function resilience_value(legitimacy, capacity, flexibility, coordination, learning, accountability, equity, burden)
    return 0.14 * legitimacy +
           0.14 * capacity +
           0.13 * flexibility +
           0.14 * coordination +
           0.14 * learning +
           0.14 * accountability +
           0.15 * equity -
           0.02 * burden
end

println("strategy,resilience_value,equity_adjusted_value,implementation_burden")

for s in strategies
    name, legitimacy, capacity, flexibility, coordination, learning, accountability, equity, burden = s
    value = resilience_value(legitimacy, capacity, flexibility, coordination, learning, accountability, equity, burden)
    equity_adjusted = value * (0.72 + 0.028 * equity)
    @printf("%s,%.5f,%.5f,%.2f\n", name, value, equity_adjusted, burden)
end
