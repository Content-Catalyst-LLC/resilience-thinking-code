#include <cmath>
#include <iostream>
#include <string>

double risk_pressure(double hazard, double exposure, double vulnerability, double adaptive) {
    return hazard * exposure * vulnerability * (1.0 - 0.55 * adaptive);
}

double governance_capacity(double trust, double participation, double knowledge, double coordination, double transparency, double accountability) {
    return 0.18 * trust + 0.17 * participation + 0.17 * knowledge + 0.18 * coordination + 0.15 * transparency + 0.15 * accountability;
}

int main() {
    const int steps = 84;
    double hazard = 0.74;
    double exposure = 0.78;
    double vulnerability = 0.64;
    double buffer = 0.55;
    double adaptive = 0.58;
    double learning = 0.52;

    double rp = risk_pressure(hazard, exposure, vulnerability, adaptive);
    double gc = governance_capacity(0.46, 0.42, 0.50, 0.48, 0.44, 0.46);
    double margin = buffer + adaptive + learning + gc - rp - vulnerability;

    std::cout << "time,disturbance,resilience_margin,threshold_flag\n";

    for (int t = 1; t <= steps; ++t) {
        double disturbance = 0.05 + 0.025 * std::sin(t / 7.0);
        if (t % 8 == 0) {
            disturbance += 0.76;
        }

        double governance_response = 0.018 * gc * (1.0 - 0.35 * 0.72);
        double adaptive_response = 0.014 * adaptive + 0.010 * learning;
        double vulnerability_amplification = 0.020 * vulnerability + 0.010 * exposure;
        double disturbance_effect = disturbance * (0.35 + 0.55 * exposure);

        margin = margin - disturbance_effect - vulnerability_amplification + governance_response + adaptive_response;
        std::string flag = margin < 0.75 ? "threshold risk" : "viable margin";

        std::cout << t << "," << disturbance << "," << margin << "," << flag << "\n";
    }

    return 0;
}
