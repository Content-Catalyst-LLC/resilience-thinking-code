# Engineering return vs ecological threshold dynamics.
#
# Run:
#   julia julia/threshold_dynamics.jl

using Printf

function engineering_return(; steps=120, x0=1.0, xstar=0.0, a=0.18)
    x = x0
    rows = []
    for t in 1:steps
        if t > 1
            x = x - a * (x - xstar)
        end
        push!(rows, (t, x))
    end
    return rows
end

function ecological_threshold(; steps=120, x0=-0.9, r=1.1, dt=0.05)
    x = x0
    rows = []
    for t in 1:steps
        pressure = -0.45 + 1.30 * (t - 1) / (steps - 1)
        if t > 1
            x = x + dt * (r*x - x^3 + pressure)
        end
        push!(rows, (t, pressure, x))
    end
    return rows
end

eng = engineering_return()
eco = ecological_threshold()

println("time,engineering_state,pressure,ecological_state")
for i in 1:length(eng)
    t, e = eng[i]
    _, p, x = eco[i]
    @printf("%d,%.6f,%.6f,%.6f\n", t, e, p, x)
end
