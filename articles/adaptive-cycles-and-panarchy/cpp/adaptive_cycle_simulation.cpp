#include <algorithm>
#include <cmath>
#include <iostream>
#include <string>

int main() {
    const int steps = 120;
    double potential = 0.20;
    double connectedness = 0.15;
    double resilience = 0.82;
    double rigidity = 0.10;
    double memory = 0.55;
    double novelty = 0.15;
    std::string phase = "r";

    std::cout << "time,phase,potential,connectedness,resilience,rigidity,memory,novelty,release_flag\n";

    for (int t = 1; t <= steps; ++t) {
        if (phase == "r" || phase == "K") {
            potential = std::min(1.0, potential + 0.11 * potential * (1.0 - potential));
            connectedness = std::min(1.0, connectedness + 0.08 * (1.0 - connectedness));
            rigidity = std::min(1.0, rigidity + 0.055 * connectedness);
            resilience = std::max(0.0, 1.0 - 0.62 * connectedness - 0.35 * rigidity);
            memory = std::min(1.0, memory + 0.015 * potential);
            novelty = std::max(0.02, 0.25 * (1.0 - connectedness));
            phase = connectedness > 0.55 ? "K" : "r";

            if (rigidity > 0.72 && resilience < 0.34) {
                phase = "Omega";
            }
        } else if (phase == "Omega") {
            potential = std::max(0.05, potential * 0.42);
            connectedness = std::max(0.08, connectedness * 0.32);
            rigidity = std::max(0.05, rigidity * 0.38);
            resilience = std::min(1.0, resilience + 0.30);
            memory = std::max(0.25, memory * 0.86);
            novelty = 0.32;
            phase = "alpha";
        } else if (phase == "alpha") {
            novelty = 0.24;
            potential = std::min(1.0, 0.48 * memory + 0.12);
            connectedness = std::min(1.0, connectedness + 0.03);
            rigidity = std::max(0.03, rigidity - 0.004);
            resilience = std::min(1.0, resilience + 0.05);
            memory = std::min(1.0, memory + 0.005);
            phase = (potential > 0.32 && connectedness < 0.50) ? "r" : "alpha";
        }

        int release_flag = phase == "Omega" ? 1 : 0;
        std::cout << t << "," << phase << "," << potential << "," << connectedness << ","
                  << resilience << "," << rigidity << "," << memory << "," << novelty << ","
                  << release_flag << "\n";
    }

    return 0;
}
