#include <cmath>
#include <iostream>
#include <string>

int main() {
    const int steps = 100;
    double vulnerability = 0.35;
    const double reinforcing = 0.18;
    const double repair = 0.25;
    const double adaptive = 0.70;
    const double buffer = 0.65;
    const double threshold = 0.25;

    std::cout << "time,disturbance,vulnerability_stock,resilience_margin,threshold_flag\n";

    for (int t = 1; t <= steps; ++t) {
        double disturbance = 0.06 + 0.03 * std::sin(t / 6.0);
        if (t == 20 || t == 40 || t == 65 || t == 83) {
            disturbance += 0.30;
        }

        vulnerability += reinforcing * vulnerability + 0.35 * disturbance - repair * disturbance - 0.012 * adaptive;
        if (vulnerability < 0.0) vulnerability = 0.0;
        if (vulnerability > 2.0) vulnerability = 2.0;

        double margin = buffer + adaptive - vulnerability - 0.25 * disturbance;
        std::string flag = margin < threshold ? "threshold risk" : "viable margin";

        std::cout << t << "," << disturbance << "," << vulnerability << "," << margin << "," << flag << "\n";
    }

    return 0;
}
