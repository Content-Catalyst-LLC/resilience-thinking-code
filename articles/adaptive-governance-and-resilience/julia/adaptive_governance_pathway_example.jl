# Adaptive governance pathway example.
# Run: julia julia/adaptive_governance_pathway_example.jl

using Printf

strategies = [
    ("Adaptive Pathways and Decision Triggers", 8.6, 8.9, 7.9, 8.1, 7.9, 8.0, 7.8, 3.2),
    ("Community Knowledge Co-Production Platform", 8.3, 7.6, 8.0, 9.1, 8.8, 8.3, 8.7, 3.1),
    ("Equity Accountability and Rights Safeguard", 8.1, 7.7, 7.9, 8.4, 8.7, 9.1, 9.2, 3.0)
]

function governance_value(learning, flexibility, coordination, knowledge, legitimacy, accountability, equity, burden)
    return 0.15 * learning +
           0.14 * flexibility +
           0.14 * coordination +
           0.14 * knowledge +
           0.14 * legitimacy +
           0.14 * accountability +
           0.15 * equity -
           0.02 * burden
end

println("strategy,governance_value,accountability_adjusted_value,implementation_burden")

for s in strategies
    name, learning, flexibility, coordination, knowledge, legitimacy, accountability, equity, burden = s
    value = governance_value(learning, flexibility, coordination, knowledge, legitimacy, accountability, equity, burden)
    gap = max(0, flexibility - accountability)
    adjusted = value - 0.08 * gap - 0.08 * max(0, 8.2 - equity)
    @printf("%s,%.5f,%.5f,%.2f\n", name, value, adjusted, burden)
end
