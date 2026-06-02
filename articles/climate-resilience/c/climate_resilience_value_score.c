#include <stdio.h>

double climate_resilience_value(
    double exposure_reduction,
    double vulnerability_reduction,
    double adaptive_capacity,
    double recovery_capacity,
    double transformative_capacity,
    double justice_protection,
    double maladaptation_risk
) {
    return 0.16 * exposure_reduction
        + 0.16 * vulnerability_reduction
        + 0.16 * adaptive_capacity
        + 0.15 * recovery_capacity
        + 0.15 * transformative_capacity
        + 0.14 * justice_protection
        - 0.08 * maladaptation_risk;
}

int main(void) {
    double score = climate_resilience_value(8.3, 8.5, 8.2, 7.9, 8.4, 8.8, 2.8);

    printf("exposure_reduction,vulnerability_reduction,adaptive_capacity,recovery_capacity,transformative_capacity,justice_protection,maladaptation_risk,climate_resilience_value\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           8.3, 8.5, 8.2, 7.9, 8.4, 8.8, 2.8, score);
    return 0;
}
