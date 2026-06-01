#include <cmath>
#include <iostream>

int main() {
    const int steps = 120;
    double engineering = 1.0;
    double x_star = 0.0;
    double return_rate = 0.18;

    double ecological = -0.9;
    double r = 1.1;
    double dt = 0.05;

    std::cout << "time,engineering_state,pressure,ecological_state\n";

    for (int t = 1; t <= steps; ++t) {
        double pressure = -0.45 + 1.30 * (static_cast<double>(t - 1) / (steps - 1));

        if (t > 1) {
            engineering = engineering - return_rate * (engineering - x_star);
            ecological = ecological + dt * (r * ecological - std::pow(ecological, 3) + pressure);
        }

        std::cout << t << "," << engineering << "," << pressure << "," << ecological << "\n";
    }

    return 0;
}
