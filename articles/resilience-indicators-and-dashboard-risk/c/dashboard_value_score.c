#include <stdio.h>

double dashboard_value(
    double indicator_coverage,
    double threshold_sensitivity,
    double justice_visibility,
    double uncertainty_transparency,
    double decision_trigger_clarity,
    double learning_integration,
    double dashboard_risk
) {
    return 0.15 * indicator_coverage
        + 0.17 * threshold_sensitivity
        + 0.16 * justice_visibility
        + 0.14 * uncertainty_transparency
        + 0.16 * decision_trigger_clarity
        + 0.14 * learning_integration
        - 0.08 * dashboard_risk;
}

int main(void) {
    double score = dashboard_value(8.4, 8.5, 8.1, 8.5, 9.0, 8.9, 3.6);

    printf("indicator_coverage,threshold_sensitivity,justice_visibility,uncertainty_transparency,decision_trigger_clarity,learning_integration,dashboard_risk,dashboard_value\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           8.4, 8.5, 8.1, 8.5, 9.0, 8.9, 3.6, score);
    return 0;
}
