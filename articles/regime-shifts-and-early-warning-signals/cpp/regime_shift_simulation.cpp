#include <algorithm>
#include <cmath>
#include <iostream>
#include <string>

double update_state(double x, double pressure, double r = 1.2, double dt = 0.05) {
    return x + dt * (r * x - x * x * x + pressure);
}

int main() {
    const int steps = 180;
    const double start = -0.75;
    const double end = 0.85;

    double x = -0.90;

    std::cout << "time,pressure,state,regime\n";

    for (int t = 1; t <= steps; ++t) {
        double pressure = start + (end - start) * (t - 1) / (steps - 1);
        if (t > 1) {
            x = update_state(x, pressure);
        }

        std::string regime = x >= 0.0 ? "upper regime" : "lower regime";
        std::cout << t << "," << pressure << "," << x << "," << regime << "\n";
    }

    return 0;
}
