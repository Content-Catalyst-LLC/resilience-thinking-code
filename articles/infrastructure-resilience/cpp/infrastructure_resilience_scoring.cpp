#include <iostream>
#include <string>
#include <vector>

struct Strategy {
    std::string name;
    double service_continuity;
    double redundancy;
    double recovery_speed;
    double adaptive_capacity;
    double equity_protection;
    double cascading_exposure;
};

double resilience_value(const Strategy& s) {
    return 0.22 * s.service_continuity
        + 0.20 * s.redundancy
        + 0.18 * s.recovery_speed
        + 0.16 * s.adaptive_capacity
        + 0.16 * s.equity_protection
        - 0.08 * s.cascading_exposure;
}

int main() {
    std::vector<Strategy> strategies = {
        {"Grid Redundancy and Microgrid Expansion", 8.7, 8.9, 8.0, 8.2, 7.8, 3.9},
        {"Hybrid Wetland and Stormwater Infrastructure", 8.0, 7.8, 7.6, 8.4, 8.1, 3.6},
        {"Equitable Critical Service Restoration Program", 8.4, 8.0, 8.6, 8.1, 8.9, 3.4}
    };

    std::cout << "strategy,resilience_value,cascading_exposure\n";
    for (const auto& s : strategies) {
        std::cout << s.name << "," << resilience_value(s) << "," << s.cascading_exposure << "\n";
    }

    return 0;
}
