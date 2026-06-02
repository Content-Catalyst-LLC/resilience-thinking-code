#include <iostream>
#include <string>
#include <vector>

struct Strategy {
    std::string name;
    double participation;
    double diversity;
    double influence;
    double trust;
    double protection;
    double reciprocity;
    double accountability;
    double burden;
};

double knowledge_value(const Strategy& s) {
    return 0.14 * s.participation
        + 0.14 * s.diversity
        + 0.15 * s.influence
        + 0.14 * s.trust
        + 0.14 * s.protection
        + 0.14 * s.reciprocity
        + 0.15 * s.accountability
        - 0.02 * s.burden;
}

int main() {
    std::vector<Strategy> strategies = {
        {"Participatory Risk Mapping and Action Triggers", 8.7, 8.8, 8.4, 8.2, 8.0, 8.3, 8.5, 3.2},
        {"Indigenous Knowledge Governance Protocol", 8.4, 9.2, 8.8, 8.9, 9.4, 9.0, 8.7, 3.5},
        {"Funded Community Resilience Advisory Council", 9.0, 8.7, 9.1, 8.8, 8.5, 8.9, 9.0, 3.3}
    };

    std::cout << "strategy,knowledge_integration_value,implementation_burden\n";
    for (const auto& s : strategies) {
        std::cout << s.name << "," << knowledge_value(s) << "," << s.burden << "\n";
    }

    return 0;
}
