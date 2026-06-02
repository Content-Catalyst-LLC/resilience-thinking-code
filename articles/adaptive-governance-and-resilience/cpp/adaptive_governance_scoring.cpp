#include <iostream>
#include <string>
#include <vector>

struct Strategy {
    std::string name;
    double learning;
    double flexibility;
    double coordination;
    double knowledge;
    double legitimacy;
    double accountability;
    double equity;
    double burden;
};

double governance_value(const Strategy& s) {
    return 0.15 * s.learning
        + 0.14 * s.flexibility
        + 0.14 * s.coordination
        + 0.14 * s.knowledge
        + 0.14 * s.legitimacy
        + 0.14 * s.accountability
        + 0.15 * s.equity
        - 0.02 * s.burden;
}

int main() {
    std::vector<Strategy> strategies = {
        {"Adaptive Pathways and Decision Triggers", 8.6, 8.9, 7.9, 8.1, 7.9, 8.0, 7.8, 3.2},
        {"Community Knowledge Co-Production Platform", 8.3, 7.6, 8.0, 9.1, 8.8, 8.3, 8.7, 3.1},
        {"Equity Accountability and Rights Safeguard", 8.1, 7.7, 7.9, 8.4, 8.7, 9.1, 9.2, 3.0}
    };

    std::cout << "strategy,adaptive_governance_value,implementation_burden\n";
    for (const auto& s : strategies) {
        std::cout << s.name << "," << governance_value(s) << "," << s.burden << "\n";
    }

    return 0;
}
