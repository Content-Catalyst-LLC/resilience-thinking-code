#include <iostream>
#include <string>
#include <vector>

struct Strategy {
    std::string name;
    double exposure_reduction;
    double vulnerability_reduction;
    double adaptive_capacity;
    double recovery_capacity;
    double transformative_capacity;
    double justice_protection;
    double maladaptation_risk;
};

double climate_resilience_value(const Strategy& s) {
    return 0.16 * s.exposure_reduction
        + 0.16 * s.vulnerability_reduction
        + 0.16 * s.adaptive_capacity
        + 0.15 * s.recovery_capacity
        + 0.15 * s.transformative_capacity
        + 0.14 * s.justice_protection
        - 0.08 * s.maladaptation_risk;
}

int main() {
    std::vector<Strategy> strategies = {
        {"Heat-Resilient Urban Redesign", 8.2, 7.9, 8.0, 7.8, 8.1, 8.0, 3.5},
        {"Coastal Ecosystem-Based Adaptation Program", 8.5, 8.3, 7.9, 7.6, 8.4, 7.8, 3.0},
        {"Community-Led Floodplain Adaptation", 8.3, 8.5, 8.2, 7.9, 8.4, 8.8, 2.8}
    };

    std::cout << "strategy,climate_resilience_value,maladaptation_risk\n";
    for (const auto& s : strategies) {
        std::cout << s.name << "," << climate_resilience_value(s) << "," << s.maladaptation_risk << "\n";
    }

    return 0;
}
