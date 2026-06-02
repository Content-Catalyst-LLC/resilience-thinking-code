#include <stdio.h>

double patch_resilience_margin(
    double condition,
    double buffer_capacity,
    double ecological_memory,
    double recovery_capacity,
    double refugia,
    double disturbance,
    double exposure,
    double social_exposure
) {
    return condition + buffer_capacity + ecological_memory + recovery_capacity
        + 0.25 * refugia - disturbance - exposure - 0.30 * social_exposure;
}

int main(void) {
    double margin = patch_resilience_margin(0.78, 0.70, 0.72, 0.64, 1.0, 0.30, 0.66, 0.54);

    printf("condition,buffer_capacity,ecological_memory,recovery_capacity,refugia,disturbance,exposure,social_exposure,resilience_margin\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           0.78, 0.70, 0.72, 0.64, 1.0, 0.30, 0.66, 0.54, margin);
    return 0;
}
