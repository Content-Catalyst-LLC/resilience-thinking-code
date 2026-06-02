#include <iostream>
#include <string>
#include <vector>

struct Pathway {
    std::string name;
    double resilience;
    double ecology;
    double inclusion;
    double economy;
    double governance;
    double adaptive;
    double pressure;
    double burden;
};

double viability_value(const Pathway& p) {
    return 0.18 * p.resilience
        + 0.17 * p.ecology
        + 0.16 * p.inclusion
        + 0.14 * p.economy
        + 0.14 * p.governance
        + 0.15 * p.adaptive
        - 0.04 * p.pressure
        - 0.02 * p.burden;
}

int main() {
    std::vector<Pathway> pathways = {
        {"Distributed Renewable Infrastructure", 8.5, 8.2, 7.8, 8.0, 7.8, 8.4, 4.0, 3.5},
        {"Climate-Resilient Food and Water Strategy", 8.7, 8.4, 8.1, 8.2, 8.1, 8.6, 3.9, 3.4},
        {"Ecosystem Restoration and Livelihood Diversification", 8.4, 9.0, 8.2, 7.9, 8.0, 8.7, 3.5, 3.2}
    };

    std::cout << "pathway,viability_value,resource_pressure,implementation_burden\n";
    for (const auto& p : pathways) {
        std::cout << p.name << "," << viability_value(p) << "," << p.pressure << "," << p.burden << "\n";
    }

    return 0;
}
