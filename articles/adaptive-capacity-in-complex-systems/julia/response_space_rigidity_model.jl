# Response-space and rigidity model
#
# Run:
#   julia julia/response_space_rigidity_model.jl

using Printf

function simulate_viability(; steps=80, capacity=0.58, vulnerability=0.62,
    rigidity=0.55, exposure=0.70, slack=0.50, trust=0.57)

    viability = 1.0
    println("time,disturbance,adaptive_capacity,rigidity,response_space,viability,threshold_flag")

    for t in 1:steps
        seasonal = 0.04 + 0.025 * sin(t / 8.0)
        shock = (t % 10 == 0) ? 0.22 : 0.0
        disturbance = 0.26 + seasonal + shock + 0.18 * exposure

        capacity = max(0.0, min(1.2, capacity + 0.010 + 0.006 * 0.50 - 0.010 * rigidity))
        rigidity = max(0.0, min(1.0, rigidity + 0.010 + 0.004 * disturbance - 0.006 * 0.50))

        response_space = capacity + 0.35 * slack + 0.25 * trust - rigidity - 0.25 * vulnerability

        viability = viability - 0.46 * disturbance + 0.25 * capacity + 0.08 * response_space - 0.12 * rigidity
        viability = max(0.0, min(1.2, viability))

        flag = viability < 0.45 ? "threshold risk" : "viable margin"
        @printf("%d,%.5f,%.5f,%.5f,%.5f,%.5f,%s\n", t, disturbance, capacity, rigidity, response_space, viability, flag)
    end
end

simulate_viability()
