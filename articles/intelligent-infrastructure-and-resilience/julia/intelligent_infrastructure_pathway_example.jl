# Intelligent infrastructure resilience pathway example.
# Run: julia julia/intelligent_infrastructure_pathway_example.jl

using Printf

strategies = [
    ("Digital Twin and Scenario Stress Testing", 8.3, 8.5, 8.1, 9.3, 8.3, 8.6, 8.5, 8.1, 8.2, 3.0, 3.7),
    ("Predictive Maintenance and Asset Renewal", 8.5, 9.3, 8.2, 8.6, 8.4, 8.4, 8.4, 8.2, 8.0, 2.8, 3.8),
    ("Equity-Centered Climate Adaptation Portfolio", 8.2, 8.1, 8.0, 8.4, 8.5, 9.3, 8.9, 9.3, 9.0, 2.6, 3.9)
]

function infrastructure_value(monitoring, maintenance, cyber, twin, redundancy, climate, governance, equity, ecology, fragility, implementation)
    return 0.10 * monitoring +
           0.11 * maintenance +
           0.11 * cyber +
           0.10 * twin +
           0.11 * redundancy +
           0.11 * climate +
           0.12 * governance +
           0.12 * equity +
           0.10 * ecology -
           0.04 * fragility -
           0.04 * implementation
end

println("strategy,infrastructure_resilience_value,adjusted_value,fragility_risk")

for s in strategies
    name, monitoring, maintenance, cyber, twin, redundancy, climate, governance, equity, ecology, fragility, implementation = s
    value = infrastructure_value(monitoring, maintenance, cyber, twin, redundancy, climate, governance, equity, ecology, fragility, implementation)
    adjusted = value - 0.07 * max(0, 8.5 - governance) - 0.08 * max(0, 8.5 - equity) - 0.07 * max(0, 8.5 - redundancy)
    @printf("%s,%.5f,%.5f,%.2f\n", name, value, adjusted, fragility)
end
