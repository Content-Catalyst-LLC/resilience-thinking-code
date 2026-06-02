#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    const int steps = 80;
    const double gain = 0.03;
    const double balancing = 0.14;
    const double target = 75.0;
    const int delay = 5;

    std::vector<double> x(steps + delay + 2, 20.0);

    std::cout << "time,value,target,gain,balancing,delay,overshoot\n";

    for (int t = 1; t < steps; ++t) {
        int delayed_index = std::max(0, t - delay);
        x[t] = x[t - 1] + gain * x[t - 1] - balancing * (x[delayed_index] - target);
        double overshoot = std::max(0.0, x[t] - target);
        std::cout << t << "," << x[t] << "," << target << "," << gain << ","
                  << balancing << "," << delay << "," << overshoot << "\n";
    }

    return 0;
}
