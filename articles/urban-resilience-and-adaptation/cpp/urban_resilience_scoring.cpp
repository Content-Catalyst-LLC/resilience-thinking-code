#include <iostream>
#include <string>
#include <vector>

struct Strategy {
    std::string name;
    double exposure;
    double vulnerability;
    double service;
    double adaptive;
    double ecology;
    double equity;
    double maladaptation;
};

double resilience_value(const Strategy& s) {
    return 0.16 * s.exposure
        + 0.17 * s.vulnerability
        + 0.17 * s.service
        + 0.15 * s.adaptive
        + 0.14 * s.ecology
        + 0.15 * s.equity
        - 0.06 * s.maladaptation;
}

int main() {
    std::vector<Strategy> strategies = {
        {"Heat-Resilient Housing Retrofit Program", 7.8, 8.8, 8.1, 8.0, 7.4, 8.6, 2.9},
        {"Community Resilience Hub Network", 7.2, 8.5, 8.0, 8.6, 7.6, 8.9, 2.6},
        {"Anti-Displacement Climate Adaptation Framework", 7.5, 8.9, 7.7, 8.4, 7.5, 9.1, 2.5}
    };

    std::cout << "strategy,resilience_value,maladaptation_risk\n";
    for (const auto& s : strategies) {
        std::cout << s.name << "," << resilience_value(s) << "," << s.maladaptation << "\n";
    }

    return 0;
}
