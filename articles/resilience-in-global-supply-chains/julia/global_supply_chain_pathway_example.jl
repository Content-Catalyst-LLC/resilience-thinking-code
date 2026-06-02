# Global supply chain resilience pathway example.
# Run: julia julia/global_supply_chain_pathway_example.jl

using Printf

strategies = [
    ("Supplier Diversification and Qualification Program", 8.8, 8.2, 7.6, 8.0, 8.4, 7.9, 7.6, 4.0, 3.2),
    ("Multi-Route Logistics and Chokepoint Redesign", 8.1, 8.8, 8.0, 8.2, 8.5, 7.8, 8.5, 4.0, 3.4),
    ("Fair Supplier Finance and Labor Continuity Program", 7.7, 8.1, 7.5, 8.3, 8.2, 9.0, 7.6, 3.8, 3.0)
]

function supply_chain_value(redundancy, flexibility, visibility, coordination, adaptation, equity, infrastructure, exposure, burden)
    return 0.13 * redundancy +
           0.13 * flexibility +
           0.13 * visibility +
           0.13 * coordination +
           0.13 * adaptation +
           0.13 * equity +
           0.13 * infrastructure -
           0.06 * exposure -
           0.03 * burden
end

println("strategy,supply_chain_resilience_value,equity_adjusted_value,implementation_burden")

for s in strategies
    name, redundancy, flexibility, visibility, coordination, adaptation, equity, infrastructure, exposure, burden = s
    value = supply_chain_value(redundancy, flexibility, visibility, coordination, adaptation, equity, infrastructure, exposure, burden)
    adjusted = value - 0.08 * max(0, 8.0 - equity) - 0.06 * max(0, 8.0 - infrastructure)
    @printf("%s,%.5f,%.5f,%.2f\n", name, value, adjusted, burden)
end
