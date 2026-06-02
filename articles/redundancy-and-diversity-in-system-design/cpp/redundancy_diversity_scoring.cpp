#include <iostream>
#include <string>
#include <vector>

struct Strategy {
    std::string name;
    double redundancy;
    double diversity;
    double response_diversity;
    double coordination_capacity;
    double justice_contribution;
    double maintenance_reliability;
    double common_mode_risk;
};

double resilience_value(const Strategy& s) {
    return 0.22 * s.redundancy
        + 0.18 * s.diversity
        + 0.22 * s.response_diversity
        + 0.13 * s.coordination_capacity
        + 0.10 * s.justice_contribution
        + 0.07 * s.maintenance_reliability
        - 0.08 * s.common_mode_risk;
}

int main() {
    std::vector<Strategy> strategies = {
        {"Distributed Backup Infrastructure Network", 8.8, 7.4, 7.8, 7.6, 7.2, 7.5, 3.8},
        {"Multi-Supplier and Multi-Technology System Design", 7.9, 8.9, 8.6, 7.3, 7.4, 7.2, 3.5},
        {"Cross-Trained Organizational Response Model", 8.2, 8.1, 8.4, 8.2, 7.8, 7.9, 4.0}
    };

    std::cout << "strategy,resilience_value,common_mode_risk\n";
    for (const auto& s : strategies) {
        std::cout << s.name << "," << resilience_value(s) << "," << s.common_mode_risk << "\n";
    }

    return 0;
}
