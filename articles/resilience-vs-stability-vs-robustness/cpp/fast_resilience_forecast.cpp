#include <cmath>
#include <iostream>
#include <string>
#include <vector>

double sigmoid(double z) {
    return 1.0 / (1.0 + std::exp(-z));
}

double predict_failure(double adaptive, double threshold, double learning, double redundancy,
                       double modularity, double exposure, double sensitivity, double shock) {
    double protective = 0.24*adaptive + 0.22*threshold + 0.18*learning + 0.18*redundancy + 0.18*modularity;
    double pressure = 0.32*exposure + 0.28*sensitivity + 0.40*shock;
    return sigmoid(-2.0 + 4.2*pressure - 3.8*protective);
}

int main() {
    struct Scenario {
        std::string name;
        double adaptive, threshold, learning, redundancy, modularity, exposure, sensitivity, shock;
    };

    std::vector<Scenario> scenarios = {
        {"stable_but_brittle", 0.28, 0.32, 0.24, 0.35, 0.34, 0.64, 0.62, 0.45},
        {"robust_but_inflexible", 0.38, 0.46, 0.33, 0.60, 0.43, 0.70, 0.58, 0.52},
        {"adaptive_resilient", 0.88, 0.80, 0.86, 0.73, 0.70, 0.52, 0.46, 0.50}
    };

    std::cout << "scenario,predicted_failure_probability\n";
    for (const auto& s : scenarios) {
        double p = predict_failure(s.adaptive, s.threshold, s.learning, s.redundancy, s.modularity,
                                   s.exposure, s.sensitivity, s.shock);
        std::cout << s.name << "," << p << "\n";
    }

    return 0;
}
