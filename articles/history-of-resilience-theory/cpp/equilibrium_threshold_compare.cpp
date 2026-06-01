#include <cmath>
#include <iostream>

int main() {
    const int steps = 160;
    double x_star = 0.0;
    double a = 0.10;
    double equilibrium = 1.0;

    double threshold = -0.9;
    double r = 1.1;
    double dt = 0.05;

    std::cout << "time,equilibrium_state,pressure,threshold_state\n";

    for (int t = 1; t <= steps; ++t) {
        double pressure = -0.45 + 1.30 * (static_cast<double>(t - 1) / (steps - 1));

        if (t > 1) {
            equilibrium = equilibrium - a * (equilibrium - x_star);
            threshold = threshold + dt * (r * threshold - std::pow(threshold, 3) + pressure);
        }

        std::cout << t << "," << equilibrium << "," << pressure << "," << threshold << "\n";
    }

    return 0;
}
