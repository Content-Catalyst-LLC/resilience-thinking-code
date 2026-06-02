# Common-mode failure and response-diversity example
#
# Run:
#   julia julia/common_mode_response_diversity.jl

using Printf

strategies = [
    ("Distributed Backup Infrastructure Network", 8.8, 7.4, 7.8, 7.6, 7.2, 7.5, 3.8),
    ("Multi-Supplier and Multi-Technology System Design", 7.9, 8.9, 8.6, 7.3, 7.4, 7.2, 3.5),
    ("Cross-Trained Organizational Response Model", 8.2, 8.1, 8.4, 8.2, 7.8, 7.9, 4.0),
    ("Ecological Restoration for Functional Overlap", 7.6, 8.5, 8.8, 7.4, 7.6, 7.1, 3.7)
]

function resilience_value(redundancy, diversity, response_diversity, coordination, justice, maintenance, common_mode)
    return 0.22 * redundancy +
           0.18 * diversity +
           0.22 * response_diversity +
           0.13 * coordination +
           0.10 * justice +
           0.07 * maintenance -
           0.08 * common_mode
end

println("strategy,redundancy,diversity,response_diversity,common_mode_risk,resilience_value,diagnostic")

for s in strategies
    name, redundancy, diversity, response_diversity, coordination, justice, maintenance, common_mode = s
    value = resilience_value(redundancy, diversity, response_diversity, coordination, justice, maintenance, common_mode)
    diagnostic = common_mode >= 4.0 ? "common-mode failure review needed" : "manageable common-mode risk"
    @printf("%s,%.2f,%.2f,%.2f,%.2f,%.5f,%s\n", name, redundancy, diversity, response_diversity, common_mode, value, diagnostic)
end
