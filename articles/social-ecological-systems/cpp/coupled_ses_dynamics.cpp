#include <algorithm>
#include <iostream>
#include <string>

int main() {
    const int steps = 90;
    double ecology = 0.75;
    double social_pressure = 0.55;
    const double governance = 0.60;
    const double livelihood_pressure = 0.55;
    const double climate_pressure = 0.58;
    const double market_shock = 0.38;

    const double r = 0.08;
    const double k = 1.0;
    const double q = 0.10;

    std::cout << "time,ecology,social_pressure,extraction,resilience_margin,threshold_flag\n";

    for (int t = 1; t <= steps; ++t) {
        double extraction = q * social_pressure * ecology;
        double ecological_growth = r * ecology * (1.0 - ecology / k);
        double climate_effect = 0.022 * climate_pressure;
        double governance_repair = 0.017 * governance;

        ecology = ecology + ecological_growth - extraction - climate_effect + governance_repair;
        ecology = std::max(0.01, std::min(1.20, ecology));

        double market_pulse = (t == 20 || t == 42 || t == 68) ? 0.035 * market_shock : 0.0;
        social_pressure = social_pressure + 0.050 * livelihood_pressure + 0.028 * (1.0 - governance) + market_pulse - 0.043 * ecology;
        social_pressure = std::max(0.05, std::min(1.20, social_pressure));

        double margin = ecology + governance + 0.35 * (1.0 - livelihood_pressure) - social_pressure - 0.35 * climate_pressure;
        std::string flag = margin < 0.20 ? "threshold risk" : "viable margin";

        std::cout << t << "," << ecology << "," << social_pressure << "," << extraction << "," << margin << "," << flag << "\n";
    }

    return 0;
}
