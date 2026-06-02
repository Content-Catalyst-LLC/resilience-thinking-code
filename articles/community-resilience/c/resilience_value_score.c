#include <stdio.h>

double resilience_value(
    double social,
    double institution,
    double access,
    double economy,
    double information,
    double adaptive,
    double equity,
    double burden
) {
    return 0.14 * social
        + 0.14 * institution
        + 0.14 * access
        + 0.13 * economy
        + 0.13 * information
        + 0.15 * adaptive
        + 0.15 * equity
        - 0.02 * burden;
}

int main(void) {
    double score = resilience_value(8.4, 8.3, 7.4, 7.8, 7.8, 8.6, 8.8, 3.1);

    printf("social,institution,access,economy,information,adaptive,equity,burden,resilience_value\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           8.4, 8.3, 7.4, 7.8, 7.8, 8.6, 8.8, 3.1, score);
    return 0;
}
