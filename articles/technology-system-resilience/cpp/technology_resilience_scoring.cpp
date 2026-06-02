#include <iostream>
#include <string>
#include <vector>

struct Strategy {
    std::string name;
    double architecture;
    double redundancy;
    double observability;
    double cybersecurity;
    double data_integrity;
    double maintainability;
    double governance;
    double human;
    double vendor;
    double debt;
    double implementation;
};

double technology_value(const Strategy& s) {
    return 0.10 * s.architecture
        + 0.10 * s.redundancy
        + 0.10 * s.observability
        + 0.11 * s.cybersecurity
        + 0.11 * s.data_integrity
        + 0.11 * s.maintainability
        + 0.11 * s.governance
        + 0.11 * s.human
        + 0.10 * s.vendor
        - 0.03 * s.debt
        - 0.02 * s.implementation;
}

int main() {
    std::vector<Strategy> strategies = {
        {"Graceful Degradation and Fallback Architecture", 9.2, 8.8, 8.4, 8.2, 7.8, 8.3, 8.4, 8.5, 8.0, 3.0, 3.4},
        {"Cyber Recovery and Tested Backup Program", 8.0, 8.9, 8.5, 9.2, 8.4, 8.1, 8.6, 8.0, 7.9, 3.2, 3.5},
        {"Data Integrity and Lineage Governance", 8.0, 7.8, 8.6, 8.1, 9.3, 8.2, 8.8, 8.2, 7.8, 3.0, 3.4}
    };

    std::cout << "strategy,technology_resilience_value,technical_debt_risk\n";
    for (const auto& s : strategies) {
        std::cout << s.name << "," << technology_value(s) << "," << s.debt << "\n";
    }

    return 0;
}
