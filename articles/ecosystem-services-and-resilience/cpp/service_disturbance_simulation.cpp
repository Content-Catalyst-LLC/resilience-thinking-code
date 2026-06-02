#include <algorithm>
#include <cmath>
#include <iostream>
#include <string>

int main() {
    const int steps = 100;
    double condition = 0.62;
    double functional_capacity = 0.58;
    const double redundancy = 0.48;
    const double memory = 0.52;
    const double governance = 0.55;
    const double exposure = 0.70;
    const double access = 0.52;

    std::cout << "time,disturbance,ecosystem_condition,functional_capacity,service_flow,resilience_margin,threshold_flag\n";

    for (int t = 1; t <= steps; ++t) {
        double seasonal = 0.04 + 0.020 * std::sin(t / 8.0);
        double shock = (t == 22 || t == 45 || t == 67 || t == 84) ? 0.25 : 0.0;
        double disturbance = seasonal + shock + 0.18 * exposure;

        double repair = 0.010 * redundancy + 0.009 * memory + 0.008 * governance;
        double erosion = disturbance * (0.42 + exposure);

        condition = std::max(0.01, std::min(1.0, condition - 0.045 * erosion + repair));
        functional_capacity = std::max(0.01, std::min(1.0, functional_capacity - 0.030 * erosion + 0.006 * redundancy));

        double service_flow = condition * functional_capacity * (1.0 - 0.35 * disturbance);
        service_flow = std::max(0.0, std::min(1.0, service_flow));

        double margin = condition + functional_capacity + redundancy + memory + governance + 0.35 * access - disturbance - exposure;
        std::string flag = margin < 1.30 ? "threshold risk" : "viable margin";

        std::cout << t << "," << disturbance << "," << condition << "," << functional_capacity << "," << service_flow << "," << margin << "," << flag << "\n";
    }

    return 0;
}
