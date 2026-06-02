#include <stdio.h>

double transformation_readiness(
    double adaptive_support,
    double transformability,
    double governance_readiness,
    double justice_contribution,
    double ecological_viability,
    double legitimacy,
    double resource_feasibility,
    double structural_risk
) {
    return 0.18 * adaptive_support
        + 0.20 * transformability
        + 0.18 * governance_readiness
        + 0.16 * justice_contribution
        + 0.14 * ecological_viability
        + 0.08 * legitimacy
        + 0.06 * resource_feasibility
        - 0.10 * structural_risk;
}

int main(void) {
    double score = transformation_readiness(8.3, 8.5, 7.8, 8.4, 8.1, 7.8, 7.0, 4.0);

    printf("adaptive_support,transformability,governance_readiness,justice_contribution,ecological_viability,legitimacy,resource_feasibility,structural_risk,transformation_readiness\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           8.3, 8.5, 7.8, 8.4, 8.1, 7.8, 7.0, 4.0, score);
    return 0;
}
