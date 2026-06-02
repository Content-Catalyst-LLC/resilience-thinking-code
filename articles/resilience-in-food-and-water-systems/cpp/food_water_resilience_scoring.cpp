#include <iostream>
#include <string>
#include <vector>

struct Strategy {
    std::string name;
    double availability;
    double access;
    double stability;
    double quality;
    double adaptive_capacity;
    double equity_protection;
    double resource_depletion_risk;
};

double resilience_value(const Strategy& s) {
    return 0.17 * s.availability
        + 0.17 * s.access
        + 0.16 * s.stability
        + 0.14 * s.quality
        + 0.16 * s.adaptive_capacity
        + 0.14 * s.equity_protection
        - 0.06 * s.resource_depletion_risk;
}

int main() {
    std::vector<Strategy> strategies = {
        {"Watershed Restoration and Recharge Program", 8.3, 7.4, 7.9, 8.6, 8.5, 7.7, 2.7},
        {"Community Water Governance and Access Reform", 7.6, 8.8, 7.7, 8.1, 8.7, 8.9, 2.8},
        {"Safe Water Treatment and Sanitation Resilience Plan", 7.8, 8.5, 8.1, 8.9, 8.0, 8.6, 3.0}
    };

    std::cout << "strategy,resilience_value,resource_depletion_risk\n";
    for (const auto& s : strategies) {
        std::cout << s.name << "," << resilience_value(s) << "," << s.resource_depletion_risk << "\n";
    }

    return 0;
}
