# Nonlinear threshold predictor example
#
# Run:
#   julia julia/nonlinear_threshold_predictor.jl

using Printf

function sigmoid(z)
    return 1.0 / (1.0 + exp(-z))
end

function predicted_failure_probability(adaptive, threshold, learning, redundancy, modularity, exposure, sensitivity, shock)
    protective = 0.24*adaptive + 0.22*threshold + 0.18*learning + 0.18*redundancy + 0.18*modularity
    pressure = 0.32*exposure + 0.28*sensitivity + 0.40*shock
    z = -2.0 + 4.2*pressure - 3.8*protective
    return sigmoid(z)
end

scenarios = [
    ("stable_but_brittle", 0.28, 0.32, 0.24, 0.35, 0.34, 0.64, 0.62, 0.45),
    ("robust_but_inflexible", 0.38, 0.46, 0.33, 0.60, 0.43, 0.70, 0.58, 0.52),
    ("adaptive_resilient", 0.88, 0.80, 0.86, 0.73, 0.70, 0.52, 0.46, 0.50)
]

println("scenario,predicted_failure_probability")
for s in scenarios
    name, adaptive, threshold, learning, redundancy, modularity, exposure, sensitivity, shock = s
    p = predicted_failure_probability(adaptive, threshold, learning, redundancy, modularity, exposure, sensitivity, shock)
    @printf("%s,%.4f\n", name, p)
end
