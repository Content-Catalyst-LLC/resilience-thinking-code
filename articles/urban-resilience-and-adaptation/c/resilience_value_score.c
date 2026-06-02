#include <stdio.h>

double resilience_value(
    double exposure,
    double vulnerability,
    double service,
    double adaptive,
    double ecology,
    double equity,
    double maladaptation
) {
    return 0.16 * exposure
        + 0.17 * vulnerability
        + 0.17 * service
        + 0.15 * adaptive
        + 0.14 * ecology
        + 0.15 * equity
        - 0.06 * maladaptation;
}

int main(void) {
    double score = resilience_value(7.5, 8.9, 7.7, 8.4, 7.5, 9.1, 2.5);

    printf("exposure,vulnerability,service,adaptive,ecology,equity,maladaptation,resilience_value\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           7.5, 8.9, 7.7, 8.4, 7.5, 9.1, 2.5, score);
    return 0;
}
