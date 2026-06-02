#include <stdio.h>

double threshold_risk_score(
    double pressure,
    double feedback_strength,
    double disturbance_load,
    double exposure,
    double adaptive_capacity,
    double system_memory,
    double recovery_speed
) {
    return 0.24 * pressure
        + 0.22 * feedback_strength
        + 0.18 * disturbance_load
        + 0.14 * exposure
        - 0.10 * adaptive_capacity
        - 0.07 * system_memory
        - 0.05 * recovery_speed;
}

int main(void) {
    double risk = threshold_risk_score(0.74, 0.66, 0.62, 0.78, 0.44, 0.46, 0.36);

    printf("pressure,feedback_strength,disturbance_load,exposure,adaptive_capacity,system_memory,recovery_speed,threshold_risk_score\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           0.74, 0.66, 0.62, 0.78, 0.44, 0.46, 0.36, risk);
    return 0;
}
