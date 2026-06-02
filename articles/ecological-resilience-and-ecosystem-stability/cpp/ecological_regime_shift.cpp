#include <cmath>
#include <iostream>
#include <string>

int main() {
    const int steps = 140;
    double x = -0.9;
    const double r = 1.1;
    const double dt = 0.05;

    std::cout << "time,external_pressure,ecosystem_state,basin_width,disturbance_load,regenerative_capacity,resilience_margin,threshold_flag\n";
    for (int t = 1; t <= steps; ++t) {
        double pressure = -0.6 + 1.45 * (static_cast<double>(t - 1) / (steps - 1));
        if (t > 1) x = x + dt * (r * x - std::pow(x, 3) + pressure);
        double basin_width = 0.85 - 0.47 * (static_cast<double>(t - 1) / (steps - 1));
        double disturbance_load = 0.10 + 0.68 * (static_cast<double>(t - 1) / (steps - 1));
        double regenerative_capacity = 0.36 + 0.18 * std::sin(t / 18.0);
        double margin = basin_width - disturbance_load + regenerative_capacity;
        std::string flag = margin < 0.15 ? "threshold risk" : "viable margin";
        std::cout << t << "," << pressure << "," << x << "," << basin_width << "," << disturbance_load << "," << regenerative_capacity << "," << margin << "," << flag << "\n";
    }
    return 0;
}
