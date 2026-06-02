#include <stdio.h>

double resilience_value(
    double prevention,
    double detection,
    double continuity,
    double workforce,
    double governance,
    double trust,
    double equity,
    double burden
) {
    return 0.14 * prevention
        + 0.15 * detection
        + 0.15 * continuity
        + 0.14 * workforce
        + 0.14 * governance
        + 0.13 * trust
        + 0.13 * equity
        - 0.02 * burden;
}

int main(void) {
    double score = resilience_value(8.1, 8.0, 8.2, 8.3, 8.8, 8.7, 9.1, 3.0);

    printf("prevention,detection,continuity,workforce,governance,trust,equity,burden,resilience_value\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           8.1, 8.0, 8.2, 8.3, 8.8, 8.7, 9.1, 3.0, score);
    return 0;
}
