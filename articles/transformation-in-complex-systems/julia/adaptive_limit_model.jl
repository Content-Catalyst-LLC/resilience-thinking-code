# Adaptive-limit and transformative-capacity example
#
# Run:
#   julia julia/adaptive_limit_model.jl

using Printf

function clamp01(x)
    return max(0.0, min(1.0, x))
end

steps = 80
viability = 0.72
adaptive_capacity = 0.62
structural_rigidity = 0.36
stress = 0.30
transformative_capacity = 0.22

println("time,viability,adaptive_capacity,structural_rigidity,stress,transformative_capacity,regime_note")

for t in 1:steps
    stress = clamp01(stress + 0.006)
    structural_rigidity = clamp01(structural_rigidity + 0.002)
    adaptive_capacity = clamp01(adaptive_capacity - 0.0015 * stress + 0.001 * transformative_capacity)

    if t >= 40
        transformative_capacity = clamp01(transformative_capacity + 0.007)
    end

    viability = clamp01(
        viability +
        0.12 * adaptive_capacity -
        0.10 * structural_rigidity -
        0.16 * stress +
        0.08 * transformative_capacity
    )

    regime_note = transformative_capacity > 0.50 ? "transformation pathway strengthening" : "adaptation within current regime"
    @printf("%d,%.5f,%.5f,%.5f,%.5f,%.5f,%s\n",
        t, viability, adaptive_capacity, structural_rigidity, stress, transformative_capacity, regime_note)
end
