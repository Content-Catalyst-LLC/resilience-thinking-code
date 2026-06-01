# Threshold model for the historical shift from stability logic to resilience logic.
#
# Run:
#   julia julia/threshold_history_model.jl

using Printf

function dxdt(x, r, p)
    return r*x - x^3 + p
end

function simulate_threshold(; steps=160, x0=-0.9, r=1.1, dt=0.05)
    x = x0
    rows = []
    for t in 1:steps
        pressure = -0.45 + 1.30 * (t - 1) / (steps - 1)
        if t > 1
            x += dt * dxdt(x, r, pressure)
        end
        push!(rows, (t, pressure, x))
    end
    return rows
end

println("time,pressure,threshold_state")
for (t, p, x) in simulate_threshold()
    @printf("%d,%.5f,%.5f\n", t, p, x)
end
