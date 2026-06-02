# Network cascade diagnostic example
#
# Run:
#   julia julia/network_cascade_example.jl

using Printf

nodes = [
    ("Power", 0.62, 0.55, 0.42, 0.60),
    ("Water", 0.58, 0.48, 0.46, 0.68),
    ("Communications", 0.55, 0.52, 0.40, 0.54),
    ("Hospitals", 0.60, 0.50, 0.44, 0.74),
    ("Transportation", 0.52, 0.46, 0.48, 0.58)
]

function cascade_pressure(coupling, redundancy, isolation_capacity, common_mode_exposure)
    return clamp(coupling + 0.35 * common_mode_exposure - 0.30 * redundancy - 0.25 * isolation_capacity, 0.02, 0.95)
end

println("node,redundancy,isolation_capacity,common_mode_exposure,justice_sensitivity,example_cascade_pressure")

for n in nodes
    name, redundancy, isolation_capacity, common_mode, justice = n
    pressure = cascade_pressure(0.66, redundancy, isolation_capacity, common_mode)
    @printf("%s,%.2f,%.2f,%.2f,%.2f,%.5f\n", name, redundancy, isolation_capacity, common_mode, justice, pressure)
end
