# Strategic slack pathway example.
# Run: julia julia/strategic_slack_pathway_example.jl

using Printf

portfolios = [
    ("Workforce Depth and Recovery Time", 7.5, 9.2, 7.8, 8.0, 7.5, 8.2, 9.1, 2.6, 3.4),
    ("Knowledge Architecture and Institutional Memory", 7.4, 8.0, 7.6, 9.3, 7.8, 8.5, 8.3, 2.9, 3.3),
    ("Adaptive Governance and Emergency Decision Space", 7.8, 8.1, 8.0, 8.4, 8.1, 9.1, 8.4, 2.8, 3.2)
]

function slack_value(financial, workforce, operational, knowledge, network, governance, ethics, ethical_burden, implementation)
    return 0.13 * financial +
           0.14 * workforce +
           0.13 * operational +
           0.13 * knowledge +
           0.13 * network +
           0.14 * governance +
           0.13 * ethics -
           0.04 * ethical_burden -
           0.03 * implementation
end

println("portfolio,slack_resilience_value,adjusted_value,ethical_burden")

for p in portfolios
    name, financial, workforce, operational, knowledge, network, governance, ethics, ethical_burden, implementation = p
    value = slack_value(financial, workforce, operational, knowledge, network, governance, ethics, ethical_burden, implementation)
    adjusted = value - 0.07 * max(0, 8.2 - workforce) - 0.06 * max(0, 8.2 - knowledge) - 0.06 * max(0, 8.2 - governance)
    @printf("%s,%.5f,%.5f,%.2f\n", name, value, adjusted, ethical_burden)
end
