using Printf

x = -0.9
steps = 140
r = 1.1
dt = 0.05

println("time,external_pressure,ecosystem_state,basin_width,disturbance_load,regenerative_capacity,resilience_margin,threshold_flag")

for t in 1:steps
    pressure = -0.6 + 1.45 * (t - 1) / (steps - 1)
    if t > 1
        global x = x + dt * (r*x - x^3 + pressure)
    end
    basin_width = 0.85 - 0.47 * (t - 1) / (steps - 1)
    disturbance_load = 0.10 + 0.68 * (t - 1) / (steps - 1)
    regenerative_capacity = 0.36 + 0.18 * sin(t / 18.0)
    margin = basin_width - disturbance_load + regenerative_capacity
    flag = margin < 0.15 ? "threshold risk" : "viable margin"
    @printf("%d,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f,%s\n", t, pressure, x, basin_width, disturbance_load, regenerative_capacity, margin, flag)
end
