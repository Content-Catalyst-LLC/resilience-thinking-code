#include <iostream>
#include <string>
#include <vector>

struct Strategy {
    std::string name;
    double liquidity;
    double workforce;
    double supply;
    double digital;
    double public_capacity;
    double community;
    double equity;
    double inequality;
    double implementation;
};

double local_value(const Strategy& s) {
    return 0.14 * s.liquidity
        + 0.14 * s.workforce
        + 0.12 * s.supply
        + 0.12 * s.digital
        + 0.14 * s.public_capacity
        + 0.15 * s.community
        + 0.16 * s.equity
        - 0.07 * s.inequality
        - 0.06 * s.implementation;
}

int main() {
    std::vector<Strategy> strategies = {
        {"Emergency Microgrant and Liquidity Fund", 9.2, 7.4, 7.2, 7.4, 8.3, 7.5, 8.6, 2.8, 3.0},
        {"Community Development Finance and Patient Capital", 8.7, 7.5, 7.6, 7.5, 8.4, 8.7, 8.9, 2.7, 3.5},
        {"Local Procurement and Anchor Institution Access", 7.6, 7.8, 8.6, 7.8, 8.8, 8.8, 8.4, 3.0, 3.6}
    };

    std::cout << "strategy,local_resilience_value,inequality_risk\n";
    for (const auto& s : strategies) {
        std::cout << s.name << "," << local_value(s) << "," << s.inequality << "\n";
    }

    return 0;
}
