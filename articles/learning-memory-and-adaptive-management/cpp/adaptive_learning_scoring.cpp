#include <iostream>
#include <string>
#include <vector>

struct Strategy {
    std::string name;
    double monitoring_quality;
    double memory_retention;
    double feedback_use;
    double governance_flexibility;
    double community_knowledge;
    double justice_protection;
    double implementation_reliability;
    double forgetting_pressure;
};

double adaptive_learning_value(const Strategy& s) {
    return 0.15 * s.monitoring_quality
        + 0.15 * s.memory_retention
        + 0.17 * s.feedback_use
        + 0.14 * s.governance_flexibility
        + 0.12 * s.community_knowledge
        + 0.11 * s.justice_protection
        + 0.09 * s.implementation_reliability
        - 0.07 * s.forgetting_pressure;
}

int main() {
    std::vector<Strategy> strategies = {
        {"Ecological Monitoring and Threshold Review", 8.6, 8.2, 8.1, 7.5, 7.4, 7.5, 7.8, 3.2},
        {"Community Knowledge and Early Warning Network", 7.9, 8.3, 8.0, 7.7, 9.0, 8.8, 7.6, 2.8},
        {"Adaptive Governance Decision-Trigger Framework", 8.1, 7.9, 8.8, 8.7, 7.9, 8.0, 8.0, 3.1}
    };

    std::cout << "strategy,adaptive_learning_value,forgetting_pressure\n";
    for (const auto& s : strategies) {
        std::cout << s.name << "," << adaptive_learning_value(s) << "," << s.forgetting_pressure << "\n";
    }

    return 0;
}
