# Feedback delay model
#
# Run:
#   julia julia/feedback_delay_model.jl

using Printf

function simulate_feedback(; steps=80, gain=0.03, balancing=0.14, target=75.0, delay=5)
    x = fill(20.0, steps + delay + 2)

    println("time,value,target,gain,balancing,delay,overshoot")

    for t in 2:steps
        delayed_index = max(1, t - delay)
        x[t] = x[t - 1] + gain * x[t - 1] - balancing * (x[delayed_index] - target)
        overshoot = max(0.0, x[t] - target)
        @printf("%d,%.6f,%.6f,%.6f,%.6f,%d,%.6f\n", t, x[t], target, gain, balancing, delay, overshoot)
    end
end

simulate_feedback()
