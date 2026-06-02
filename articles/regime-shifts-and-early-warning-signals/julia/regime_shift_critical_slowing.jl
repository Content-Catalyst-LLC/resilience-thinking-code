# Regime shift and critical slowing example
#
# Run:
#   julia julia/regime_shift_critical_slowing.jl

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
    if std(x) == 0 || std(y) == 0
        return NaN
    end
    return cor(x, y)
end

steps = 180
pressure = collect(range(-0.75, 0.85, length=steps))
state = zeros(steps)
state[1] = -0.90
window = 18

for t in 2:steps
    state[t] = update_state(state[t - 1], pressure[t])
end

println("time,pressure,state,regime,rolling_variance,rolling_autocorr,recovery_speed_proxy")

for t in 1:steps
    regime = state[t] >= 0 ? "upper regime" : "lower regime"
    if t >= window
        segment = state[(t-window+1):t]
        rv = var(segment)
        ac = lag1_autocorr(segment)
        rsp = 1 - ac
        @printf("%d,%.6f,%.6f,%s,%.6f,%.6f,%.6f\n", t, pressure[t], state[t], regime, rv, ac, rsp)
    else
        @printf("%d,%.6f,%.6f,%s,,,\n", t, pressure[t], state[t], regime)
    end
end
