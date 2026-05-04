# Resilience Thinking: Nonlinear Threshold Model in Julia
# Educational example only.

function simulate_threshold(; r=1.0, p=0.1, x0=0.2, dt=0.01, steps=1000)
    x = zeros(Float64, steps)
    x[1] = x0

    for t in 2:steps
        dx = r * x[t - 1] - x[t - 1]^3 + p
        x[t] = x[t - 1] + dt * dx
    end

    return x
end

states = simulate_threshold(p=0.2)

println("Final state: ", states[end])
println("Minimum state: ", minimum(states))
println("Maximum state: ", maximum(states))
