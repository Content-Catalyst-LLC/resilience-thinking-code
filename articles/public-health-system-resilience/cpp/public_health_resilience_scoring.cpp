#include <iostream>
#include <string>
#include <vector>

struct Strategy {
    std::string name;
    double prevention;
    double detection;
    double continuity;
    double workforce;
    double governance;
    double trust;
    double equity;
    double burden;
};

double resilience_value(const Strategy& s) {
    return 0.14 * s.prevention
        + 0.15 * s.detection
        + 0.15 * s.continuity
        + 0.14 * s.workforce
        + 0.14 * s.governance
        + 0.13 * s.trust
        + 0.13 * s.equity
        - 0.02 * s.burden;
}

int main() {
    std::vector<Strategy> strategies = {
        {"Essential Health Service Continuity Program", 7.6, 7.4, 9.0, 8.1, 8.2, 7.9, 8.2, 3.2},
        {"Community Health Trust and Outreach Network", 8.2, 7.9, 8.1, 8.2, 8.5, 9.0, 8.9, 2.8},
        {"Equity-Centered Emergency Preparedness Framework", 8.1, 8.0, 8.2, 8.3, 8.8, 8.7, 9.1, 3.0}
    };

    std::cout << "strategy,resilience_value,implementation_burden\n";
    for (const auto& s : strategies) {
        std::cout << s.name << "," << resilience_value(s) << "," << s.burden << "\n";
    }

    return 0;
}
