#include <iostream>
#include <string>
#include <vector>

struct Strategy {
    std::string name;
    double resistance;
    double recovery;
    double adaptation;
    double transformation;
    double equity;
    double institutions;
    double burden;
};

double resilience_value(const Strategy& s) {
    return 0.16 * s.resistance
        + 0.16 * s.recovery
        + 0.17 * s.adaptation
        + 0.17 * s.transformation
        + 0.17 * s.equity
        + 0.17 * s.institutions
        - 0.02 * s.burden;
}

int main() {
    std::vector<Strategy> strategies = {
        {"Industrial Diversification and Local Production Program", 8.0, 8.0, 8.5, 8.4, 8.1, 8.2, 3.5},
        {"Countercyclical Stabilization and Public Investment Framework", 8.5, 8.8, 8.0, 8.0, 8.3, 8.8, 3.4},
        {"Community Finance and Small Business Continuity Fund", 8.1, 8.5, 8.1, 7.9, 8.7, 8.2, 2.9}
    };

    std::cout << "strategy,economic_resilience_value,implementation_burden\n";
    for (const auto& s : strategies) {
        std::cout << s.name << "," << resilience_value(s) << "," << s.burden << "\n";
    }

    return 0;
}
