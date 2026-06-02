#include <algorithm>
#include <cmath>
#include <iostream>
#include <string>

int main() {
    const int steps = 80;
    double capacity = 0.58;
    double vulnerability = 0.62;
    double rigidity = 0.55;
    double exposure = 0.70;
    double slack = 0.50;
    double trust = 0.57;
    double viability = 1.0;

    std::cout << "time,disturbance,adaptive_capacity,rigidity,response_space,viability,threshold_flag\n";

    for (int t = 1; t <= steps; ++t) {
        double seasonal = 0.04 + 0.025 * std::sin(t / 8.0);
        double shock = (t % 10 == 0) ? 0.22 : 0.0;
        double disturbance = 0.26 + seasonal + shock + 0.18 * exposure;

        capacity = std::max(0.0, std::min(1.2, capacity + 0.010 + 0.006 * 0.50 - 0.010 * rigidity));
        rigidity = std::max(0.0, std::min(1.0, rigidity + 0.010 + 0.004 * disturbance - 0.006 * 0.50));

        double response_space = capacity + 0.35 * slack + 0.25 * trust - rigidity - 0.25 * vulnerability;

        viability = viability - 0.46 * disturbance + 0.25 * capacity + 0.08 * response_space - 0.12 * rigidity;
        viability = std::max(0.0, std::min(1.2, viability));

        std::string flag = viability < 0.45 ? "threshold risk" : "viable margin";
        std::cout << t << "," << disturbance << "," << capacity << "," << rigidity << "," << response_space << "," << viability << "," << flag << "\n";
    }

    return 0;
}
