#include <stdio.h>

double regime_risk_score(
    double pressure,
    double feedback_strength,
    double variance_signal,
    double autocorr_signal,
    double exposure,
    double recovery_speed,
    double adaptive_capacity,
    double system_memory,
    double monitoring_quality,
    double justice_visibility
) {
    return 0.18 * pressure
        + 0.17 * feedback_strength
        + 0.15 * variance_signal
        + 0.15 * autocorr_signal
        + 0.12 * exposure
        - 0.08 * recovery_speed
        - 0.06 * adaptive_capacity
        - 0.04 * system_memory
        - 0.03 * monitoring_quality
        - 0.02 * justice_visibility;
}

int main(void) {
    double score = regime_risk_score(0.74, 0.66, 0.62, 0.64, 0.78, 0.36, 0.44, 0.46, 0.52, 0.46);

    printf("pressure,feedback_strength,variance_signal,autocorr_signal,exposure,recovery_speed,adaptive_capacity,system_memory,monitoring_quality,justice_visibility,regime_risk_score\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           0.74, 0.66, 0.62, 0.64, 0.78, 0.36, 0.44, 0.46, 0.52, 0.46, score);
    return 0;
}
