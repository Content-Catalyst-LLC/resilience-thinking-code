# Public health system resilience pathway example.
# Run: julia julia/public_health_resilience_pathway_example.jl

using Printf

strategies = [
    ("Essential Health Service Continuity Program", 7.6, 7.4, 9.0, 8.1, 8.2, 7.9, 8.2, 3.2),
    ("Community Health Trust and Outreach Network", 8.2, 7.9, 8.1, 8.2, 8.5, 9.0, 8.9, 2.8),
    ("Equity-Centered Emergency Preparedness Framework", 8.1, 8.0, 8.2, 8.3, 8.8, 8.7, 9.1, 3.0)
]

function resilience_value(prevention, detection, continuity, workforce, governance, trust, equity, burden)
    return 0.14 * prevention +
           0.15 * detection +
           0.15 * continuity +
           0.14 * workforce +
           0.14 * governance +
           0.13 * trust +
           0.13 * equity -
           0.02 * burden
end

println("strategy,resilience_value,equity_adjusted_value,implementation_burden")

for s in strategies
    name, prevention, detection, continuity, workforce, governance, trust, equity, burden = s
    value = resilience_value(prevention, detection, continuity, workforce, governance, trust, equity, burden)
    equity_adjusted = value * (0.72 + 0.028 * equity)
    @printf("%s,%.5f,%.5f,%.2f\n", name, value, equity_adjusted, burden)
end
