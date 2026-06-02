#include <iostream>
#include <string>
#include <vector>

struct Pathway {
    std::string name;
    double adaptive_support;
    double transformability;
    double governance_readiness;
    double justice_contribution;
    double ecological_viability;
    double legitimacy;
    double resource_feasibility;
    double structural_risk;
};

double readiness(const Pathway& p) {
    return 0.18 * p.adaptive_support
        + 0.20 * p.transformability
        + 0.18 * p.governance_readiness
        + 0.16 * p.justice_contribution
        + 0.14 * p.ecological_viability
        + 0.08 * p.legitimacy
        + 0.06 * p.resource_feasibility
        - 0.10 * p.structural_risk;
}

int main() {
    std::vector<Pathway> pathways = {
        {"Energy System Transition", 8.0, 8.8, 7.4, 7.1, 8.7, 7.5, 7.2, 4.2},
        {"Climate-Resilient Urban Redesign", 8.3, 8.5, 7.8, 8.4, 8.1, 7.8, 7.0, 4.0},
        {"Institutional Governance Reform", 7.6, 8.7, 8.4, 8.2, 7.2, 8.1, 6.8, 4.1}
    };

    std::cout << "pathway,transformation_readiness\n";
    for (const auto& p : pathways) {
        std::cout << p.name << "," << readiness(p) << "\n";
    }

    return 0;
}
