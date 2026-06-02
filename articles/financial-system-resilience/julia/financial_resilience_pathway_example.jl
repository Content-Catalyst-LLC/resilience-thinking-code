# Financial system resilience pathway example.
# Run: julia julia/financial_resilience_pathway_example.jl

using Printf

strategies = [
    ("Higher Capital and Liquidity Buffers", 8.9, 8.8, 7.6, 8.3, 7.4, 3.9, 3.2),
    ("Payment and Clearing Infrastructure Hardening", 7.4, 7.8, 9.2, 8.5, 7.8, 3.8, 3.5),
    ("Inclusive Finance and Household Balance Sheet Resilience", 7.2, 7.4, 7.4, 8.1, 9.2, 4.0, 3.0)
]

function financial_value(capital, liquidity, infrastructure, governance, inclusion, exposure, burden)
    return 0.16 * capital +
           0.16 * liquidity +
           0.16 * infrastructure +
           0.16 * governance +
           0.16 * inclusion -
           0.12 * exposure -
           0.08 * burden
end

println("strategy,financial_resilience_value,inclusion_adjusted_value,implementation_burden")

for s in strategies
    name, capital, liquidity, infrastructure, governance, inclusion, exposure, burden = s
    value = financial_value(capital, liquidity, infrastructure, governance, inclusion, exposure, burden)
    adjusted = value - 0.07 * max(0, 8.0 - inclusion) - 0.06 * max(0, 8.0 - infrastructure)
    @printf("%s,%.5f,%.5f,%.2f\n", name, value, adjusted, burden)
end
