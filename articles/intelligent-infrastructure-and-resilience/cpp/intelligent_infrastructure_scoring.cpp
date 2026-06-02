#include <iostream>
#include <string>
#include <vector>

struct Strategy {
    std::string name;
    double monitoring;
    double maintenance;
    double cyber;
    double twin;
    double redundancy;
    double climate;
    double governance;
    double equity;
    double ecology;
    double fragility;
    double implementation;
};

double infrastructure_value(const Strategy& s) {
    return 0.10 * s.monitoring
        + 0.11 * s.maintenance
        + 0.11 * s.cyber
        + 0.10 * s.twin
        + 0.11 * s.redundancy
        + 0.11 * s.climate
        + 0.12 * s.governance
        + 0.12 * s.equity
        + 0.10 * s.ecology
        - 0.04 * s.fragility
        - 0.04 * s.implementation;
}

int main() {
    std::vector<Strategy> strategies = {
        {"Digital Twin and Scenario Stress Testing", 8.3, 8.5, 8.1, 9.3, 8.3, 8.6, 8.5, 8.1, 8.2, 3.0, 3.7},
        {"Predictive Maintenance and Asset Renewal", 8.5, 9.3, 8.2, 8.6, 8.4, 8.4, 8.4, 8.2, 8.0, 2.8, 3.8},
        {"Equity-Centered Climate Adaptation Portfolio", 8.2, 8.1, 8.0, 8.4, 8.5, 9.3, 8.9, 9.3, 9.0, 2.6, 3.9}
    };

    std::cout << "strategy,infrastructure_resilience_value,fragility_risk\n";
    for (const auto& s : strategies) {
        std::cout << s.name << "," << infrastructure_value(s) << "," << s.fragility << "\n";
    }

    return 0;
}
