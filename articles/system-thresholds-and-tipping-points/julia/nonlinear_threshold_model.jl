# Nonlinear threshold and critical slowing down example
#
# Run:
#   julia julia/nonlinear_threshold_model.jl

using Printf
using Statistics

function update_state(x, pressure; r=1.2, dt=0.05)
    return x + dt * (r * x - x^3 + pressure)
end

function lag1_autocorr(values)
    if length(values) < 3
        return NaN
    end
    x = values[1:end-1]
    y = values[2:end]
    sx = std(x)
    sy = std(y)
    if sx == 0 || sy == 0
        return NaN
    end
    return cor(x, y)
end

steps = 160
pressures = collect(range(-0.8, 0.8, length=steps))
states = zeros(steps)
states[1] = -0.9
window = 16

println("step,pressure,state,rolling_variance,rolling_autocorr,recovery_speed_proxy,regime")

for i in 2:steps
    states[i] = update_state(states[i-1], pressures[i])
end

for i in 1:steps
    if i >= window
        segment = states[(i-window+1):i]
        rv = var(segment)
        ac = lag1_autocorr(segment)
        rsp = 1 - ac
        regime = states[i] >= 0 ? "upper regime" : "lower regime"
        @printf("%d,%.6f,%.6f,%.6f,%.6f,%.6f,%s\n", i, pressures[i], states[i], rv, ac, rsp, regime)
    else
        regime = states[i] >= 0 ? "upper regime" : "lower regime"
        @printf("%d,%.6f,%.6f,,,,%s\n", i, pressures[i], states[i], regime)
    end
end
