#include <iostream>
#include <string>
#include <vector>

struct Strategy {
    std::string name;
    double social;
    double institution;
    double access;
    double economy;
    double information;
    double adaptive;
    double equity;
    double burden;
};

double resilience_value(const Strategy& s) {
    return 0.14 * s.social
        + 0.14 * s.institution
        + 0.14 * s.access
        + 0.13 * s.economy
        + 0.13 * s.information
        + 0.15 * s.adaptive
        + 0.15 * s.equity
        - 0.02 * s.burden;
}

int main() {
    std::vector<Strategy> strategies = {
        {"Neighborhood Mutual Aid and Preparedness Network", 8.9, 7.5, 7.1, 7.6, 7.9, 8.2, 8.1, 2.7},
        {"Inclusive Community Governance and Adaptation Forum", 8.4, 8.3, 7.4, 7.8, 7.8, 8.6, 8.8, 3.1},
        {"Community Health and Care Continuity Network", 8.6, 8.0, 7.8, 7.5, 8.0, 8.1, 8.7, 3.0}
    };

    std::cout << "strategy,resilience_value,implementation_burden\n";
    for (const auto& s : strategies) {
        std::cout << s.name << "," << resilience_value(s) << "," << s.burden << "\n";
    }

    return 0;
}
