#include <stdio.h>

double hidden_risk_score(
    double maintenance_backlog,
    double climate_pressure,
    double exposure,
    double public_trust,
    double ecological_memory,
    double adaptive_capacity,
    double monitoring_quality,
    double justice_visibility
) {
    return 0.20 * maintenance_backlog
        + 0.18 * climate_pressure
        + 0.16 * exposure
        + 0.12 * (1.0 - public_trust)
        + 0.12 * (1.0 - ecological_memory)
        + 0.10 * (1.0 - adaptive_capacity)
        + 0.07 * (1.0 - monitoring_quality)
        + 0.05 * (1.0 - justice_visibility);
}

int main(void) {
    double score = hidden_risk_score(0.58, 0.62, 0.74, 0.52, 0.40, 0.48, 0.54, 0.48);

    printf("maintenance_backlog,climate_pressure,exposure,public_trust,ecological_memory,adaptive_capacity,monitoring_quality,justice_visibility,hidden_risk_score\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           0.58, 0.62, 0.74, 0.52, 0.40, 0.48, 0.54, 0.48, score);
    return 0;
}
