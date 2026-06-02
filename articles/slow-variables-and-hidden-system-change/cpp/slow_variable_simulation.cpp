#include <algorithm>
#include <iostream>

double clamp01(double x) {
    return std::max(0.0, std::min(1.0, x));
}

int main() {
    const int steps = 120;

    double maintenance_backlog = 0.25;
    double public_trust = 0.72;
    double ecological_memory = 0.68;
    double climate_pressure = 0.22;
    double system_function = 0.86;

    std::cout << "time,maintenance_backlog,public_trust,ecological_memory,climate_pressure,adaptive_capacity,threshold_distance,hidden_risk,fast_shock,system_function\n";

    for (int t = 1; t <= steps; ++t) {
        maintenance_backlog = clamp01(maintenance_backlog + 0.006);
        public_trust = clamp01(public_trust - 0.0035);
        ecological_memory = clamp01(ecological_memory - 0.0025);
        climate_pressure = clamp01(climate_pressure + 0.0045);

        double adaptive_capacity = clamp01(
            0.35 * public_trust +
            0.30 * ecological_memory +
            0.20 * (1.0 - maintenance_backlog) +
            0.15 * (1.0 - climate_pressure)
        );

        double threshold_distance = clamp01(
            1.0 -
            0.30 * maintenance_backlog -
            0.28 * climate_pressure -
            0.22 * (1.0 - public_trust) -
            0.20 * (1.0 - ecological_memory)
        );

        double hidden_risk = clamp01(
            0.32 * maintenance_backlog +
            0.30 * climate_pressure +
            0.22 * (1.0 - public_trust) +
            0.16 * (1.0 - ecological_memory)
        );

        double fast_shock = (t == 72 || t == 96) ? 0.32 : 0.0;

        system_function = clamp01(
            system_function -
            0.22 * hidden_risk -
            0.46 * fast_shock +
            0.18 * adaptive_capacity
        );

        std::cout << t << "," << maintenance_backlog << "," << public_trust << ","
                  << ecological_memory << "," << climate_pressure << ","
                  << adaptive_capacity << "," << threshold_distance << ","
                  << hidden_risk << "," << fast_shock << "," << system_function << "\n";
    }

    return 0;
}
