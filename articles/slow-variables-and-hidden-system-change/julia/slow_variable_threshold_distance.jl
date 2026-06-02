# Slow-variable threshold-distance example
#
# Run:
#   julia julia/slow_variable_threshold_distance.jl

using Printf

function clamp01(x)
    return max(0.0, min(1.0, x))
end

steps = 120
maintenance_backlog = 0.25
public_trust = 0.72
ecological_memory = 0.68
climate_pressure = 0.22
system_function = 0.86

println("time,maintenance_backlog,public_trust,ecological_memory,climate_pressure,adaptive_capacity,threshold_distance,hidden_risk,fast_shock,system_function")

for t in 1:steps
    maintenance_backlog = clamp01(maintenance_backlog + 0.006)
    public_trust = clamp01(public_trust - 0.0035)
    ecological_memory = clamp01(ecological_memory - 0.0025)
    climate_pressure = clamp01(climate_pressure + 0.0045)

    adaptive_capacity = clamp01(
        0.35 * public_trust +
        0.30 * ecological_memory +
        0.20 * (1 - maintenance_backlog) +
        0.15 * (1 - climate_pressure)
    )

    threshold_distance = clamp01(
        1 -
        0.30 * maintenance_backlog -
        0.28 * climate_pressure -
        0.22 * (1 - public_trust) -
        0.20 * (1 - ecological_memory)
    )

    hidden_risk = clamp01(
        0.32 * maintenance_backlog +
        0.30 * climate_pressure +
        0.22 * (1 - public_trust) +
        0.16 * (1 - ecological_memory)
    )

    fast_shock = (t == 72 || t == 96) ? 0.32 : 0.0

    system_function = clamp01(
        system_function -
        0.22 * hidden_risk -
        0.46 * fast_shock +
        0.18 * adaptive_capacity
    )

    @printf("%d,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f\n",
        t, maintenance_backlog, public_trust, ecological_memory, climate_pressure,
        adaptive_capacity, threshold_distance, hidden_risk, fast_shock, system_function)
end
