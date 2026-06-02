# Resilience score and threshold-sensitivity example
#
# Run:
#   julia julia/resilience_score_threshold_sensitivity.jl

using Printf

frameworks = [
    ("Indicator Dashboard", 7.8, 7.0, 7.4, 7.6, 6.8, 7.2, 5.2),
    ("Performance and Recovery Monitoring", 7.1, 8.8, 7.2, 7.3, 6.9, 7.8, 4.6),
    ("Scenario Stress-Test Framework", 8.0, 7.6, 8.1, 7.9, 7.2, 7.4, 3.9),
    ("Participatory Resilience Assessment", 7.2, 7.5, 8.3, 7.5, 8.8, 7.1, 4.3),
    ("Hybrid Structural and Dynamic Assessment", 8.5, 8.4, 8.7, 8.2, 8.1, 8.5, 3.2)
]

function metric_value(resistance, recovery, adaptive, buffer, justice, data_quality, threshold_blindness)
    return 0.16 * resistance +
           0.16 * recovery +
           0.16 * adaptive +
           0.15 * buffer +
           0.13 * justice +
           0.10 * data_quality -
           0.14 * threshold_blindness
end

println("framework,resistance,recovery,adaptive_capacity,buffer,justice,data_quality,threshold_blindness,metric_value,diagnostic")

for f in frameworks
    name, resistance, recovery, adaptive, buffer, justice, data_quality, threshold_blindness = f
    value = metric_value(resistance, recovery, adaptive, buffer, justice, data_quality, threshold_blindness)
    diagnostic = threshold_blindness >= 4.8 ? "threshold blindness review needed" : "threshold sensitivity acceptable"
    @printf("%s,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.5f,%s\n",
        name, resistance, recovery, adaptive, buffer, justice, data_quality, threshold_blindness, value, diagnostic)
end
