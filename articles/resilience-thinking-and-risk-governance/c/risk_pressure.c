#include <stdio.h>

double risk_pressure(double hazard, double exposure, double vulnerability, double adaptive) {
    return hazard * exposure * vulnerability * (1.0 - 0.55 * adaptive);
}

int main(void) {
    double rp = risk_pressure(0.74, 0.78, 0.64, 0.58);
    printf("risk_pressure\n");
    printf("%.6f\n", rp);
    return 0;
}
