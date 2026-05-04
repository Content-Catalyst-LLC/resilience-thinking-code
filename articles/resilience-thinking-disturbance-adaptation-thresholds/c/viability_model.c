#include <stdio.h>

int main(void) {
    const int steps = 30;
    double viability[steps];
    double disturbance = 0.08;
    double adaptive_response = 0.09;

    viability[0] = 1.0;

    for (int t = 1; t < steps; t++) {
        viability[t] = viability[t - 1] - disturbance + adaptive_response;

        if (viability[t] < 0.0) {
            viability[t] = 0.0;
        }

        if (viability[t] > 1.5) {
            viability[t] = 1.5;
        }
    }

    printf("Viability simulation\n");

    for (int t = 0; t < steps; t++) {
        printf("time=%d, viability=%.3f\n", t, viability[t]);
    }

    return 0;
}
