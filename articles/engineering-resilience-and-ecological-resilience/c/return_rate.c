#include <stdio.h>

int main(void) {
    const int steps = 120;
    const double x_star = 0.0;
    const double return_rate = 0.18;
    double x = 1.0;

    printf("time,engineering_state\n");

    for (int t = 1; t <= steps; t++) {
        if (t > 1) {
            x = x - return_rate * (x - x_star);
        }
        printf("%d,%.6f\n", t, x);
    }

    return 0;
}
