#include <algorithm>
#include <cmath>
#include <iostream>
#include <string>

int main() {
    const int steps = 100;
    double functional_output = 2.4;
    double redundancy = 4.0;
    double response_diversity = 0.055;
    const double memory = 0.60;
    const double connectivity = 0.54;
    const double exposure = 0.66;

    std::cout << "time,functional_output,redundancy,response_diversity,disturbance,resilience_margin,threshold_flag\n";

    for (int t = 1; t <= steps; ++t) {
        double seasonal = 0.055 + 0.025 * std::sin(t / 9.0);
        double shock = (t == 24 || t == 47 || t == 70 || t == 88) ? 0.32 : 0.0;
        double disturbance = seasonal + shock + 0.18 * exposure;

        functional_output = std::max(0.0, functional_output - 0.030 * disturbance + 0.010 * memory);
        redundancy = std::max(0.0, redundancy - 0.018 * disturbance + 0.004 * connectivity);
        response_diversity = std::max(0.0, response_diversity - 0.003 * disturbance + 0.001 * memory);

        double margin = functional_output + 0.055 * redundancy + response_diversity + memory + connectivity - disturbance - exposure;
        std::string flag = margin < 1.20 ? "threshold risk" : "viable margin";

        std::cout << t << "," << functional_output << "," << redundancy << "," << response_diversity << "," << disturbance << "," << margin << "," << flag << "\n";
    }

    return 0;
}
