#include <iostream>
#include <string>
#include <vector>

struct Strategy {
    std::string name;
    double monitoring;
    double forecasting;
    double scenario;
    double decision;
    double governance;
    double equity;
    double human;
    double local;
    double security;
    double risk;
    double implementation;
};

double ai_value(const Strategy& s) {
    return 0.11 * s.monitoring
        + 0.10 * s.forecasting
        + 0.11 * s.scenario
        + 0.11 * s.decision
        + 0.12 * s.governance
        + 0.12 * s.equity
        + 0.12 * s.human
        + 0.10 * s.local
        + 0.10 * s.security
        - 0.05 * s.risk
        - 0.04 * s.implementation;
}

int main() {
    std::vector<Strategy> strategies = {
        {"AI Decision Support with Human Oversight", 8.1, 8.0, 8.4, 9.1, 8.7, 8.4, 9.2, 8.2, 8.4, 2.7, 3.4},
        {"Participatory AI and Local Knowledge Integration", 7.6, 7.4, 8.2, 8.0, 8.6, 9.2, 9.1, 9.4, 8.0, 2.6, 3.7},
        {"AI Governance Audit and Drift Monitoring", 8.4, 8.2, 8.5, 8.4, 9.3, 8.8, 8.8, 8.4, 9.0, 2.5, 3.8}
    };

    std::cout << "strategy,ai_resilience_value,ai_risk\n";
    for (const auto& s : strategies) {
        std::cout << s.name << "," << ai_value(s) << "," << s.risk << "\n";
    }

    return 0;
}
