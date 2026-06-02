# Feedback, disturbance, and resilience-margin model.
#
# Run:
#   julia julia/feedback_threshold_model.jl

using Printf

function simulate(; steps=100, reinforcing=0.18, repair=0.25, adaptive=0.70, buffer=0.65, threshold=0.25)
    vulnerability = 0.35
    println("time,disturbance,vulnerability_stock,resilience_margin,threshold_flag")

    for t in 1:steps
        disturbance = 0.06 + 0.03*sin(t / 6.0)
        if t in [20, 40, 65, 83]
            disturbance += 0.30
        end

        vulnerability += reinforcing * vulnerability + 0.35 * disturbance - repair * disturbance - 0.012 * adaptive
        vulnerability = max(0.0, min(2.0, vulnerability))

        margin = buffer + adaptive - vulnerability - 0.25 * disturbance
        flag = margin < threshold ? "threshold risk" : "viable margin"

        @printf("%d,%.5f,%.5f,%.5f,%s\n", t, disturbance, vulnerability, margin, flag)
    end
end

simulate()
