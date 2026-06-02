#include <cmath>
#include <iostream>
#include <string>
#include <vector>

double update_state(double x, double pressure, double r = 1.2, double dt = 0.05) {
    return x + dt * (r * x - x * x * x + pressure);
}

int main() {
    const int steps = 160;
    const double start = -0.8;
    const double end = 0.8;

    std::cout << "direction,step,pressure,state,regime\n";

    double x = -0.9;
    for (int i = 0; i < steps; ++i) {
        double pressure = start + (end - start) * i / (steps - 1);
        if (i > 0) {
            x = update_state(x, pressure);
        }
        std::string regime = x >= 0.0 ? "upper regime" : "lower regime";
        std::cout << "Increasing Pressure," << (i + 1) << "," << pressure << "," << x << "," << regime << "\n";
    }

    double xb = x;
    for (int i = 0; i < steps; ++i) {
        double pressure = end + (start - end) * i / (steps - 1);
        if (i > 0) {
            xb = update_state(xb, pressure);
        }
        std::string regime = xb >= 0.0 ? "upper regime" : "lower regime";
        std::cout << "Decreasing Pressure," << (i + 1) << "," << pressure << "," << xb << "," << regime << "\n";
    }

    return 0;
}
