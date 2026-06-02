# Biodiversity-function threshold example
#
# Run:
#   julia julia/biodiversity_function_threshold.jl

using Printf

function simulate_function(; steps=100, functional_output=2.4, redundancy=4.0,
    response_diversity=0.055, memory=0.60, connectivity=0.54, exposure=0.66)

    println("time,functional_output,redundancy,response_diversity,disturbance,resilience_margin,threshold_flag")

    for t in 1:steps
        seasonal = 0.055 + 0.025 * sin(t / 9.0)
        shock = (t in [24, 47, 70, 88]) ? 0.32 : 0.0
        disturbance = seasonal + shock + 0.18 * exposure

        functional_output = max(0.0, functional_output - 0.030 * disturbance + 0.010 * memory)
        redundancy = max(0.0, redundancy - 0.018 * disturbance + 0.004 * connectivity)
        response_diversity = max(0.0, response_diversity - 0.003 * disturbance + 0.001 * memory)

        margin = functional_output + 0.055 * redundancy + response_diversity + memory + connectivity - disturbance - exposure
        flag = margin < 1.20 ? "threshold risk" : "viable margin"

        @printf("%d,%.5f,%.5f,%.5f,%.5f,%.5f,%s\n", t, functional_output, redundancy, response_diversity, disturbance, margin, flag)
    end
end

simulate_function()
