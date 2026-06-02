#include <iostream>
#include <string>
#include <vector>

struct Portfolio {
    std::string name;
    double financial;
    double workforce;
    double operational;
    double knowledge;
    double network;
    double governance;
    double ethics;
    double burden;
    double implementation;
};

double slack_value(const Portfolio& p) {
    return 0.13 * p.financial
        + 0.14 * p.workforce
        + 0.13 * p.operational
        + 0.13 * p.knowledge
        + 0.13 * p.network
        + 0.14 * p.governance
        + 0.13 * p.ethics
        - 0.04 * p.burden
        - 0.03 * p.implementation;
}

int main() {
    std::vector<Portfolio> portfolios = {
        {"Workforce Depth and Recovery Time", 7.5, 9.2, 7.8, 8.0, 7.5, 8.2, 9.1, 2.6, 3.4},
        {"Knowledge Architecture and Institutional Memory", 7.4, 8.0, 7.6, 9.3, 7.8, 8.5, 8.3, 2.9, 3.3},
        {"Adaptive Governance and Emergency Decision Space", 7.8, 8.1, 8.0, 8.4, 8.1, 9.1, 8.4, 2.8, 3.2}
    };

    std::cout << "portfolio,slack_resilience_value,ethical_burden\n";
    for (const auto& p : portfolios) {
        std::cout << p.name << "," << slack_value(p) << "," << p.burden << "\n";
    }

    return 0;
}
