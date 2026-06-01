#include <stdio.h>

int main(void) {
    const int steps = 160;
    const double x_star = 0.0;
    const double a = 0.10;
    double x = 1.0;

    printf("time,equilibrium_state\n");

    for (int t = 1; t <= steps; t++) {
        if (t > 1) {
            x = x - a * (x - x_star);
        }
        printf("%d,%.6f\n", t, x);
    }

    return 0;
}
