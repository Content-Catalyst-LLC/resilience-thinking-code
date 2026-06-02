# Local economic resilience pathway example.
# Run: julia julia/local_resilience_pathway_example.jl

using Printf

strategies = [
    ("Emergency Microgrant and Liquidity Fund", 9.2, 7.4, 7.2, 7.4, 8.3, 7.5, 8.6, 2.8, 3.0),
    ("Community Development Finance and Patient Capital", 8.7, 7.5, 7.6, 7.5, 8.4, 8.7, 8.9, 2.7, 3.5),
    ("Local Procurement and Anchor Institution Access", 7.6, 7.8, 8.6, 7.8, 8.8, 8.8, 8.4, 3.0, 3.6)
]

function local_value(liquidity, workforce, supply, digital, public_capacity, community, equity, inequality, implementation)
    return 0.14 * liquidity +
           0.14 * workforce +
           0.12 * supply +
           0.12 * digital +
           0.14 * public_capacity +
           0.15 * community +
           0.16 * equity -
           0.07 * inequality -
           0.06 * implementation
end

println("strategy,local_resilience_value,adjusted_value,inequality_risk")

for s in strategies
    name, liquidity, workforce, supply, digital, public_capacity, community, equity, inequality, implementation = s
    value = local_value(liquidity, workforce, supply, digital, public_capacity, community, equity, inequality, implementation)
    adjusted = value - 0.08 * max(0, 8.5 - equity) - 0.06 * max(0, 8.0 - liquidity) - 0.06 * max(0, 8.0 - workforce)
    @printf("%s,%.5f,%.5f,%.2f\n", name, value, adjusted, inequality)
end
