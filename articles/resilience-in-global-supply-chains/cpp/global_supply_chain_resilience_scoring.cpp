#include <iostream>
#include <string>
#include <vector>

struct Strategy {
    std::string name;
    double redundancy;
    double flexibility;
    double visibility;
    double coordination;
    double adaptation;
    double equity;
    double infrastructure;
    double exposure;
    double burden;
};

double supply_chain_value(const Strategy& s) {
    return 0.13 * s.redundancy
        + 0.13 * s.flexibility
        + 0.13 * s.visibility
        + 0.13 * s.coordination
        + 0.13 * s.adaptation
        + 0.13 * s.equity
        + 0.13 * s.infrastructure
        - 0.06 * s.exposure
        - 0.03 * s.burden;
}

int main() {
    std::vector<Strategy> strategies = {
        {"Supplier Diversification and Qualification Program", 8.8, 8.2, 7.6, 8.0, 8.4, 7.9, 7.6, 4.0, 3.2},
        {"Multi-Route Logistics and Chokepoint Redesign", 8.1, 8.8, 8.0, 8.2, 8.5, 7.8, 8.5, 4.0, 3.4},
        {"Fair Supplier Finance and Labor Continuity Program", 7.7, 8.1, 7.5, 8.3, 8.2, 9.0, 7.6, 3.8, 3.0}
    };

    std::cout << "strategy,supply_chain_resilience_value,implementation_burden\n";
    for (const auto& s : strategies) {
        std::cout << s.name << "," << supply_chain_value(s) << "," << s.burden << "\n";
    }

    return 0;
}
