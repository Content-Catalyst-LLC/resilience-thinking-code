#include <stdio.h>

double drr_value(
    double hazard_reduction,
    double exposure_reduction,
    double vulnerability_reduction,
    double capacity_enhancement,
    double justice_protection,
    double maladaptation_risk
) {
    return 0.17 * hazard_reduction
        + 0.18 * exposure_reduction
        + 0.18 * vulnerability_reduction
        + 0.17 * capacity_enhancement
        + 0.18 * justice_protection
        - 0.12 * maladaptation_risk;
}

int main(void) {
    double score = drr_value(6.7, 7.4, 8.9, 8.3, 9.0, 2.4);

    printf("hazard_reduction,exposure_reduction,vulnerability_reduction,capacity_enhancement,justice_protection,maladaptation_risk,drr_value\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           6.7, 7.4, 8.9, 8.3, 9.0, 2.4, score);
    return 0;
}
