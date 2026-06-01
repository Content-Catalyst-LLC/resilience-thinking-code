# Nonlinear threshold and regime-shift example
#
# Run:
#   julia julia/threshold_regime_shift.jl

using Printf

function dxdt(x, r, p)
    return r*x - x^3 + p
end

function simulate(; x0=0.1, r=1.0, p=0.0, dt=0.02, steps=500)
    x = x0
    values = Float64[]
    for _ in 1:steps
        x += dt * dxdt(x, r, p)
        push!(values, x)
    end
    return values
end

pressures = collect(-0.4:0.05:0.4)

println("pressure,final_state,regime_label")
for p in pressures
    values = simulate(p=p)
    final_state = values[end]
    label = final_state > 0 ? "positive regime" : "negative regime"
    @printf("%.2f,%.5f,%s\n", p, final_state, label)
end
