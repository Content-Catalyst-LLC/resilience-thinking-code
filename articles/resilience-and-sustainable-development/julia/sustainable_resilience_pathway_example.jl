# Sustainable resilience pathway example.
# Run: julia julia/sustainable_resilience_pathway_example.jl

using Printf

pathways = [
    ("Distributed Renewable Infrastructure", 8.5, 8.2, 7.8, 8.0, 7.8, 8.4, 4.0, 3.5),
    ("Climate-Resilient Food and Water Strategy", 8.7, 8.4, 8.1, 8.2, 8.1, 8.6, 3.9, 3.4),
    ("Ecosystem Restoration and Livelihood Diversification", 8.4, 9.0, 8.2, 7.9, 8.0, 8.7, 3.5, 3.2)
]

function viability_value(resilience, ecology, inclusion, economy, governance, adaptive, pressure, burden)
    return 0.18 * resilience +
           0.17 * ecology +
           0.16 * inclusion +
           0.14 * economy +
           0.14 * governance +
           0.15 * adaptive -
           0.04 * pressure -
           0.02 * burden
end

println("pathway,viability_value,boundary_adjusted_viability")

for p in pathways
    name, resilience, ecology, inclusion, economy, governance, adaptive, pressure, burden = p
    value = viability_value(resilience, ecology, inclusion, economy, governance, adaptive, pressure, burden)
    boundary_adjusted = value - max(0, pressure - 3.8) * 0.20 - max(0, 8.2 - inclusion) * 0.12 - max(0, 8.2 - ecology) * 0.12
    @printf("%s,%.5f,%.5f\n", name, value, boundary_adjusted)
end
