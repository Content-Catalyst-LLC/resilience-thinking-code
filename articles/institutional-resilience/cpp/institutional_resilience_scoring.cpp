#include <iostream>
#include <string>
#include <vector>

struct Strategy {
    std::string name;
    double legitimacy;
    double capacity;
    double flexibility;
    double coordination;
    double learning;
    double accountability;
    double equity;
    double burden;
};

double resilience_value(const Strategy& s) {
    return 0.14 * s.legitimacy
        + 0.14 * s.capacity
        + 0.13 * s.flexibility
        + 0.14 * s.coordination
        + 0.14 * s.learning
        + 0.14 * s.accountability
        + 0.15 * s.equity
        - 0.02 * s.burden;
}

int main() {
    std::vector<Strategy> strategies = {
        {"Public Trust and Transparency Initiative", 8.9, 7.1, 7.0, 7.2, 7.4, 8.5, 8.2, 2.8},
        {"Equity and Access Accountability Review", 8.3, 7.5, 7.8, 7.6, 7.9, 8.9, 9.1, 3.0},
        {"Institutional Learning and After-Action Implementation System", 7.8, 8.0, 8.2, 8.4, 9.0, 8.4, 8.1, 3.3}
    };

    std::cout << "strategy,resilience_value,implementation_burden\n";
    for (const auto& s : strategies) {
        std::cout << s.name << "," << resilience_value(s) << "," << s.burden << "\n";
    }

    return 0;
}
