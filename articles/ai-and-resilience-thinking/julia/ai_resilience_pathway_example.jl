# AI resilience pathway example.
# Run: julia julia/ai_resilience_pathway_example.jl

using Printf

strategies = [
    ("AI Decision Support with Human Oversight", 8.1, 8.0, 8.4, 9.1, 8.7, 8.4, 9.2, 8.2, 8.4, 2.7, 3.4),
    ("Participatory AI and Local Knowledge Integration", 7.6, 7.4, 8.2, 8.0, 8.6, 9.2, 9.1, 9.4, 8.0, 2.6, 3.7),
    ("AI Governance Audit and Drift Monitoring", 8.4, 8.2, 8.5, 8.4, 9.3, 8.8, 8.8, 8.4, 9.0, 2.5, 3.8)
]

function ai_value(monitoring, forecasting, scenario, decision, governance, equity, human, local, security, risk, implementation)
    return 0.11 * monitoring +
           0.10 * forecasting +
           0.11 * scenario +
           0.11 * decision +
           0.12 * governance +
           0.12 * equity +
           0.12 * human +
           0.10 * local +
           0.10 * security -
           0.05 * risk -
           0.04 * implementation
end

println("strategy,ai_resilience_value,adjusted_value,ai_risk")

for s in strategies
    name, monitoring, forecasting, scenario, decision, governance, equity, human, local, security, risk, implementation = s
    value = ai_value(monitoring, forecasting, scenario, decision, governance, equity, human, local, security, risk, implementation)
    adjusted = value - 0.07 * max(0, 8.5 - governance) - 0.08 * max(0, 8.5 - equity) - 0.08 * max(0, 8.5 - human) - 0.06 * max(0, 8.2 - local)
    @printf("%s,%.5f,%.5f,%.2f\n", name, value, adjusted, risk)
end
