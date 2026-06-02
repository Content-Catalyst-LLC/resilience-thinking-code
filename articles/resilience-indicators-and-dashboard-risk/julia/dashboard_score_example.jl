# Resilience dashboard score and uncertainty example
#
# Run:
#   julia julia/dashboard_score_example.jl

using Printf

systems = [
    ("Urban Water Network", 0.62, 0.70, 0.58, 0.64, 0.50, 0.46, 0.18),
    ("Wetland Floodplain System", 0.78, 0.68, 0.74, 0.80, 0.58, 0.38, 0.14),
    ("Community Cooling Network", 0.54, 0.57, 0.61, 0.52, 0.72, 0.55, 0.26)
]

function dashboard_scores(exposure, recovery, adaptive, buffer, justice, threshold_risk, missingness)
    naive = 0.17 * exposure + 0.18 * recovery + 0.19 * adaptive + 0.16 * buffer + 0.16 * justice
    threshold_adjusted = naive - 0.09 * threshold_risk
    uncertainty_adjusted = threshold_adjusted - 0.05 * missingness
    return naive, threshold_adjusted, uncertainty_adjusted
end

println("system,naive_score,threshold_adjusted_score,uncertainty_adjusted_score,red_flag")

for s in systems
    name, exposure, recovery, adaptive, buffer, justice, threshold_risk, missingness = s
    naive, threshold_adjusted, uncertainty_adjusted = dashboard_scores(exposure, recovery, adaptive, buffer, justice, threshold_risk, missingness)
    red_flag = threshold_risk >= 0.50 || justice <= 0.52 || missingness >= 0.24 ? "requires review" : "no immediate red flag"
    @printf("%s,%.5f,%.5f,%.5f,%s\n", name, naive, threshold_adjusted, uncertainty_adjusted, red_flag)
end
