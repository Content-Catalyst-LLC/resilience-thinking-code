#include <stdio.h>

double feedback_risk_score(
    double reinforcing_gain,
    double disturbance_load,
    double delay_steps_scaled,
    double balancing_strength,
    double adaptive_capacity,
    double signal_quality,
    double system_memory,
    double justice_visibility
) {
    return 0.24 * reinforcing_gain
        + 0.20 * disturbance_load
        + 0.18 * delay_steps_scaled
        - 0.16 * balancing_strength
        - 0.10 * adaptive_capacity
        - 0.07 * signal_quality
        - 0.03 * system_memory
        - 0.02 * justice_visibility;
}

int main(void) {
    double score = feedback_risk_score(0.090, 0.72, 0.90, 0.090, 0.44, 0.46, 0.50, 0.44);

    printf("reinforcing_gain,disturbance_load,delay_steps_scaled,balancing_strength,adaptive_capacity,signal_quality,system_memory,justice_visibility,feedback_risk_score\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           0.090, 0.72, 0.90, 0.090, 0.44, 0.46, 0.50, 0.44, score);
    return 0;
}
