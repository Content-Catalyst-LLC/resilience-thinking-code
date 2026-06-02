#include <stdio.h>

int main(void) {
    const int steps = 100;
    const double x_star = 0.0;
    const double return_rate = 0.12;
    double ecosystem_state = 1.0;

    printf("time,ecosystem_state\n");
    for (int t = 1; t <= steps; t++) {
        if (t > 1) ecosystem_state = ecosystem_state - return_rate * (ecosystem_state - x_star);
        printf("%d,%.6f\n", t, ecosystem_state);
    }
    return 0;
}
