#include <stdio.h>

double release_risk_index(
    double rigidity,
    double connectedness,
    double disturbance_exposure,
    double resilience,
    double novelty
) {
    return 0.30 * rigidity
        + 0.24 * connectedness
        + 0.20 * disturbance_exposure
        + 0.16 * (1.0 - resilience)
        + 0.10 * (1.0 - novelty);
}

int main(void) {
    double risk = release_risk_index(0.66, 0.78, 0.78, 0.38, 0.12);
    printf("rigidity,connectedness,disturbance_exposure,resilience,novelty,release_risk_index\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n", 0.66, 0.78, 0.78, 0.38, 0.12, risk);
    return 0;
}
