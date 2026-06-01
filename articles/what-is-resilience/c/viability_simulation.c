#include <stdio.h>

double clamp(double value, double low, double high) {
    if (value < low) return low;
    if (value > high) return high;
    return value;
}

int main(void) {
    double viability = 1.0;
    double adaptive_capacity = 0.72;
    double threshold_distance = 0.63;
    double exposure = 0.58;
    double sensitivity = 0.54;
    double redundancy = 0.61;
    double modularity = 0.56;
    double risk_pressure = 0.55 * exposure + 0.45 * sensitivity;

    printf("time_step,viability,margin\n");

    for (int t = 1; t <= 60; t++) {
        double disturbance = 0.055;

        if (t == 12) disturbance += 0.20;
        if (t == 24) disturbance += 0.28;
        if (t == 37) disturbance += 0.23;
        if (t == 48) disturbance += 0.31;

        double load = disturbance * (0.65 + exposure) * (0.55 + sensitivity);
        double protection = 0.35 * redundancy + 0.25 * modularity;
        double adaptive_response = 0.03 * adaptive_capacity;

        viability = clamp(viability - load * (1.0 - 0.45 * protection) + adaptive_response, 0.0, 1.25);
        double margin = viability + threshold_distance - risk_pressure;

        printf("%d,%.4f,%.4f\n", t, viability, margin);
    }

    return 0;
}
