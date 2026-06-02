# Spatial disturbance-threshold example
#
# Run:
#   julia julia/spatial_disturbance_threshold.jl

using Printf

function simulate_patch(; steps=80, condition=0.78, exposure=0.66, buffer=0.70,
    memory=0.72, recovery=0.64, refugia=1.0, social_exposure=0.54)

    disturbance = 0.08 + 0.10 * exposure

    println("time,condition,disturbance,resilience_margin,threshold_flag")

    for t in 1:steps
        seasonal = 0.04 + 0.025 * sin(t / 7.0)
        shock = (t in [18, 36, 55, 70]) ? 0.24 : 0.0

        disturbance = disturbance + 0.32 + seasonal + shock + 0.18 * 0.58 + 0.22 * exposure - 0.26 * buffer - 0.12 * refugia - 0.06 * 0.48
        disturbance = max(0.0, min(1.4, disturbance))

        condition = condition - 0.055 * disturbance + 0.018 * memory + 0.015 * recovery + 0.008 * refugia + 0.006 * 0.48
        condition = max(0.0, min(1.0, condition))

        margin = condition + buffer + memory + recovery + 0.25 * refugia + 0.20 * 0.48 - disturbance - exposure - 0.30 * social_exposure
        flag = margin < 0.75 ? "threshold risk" : "viable margin"

        @printf("%d,%.5f,%.5f,%.5f,%s\n", t, condition, disturbance, margin, flag)
    end
end

simulate_patch()
