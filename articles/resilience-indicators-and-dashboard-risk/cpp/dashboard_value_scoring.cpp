#include <iostream>
#include <string>
#include <vector>

struct Dashboard {
    std::string name;
    double indicator_coverage;
    double threshold_sensitivity;
    double justice_visibility;
    double uncertainty_transparency;
    double decision_trigger_clarity;
    double learning_integration;
    double dashboard_risk;
};

double dashboard_value(const Dashboard& d) {
    return 0.15 * d.indicator_coverage
        + 0.17 * d.threshold_sensitivity
        + 0.16 * d.justice_visibility
        + 0.14 * d.uncertainty_transparency
        + 0.16 * d.decision_trigger_clarity
        + 0.14 * d.learning_integration
        - 0.08 * d.dashboard_risk;
}

int main() {
    std::vector<Dashboard> dashboards = {
        {"Simple Composite Resilience Score", 7.2, 5.4, 5.8, 5.6, 5.2, 5.5, 7.8},
        {"Threshold-Sensitive Early Warning Dashboard", 8.0, 8.9, 7.2, 8.0, 8.2, 7.8, 4.2},
        {"Adaptive Learning and Decision-Trigger Dashboard", 8.4, 8.5, 8.1, 8.5, 9.0, 8.9, 3.6}
    };

    std::cout << "dashboard,dashboard_value,dashboard_risk\n";
    for (const auto& d : dashboards) {
        std::cout << d.name << "," << dashboard_value(d) << "," << d.dashboard_risk << "\n";
    }

    return 0;
}
