# Community resilience pathway example.
# Run: julia julia/community_resilience_pathway_example.jl

using Printf

strategies = [
    ("Neighborhood Mutual Aid and Preparedness Network", 8.9, 7.5, 7.1, 7.6, 7.9, 8.2, 8.1, 2.7),
    ("Inclusive Community Governance and Adaptation Forum", 8.4, 8.3, 7.4, 7.8, 7.8, 8.6, 8.8, 3.1),
    ("Community Health and Care Continuity Network", 8.6, 8.0, 7.8, 7.5, 8.0, 8.1, 8.7, 3.0)
]

function resilience_value(social, institution, access, economy, information, adaptive, equity, burden)
    return 0.14 * social +
           0.14 * institution +
           0.14 * access +
           0.13 * economy +
           0.13 * information +
           0.15 * adaptive +
           0.15 * equity -
           0.02 * burden
end

println("strategy,resilience_value,equity_adjusted_value,implementation_burden")

for s in strategies
    name, social, institution, access, economy, information, adaptive, equity, burden = s
    value = resilience_value(social, institution, access, economy, information, adaptive, equity, burden)
    equity_adjusted = value * (0.72 + 0.028 * equity)
    @printf("%s,%.5f,%.5f,%.2f\n", name, value, equity_adjusted, burden)
end
