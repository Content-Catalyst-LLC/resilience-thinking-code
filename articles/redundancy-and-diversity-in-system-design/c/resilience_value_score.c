#include <stdio.h>

double resilience_value(
    double redundancy,
    double diversity,
    double response_diversity,
    double coordination_capacity,
    double justice_contribution,
    double maintenance_reliability,
    double common_mode_risk
) {
    return 0.22 * redundancy
        + 0.18 * diversity
        + 0.22 * response_diversity
        + 0.13 * coordination_capacity
        + 0.10 * justice_contribution
        + 0.07 * maintenance_reliability
        - 0.08 * common_mode_risk;
}

int main(void) {
    double score = resilience_value(8.8, 7.4, 7.8, 7.6, 7.2, 7.5, 3.8);

    printf("redundancy,diversity,response_diversity,coordination_capacity,justice_contribution,maintenance_reliability,common_mode_risk,resilience_value\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           8.8, 7.4, 7.8, 7.6, 7.2, 7.5, 3.8, score);
    return 0;
}
