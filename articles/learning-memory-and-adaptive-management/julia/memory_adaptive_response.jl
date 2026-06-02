# Memory and adaptive response example
#
# Run:
#   julia julia/memory_adaptive_response.jl

using Printf

profiles = [
    ("High Learning and Strong Memory", 0.18, 0.88, 0.84, 0.82, 0.82, 0.20),
    ("Good Monitoring but Weak Governance", 0.16, 0.70, 0.48, 0.86, 0.45, 0.34),
    ("Strong Community Memory", 0.15, 0.86, 0.76, 0.74, 0.70, 0.24),
    ("High Forgetting and Low Feedback Use", 0.08, 0.52, 0.42, 0.55, 0.48, 0.52)
]

function adaptive_value(learning_rate, memory_retention, feedback_use, monitoring_quality, governance_capacity, forgetting_pressure)
    return 0.18 * learning_rate * 10 +
           0.20 * memory_retention * 10 +
           0.20 * feedback_use * 10 +
           0.16 * monitoring_quality * 10 +
           0.18 * governance_capacity * 10 -
           0.08 * forgetting_pressure * 10
end

println("profile,learning_rate,memory_retention,feedback_use,monitoring_quality,governance_capacity,forgetting_pressure,adaptive_value")

for p in profiles
    name, learning_rate, memory_retention, feedback_use, monitoring_quality, governance_capacity, forgetting_pressure = p
    value = adaptive_value(learning_rate, memory_retention, feedback_use, monitoring_quality, governance_capacity, forgetting_pressure)
    @printf("%s,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.5f\n",
        name, learning_rate, memory_retention, feedback_use, monitoring_quality, governance_capacity, forgetting_pressure, value)
end
