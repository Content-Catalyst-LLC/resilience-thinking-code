#include <iostream>
#include <string>
#include <vector>

struct Framework {
    std::string name;
    double resistance;
    double recovery;
    double adaptive;
    double buffer;
    double justice;
    double data_quality;
    double threshold_blindness;
};

double metric_value(const Framework& f) {
    return 0.16 * f.resistance
        + 0.16 * f.recovery
        + 0.16 * f.adaptive
        + 0.15 * f.buffer
        + 0.13 * f.justice
        + 0.10 * f.data_quality
        - 0.14 * f.threshold_blindness;
}

int main() {
    std::vector<Framework> frameworks = {
        {"Indicator Dashboard", 7.8, 7.0, 7.4, 7.6, 6.8, 7.2, 5.2},
        {"Scenario Stress-Test Framework", 8.0, 7.6, 8.1, 7.9, 7.2, 7.4, 3.9},
        {"Hybrid Structural and Dynamic Assessment", 8.5, 8.4, 8.7, 8.2, 8.1, 8.5, 3.2}
    };

    std::cout << "framework,metric_value,threshold_blindness\n";
    for (const auto& f : frameworks) {
        std::cout << f.name << "," << metric_value(f) << "," << f.threshold_blindness << "\n";
    }

    return 0;
}
