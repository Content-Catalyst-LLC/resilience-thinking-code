#include <stdio.h>

int main(void) {
    const int steps = 80;
    const double target = 0.30;
    const double correction_rate = 0.16;
    double vulnerability = 0.85;

    printf("time,vulnerability_stock\n");

    for (int t = 1; t <= steps; t++) {
        if (t > 1) {
            vulnerability = vulnerability - correction_rate * (vulnerability - target);
        }
        printf("%d,%.6f\n", t, vulnerability);
    }

    return 0;
}
