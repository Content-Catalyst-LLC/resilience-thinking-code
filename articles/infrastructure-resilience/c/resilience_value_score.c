#include <stdio.h>

double resilience_value(
    double service_continuity,
    double redundancy,
    double recovery_speed,
    double adaptive_capacity,
    double equity_protection,
    double cascading_exposure
) {
    return 0.22 * service_continuity
        + 0.20 * redundancy
        + 0.18 * recovery_speed
        + 0.16 * adaptive_capacity
        + 0.16 * equity_protection
        - 0.08 * cascading_exposure;
}

int main(void) {
    double score = resilience_value(8.4, 8.0, 8.6, 8.1, 8.9, 3.4);

    printf("service_continuity,redundancy,recovery_speed,adaptive_capacity,equity_protection,cascading_exposure,resilience_value\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           8.4, 8.0, 8.6, 8.1, 8.9, 3.4, score);
    return 0;
}
