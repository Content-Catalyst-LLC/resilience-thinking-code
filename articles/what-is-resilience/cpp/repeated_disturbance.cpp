#include <algorithm>
#include <iostream>
#include <vector>

double clamp(double value, double low, double high) {
    return std::max(low, std::min(value, high));
}

int main() {
    const int steps = 60;
    const double adaptive_capacity = 0.72;
    const double threshold_distance = 0.63;
    const double exposure = 0.58;
    const double sensitivity = 0.54;
    const double redundancy = 0.61;
    const double modularity = 0.56;

    double viability = 1.0;
    double risk_pressure = 0.55 * exposure + 0.45 * sensitivity;

    std::vector<double> disturbance;
    for (int t = 1; t <= steps; ++t) {
        double d = 0.055;
        if (t == 12) d += 0.20;
        if (t == 24) d += 0.28;
        if (t == 37) d += 0.23;
        if (t == 48) d += 0.31;
        disturbance.push_back(d);
    }

    std::cout << "time_step,viability,margin\n";
    for (int t = 0; t < steps; ++t) {
        double load = disturbance[t] * (0.65 + exposure) * (0.55 + sensitivity);
        double protection = 0.35 * redundancy + 0.25 * modularity;
        double adaptive_response = 0.03 * adaptive_capacity;
        double net_impact = load * (1.0 - 0.45 * protection);

        viability = clamp(viability - net_impact + adaptive_response, 0.0, 1.25);
        double margin = viability + threshold_distance - risk_pressure;

        std::cout << (t + 1) << "," << viability << "," << margin << "\n";
    }

    return 0;
}
