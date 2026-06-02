#include <algorithm>
#include <cmath>
#include <iostream>
#include <string>

int main() {
    const int steps = 80;
    double condition = 0.78;
    double exposure = 0.66;
    double buffer_capacity = 0.70;
    double memory = 0.72;
    double recovery = 0.64;
    double refugia = 1.0;
    double social_exposure = 0.54;
    double disturbance = 0.08 + 0.10 * exposure;

    std::cout << "time,condition,disturbance,resilience_margin,threshold_flag\n";

    for (int t = 1; t <= steps; ++t) {
        double seasonal = 0.04 + 0.025 * std::sin(t / 7.0);
        double shock = (t == 18 || t == 36 || t == 55 || t == 70) ? 0.24 : 0.0;

        disturbance = disturbance + 0.32 + seasonal + shock + 0.18 * 0.58 + 0.22 * exposure - 0.26 * buffer_capacity - 0.12 * refugia - 0.06 * 0.48;
        disturbance = std::max(0.0, std::min(1.4, disturbance));

        condition = condition - 0.055 * disturbance + 0.018 * memory + 0.015 * recovery + 0.008 * refugia + 0.006 * 0.48;
        condition = std::max(0.0, std::min(1.0, condition));

        double margin = condition + buffer_capacity + memory + recovery + 0.25 * refugia + 0.20 * 0.48 - disturbance - exposure - 0.30 * social_exposure;
        std::string flag = margin < 0.75 ? "threshold risk" : "viable margin";

        std::cout << t << "," << condition << "," << disturbance << "," << margin << "," << flag << "\n";
    }

    return 0;
}
