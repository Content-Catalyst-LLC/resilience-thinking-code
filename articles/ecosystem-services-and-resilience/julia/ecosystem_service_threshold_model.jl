# Ecosystem-service threshold model
#
# Run:
#   julia julia/ecosystem_service_threshold_model.jl

using Printf

function simulate_service(; steps=100, condition=0.62, functional_capacity=0.58,
    redundancy=0.48, memory=0.52, governance=0.55, exposure=0.70, access=0.52)

    println("time,disturbance,ecosystem_condition,functional_capacity,service_flow,resilience_margin,threshold_flag")

    for t in 1:steps
        seasonal_pressure = 0.04 + 0.020 * sin(t / 8.0)
        shock = (t in [22, 45, 67, 84]) ? 0.25 : 0.0
        disturbance = seasonal_pressure + shock + 0.18 * exposure

        repair = 0.010 * redundancy + 0.009 * memory + 0.008 * governance
        erosion = disturbance * (0.42 + exposure)

        condition = max(0.01, min(1.0, condition - 0.045 * erosion + repair))
        functional_capacity = max(0.01, min(1.0, functional_capacity - 0.030 * erosion + 0.006 * redundancy))

        service_flow = max(0.0, min(1.0, condition * functional_capacity * (1 - 0.35 * disturbance)))
        margin = condition + functional_capacity + redundancy + memory + governance + 0.35 * access - disturbance - exposure
        flag = margin < 1.30 ? "threshold risk" : "viable margin"

        @printf("%d,%.5f,%.5f,%.5f,%.5f,%.5f,%s\n", t, disturbance, condition, functional_capacity, service_flow, margin, flag)
    end
end

simulate_service()
