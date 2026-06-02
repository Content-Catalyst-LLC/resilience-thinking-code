# Adaptive-cycle transition example
#
# Run:
#   julia julia/adaptive_cycle_transition.jl

using Printf
using Random

Random.seed!(42)

function simulate_cycle(; steps=120)
    potential = 0.20
    connectedness = 0.15
    resilience = 0.82
    rigidity = 0.10
    memory = 0.55
    novelty = 0.15
    phase = "r"

    println("time,phase,potential,connectedness,resilience,rigidity,memory,novelty,release_flag")

    for t in 1:steps
        previous_phase = phase

        if phase == "r" || phase == "K"
            potential = min(1.0, potential + 0.11 * potential * (1.0 - potential))
            connectedness = min(1.0, connectedness + 0.08 * (1.0 - connectedness))
            rigidity = min(1.0, rigidity + 0.055 * connectedness)
            resilience = max(0.0, 1.0 - 0.62 * connectedness - 0.35 * rigidity)
            memory = min(1.0, memory + 0.015 * potential)
            novelty = max(0.02, 0.25 * (1.0 - connectedness))
            phase = connectedness > 0.55 ? "K" : "r"

            if rigidity > 0.72 && resilience < 0.34
                phase = "Omega"
            end

        elseif phase == "Omega"
            potential = max(0.05, potential * 0.42)
            connectedness = max(0.08, connectedness * 0.32)
            rigidity = max(0.05, rigidity * 0.38)
            resilience = min(1.0, resilience + 0.30)
            memory = max(0.25, memory * 0.86)
            novelty = 0.25 + rand() * 0.20
            phase = "alpha"

        elseif phase == "alpha"
            novelty = 0.18 + rand() * 0.20
            potential = min(1.0, 0.48 * memory + 0.06 + rand() * 0.12)
            connectedness = min(1.0, connectedness + 0.015 + rand() * 0.030)
            rigidity = max(0.03, rigidity - 0.020 + rand() * 0.035)
            resilience = min(1.0, resilience + 0.025 + rand() * 0.050)
            memory = min(1.0, memory - 0.015 + rand() * 0.040)
            phase = (potential > 0.32 && connectedness < 0.50) ? "r" : "alpha"
        end

        release_flag = phase == "Omega" ? 1 : 0
        @printf("%d,%s,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f,%d\n",
            t, phase, potential, connectedness, resilience, rigidity, memory, novelty, release_flag)
    end
end

simulate_cycle()
