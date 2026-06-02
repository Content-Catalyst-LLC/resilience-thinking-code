#include <iostream>
#include <string>
#include <vector>

struct Strategy {
    std::string name;
    double modularity;
    double redundancy;
    double dependency_mapping;
    double isolation_capacity;
    double coordination_readiness;
    double justice_protection;
    double common_mode_risk;
};

double containment_value(const Strategy& s) {
    return 0.18 * s.modularity
        + 0.16 * s.redundancy
        + 0.16 * s.dependency_mapping
        + 0.18 * s.isolation_capacity
        + 0.14 * s.coordination_readiness
        + 0.10 * s.justice_protection
        - 0.08 * s.common_mode_risk;
}

int main() {
    std::vector<Strategy> strategies = {
        {"Microgrid and Critical Service Islanding", 8.7, 8.4, 7.6, 8.8, 7.6, 7.3, 3.5},
        {"Regional Supply Network Diversification", 7.8, 8.2, 7.9, 7.4, 7.2, 7.6, 3.8},
        {"Neighborhood Resilience Hub Network", 8.1, 7.9, 7.5, 7.8, 8.0, 8.6, 3.7}
    };

    std::cout << "strategy,containment_value,common_mode_risk\n";
    for (const auto& s : strategies) {
        std::cout << s.name << "," << containment_value(s) << "," << s.common_mode_risk << "\n";
    }

    return 0;
}
