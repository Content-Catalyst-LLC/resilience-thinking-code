#include <stdio.h>

double containment_value(
    double modularity,
    double redundancy,
    double dependency_mapping,
    double isolation_capacity,
    double coordination_readiness,
    double justice_protection,
    double common_mode_risk
) {
    return 0.18 * modularity
        + 0.16 * redundancy
        + 0.16 * dependency_mapping
        + 0.18 * isolation_capacity
        + 0.14 * coordination_readiness
        + 0.10 * justice_protection
        - 0.08 * common_mode_risk;
}

int main(void) {
    double score = containment_value(8.7, 8.4, 7.6, 8.8, 7.6, 7.3, 3.5);

    printf("modularity,redundancy,dependency_mapping,isolation_capacity,coordination_readiness,justice_protection,common_mode_risk,containment_value\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           8.7, 8.4, 7.6, 8.8, 7.6, 7.3, 3.5, score);
    return 0;
}
