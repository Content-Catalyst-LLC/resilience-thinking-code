#include <iostream>
#include <string>
#include <vector>

struct Strategy {
    std::string name;
    double hazard_reduction;
    double exposure_reduction;
    double vulnerability_reduction;
    double capacity_enhancement;
    double justice_protection;
    double maladaptation_risk;
};

double drr_value(const Strategy& s) {
    return 0.17 * s.hazard_reduction
        + 0.18 * s.exposure_reduction
        + 0.18 * s.vulnerability_reduction
        + 0.17 * s.capacity_enhancement
        + 0.18 * s.justice_protection
        - 0.12 * s.maladaptation_risk;
}

int main() {
    std::vector<Strategy> strategies = {
        {"Floodplain Land-Use Restriction", 7.4, 8.6, 7.5, 6.9, 7.2, 3.4},
        {"Community Early Warning Network", 6.8, 7.1, 8.1, 8.7, 8.0, 2.6},
        {"Equitable Recovery and Housing Protection Program", 6.7, 7.4, 8.9, 8.3, 9.0, 2.4}
    };

    std::cout << "strategy,drr_value,maladaptation_risk\n";
    for (const auto& s : strategies) {
        std::cout << s.name << "," << drr_value(s) << "," << s.maladaptation_risk << "\n";
    }

    return 0;
}
