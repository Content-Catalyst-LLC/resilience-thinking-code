#include <stdio.h>

double resilience_value(
    double resistance,
    double recovery,
    double adaptation,
    double transformation,
    double equity,
    double institutions,
    double burden
) {
    return 0.16 * resistance
        + 0.16 * recovery
        + 0.17 * adaptation
        + 0.17 * transformation
        + 0.17 * equity
        + 0.17 * institutions
        - 0.02 * burden;
}

int main(void) {
    double score = resilience_value(8.1, 8.5, 8.1, 7.9, 8.7, 8.2, 2.9);

    printf("resistance,recovery,adaptation,transformation,equity,institutions,burden,resilience_value\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           8.1, 8.5, 8.1, 7.9, 8.7, 8.2, 2.9, score);
    return 0;
}
