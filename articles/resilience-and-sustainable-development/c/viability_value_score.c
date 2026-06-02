#include <stdio.h>

double viability_value(
    double resilience,
    double ecology,
    double inclusion,
    double economy,
    double governance,
    double adaptive,
    double pressure,
    double burden
) {
    return 0.18 * resilience
        + 0.17 * ecology
        + 0.16 * inclusion
        + 0.14 * economy
        + 0.14 * governance
        + 0.15 * adaptive
        - 0.04 * pressure
        - 0.02 * burden;
}

int main(void) {
    double score = viability_value(8.4, 9.0, 8.2, 7.9, 8.0, 8.7, 3.5, 3.2);

    printf("resilience,ecology,inclusion,economy,governance,adaptive,pressure,burden,viability_value\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           8.4, 9.0, 8.2, 7.9, 8.0, 8.7, 3.5, 3.2, score);
    return 0;
}
