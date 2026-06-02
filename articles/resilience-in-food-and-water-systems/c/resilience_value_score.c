#include <stdio.h>

double resilience_value(
    double availability,
    double access,
    double stability,
    double quality,
    double adaptive_capacity,
    double equity_protection,
    double resource_depletion_risk
) {
    return 0.17 * availability
        + 0.17 * access
        + 0.16 * stability
        + 0.14 * quality
        + 0.16 * adaptive_capacity
        + 0.14 * equity_protection
        - 0.06 * resource_depletion_risk;
}

int main(void) {
    double score = resilience_value(7.6, 8.8, 7.7, 8.1, 8.7, 8.9, 2.8);

    printf("availability,access,stability,quality,adaptive_capacity,equity_protection,resource_depletion_risk,resilience_value\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           7.6, 8.8, 7.7, 8.1, 8.7, 8.9, 2.8, score);
    return 0;
}
