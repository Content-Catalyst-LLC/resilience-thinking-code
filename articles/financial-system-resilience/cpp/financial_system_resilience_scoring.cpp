#include <iostream>
#include <string>
#include <vector>

struct Strategy {
    std::string name;
    double capital;
    double liquidity;
    double infrastructure;
    double governance;
    double inclusion;
    double exposure;
    double burden;
};

double financial_value(const Strategy& s) {
    return 0.16 * s.capital
        + 0.16 * s.liquidity
        + 0.16 * s.infrastructure
        + 0.16 * s.governance
        + 0.16 * s.inclusion
        - 0.12 * s.exposure
        - 0.08 * s.burden;
}

int main() {
    std::vector<Strategy> strategies = {
        {"Higher Capital and Liquidity Buffers", 8.9, 8.8, 7.6, 8.3, 7.4, 3.9, 3.2},
        {"Payment and Clearing Infrastructure Hardening", 7.4, 7.8, 9.2, 8.5, 7.8, 3.8, 3.5},
        {"Inclusive Finance and Household Balance Sheet Resilience", 7.2, 7.4, 7.4, 8.1, 9.2, 4.0, 3.0}
    };

    std::cout << "strategy,financial_resilience_value,implementation_burden\n";
    for (const auto& s : strategies) {
        std::cout << s.name << "," << financial_value(s) << "," << s.burden << "\n";
    }

    return 0;
}
