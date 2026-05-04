#include <iostream>
#include <vector>
#include <algorithm>

std::vector<double> simulate_viability(double initial, double disturbance, double adaptive_response, int steps) {
    std::vector<double> viability;
    viability.push_back(initial);

    for (int t = 1; t < steps; ++t) {
        double next = viability.back() - disturbance + adaptive_response;
        next = std::max(0.0, std::min(1.5, next));
        viability.push_back(next);
    }

    return viability;
}

int main() {
    auto values = simulate_viability(1.0, 0.08, 0.09, 30);

    std::cout << "Viability simulation\n";

    for (size_t i = 0; i < values.size(); ++i) {
        std::cout << "time=" << i << ", viability=" << values[i] << "\n";
    }

    return 0;
}
