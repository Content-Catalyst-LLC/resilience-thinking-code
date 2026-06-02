#include <stdio.h>

double resilience_value(
    double legitimacy,
    double capacity,
    double flexibility,
    double coordination,
    double learning,
    double accountability,
    double equity,
    double burden
) {
    return 0.14 * legitimacy
        + 0.14 * capacity
        + 0.13 * flexibility
        + 0.14 * coordination
        + 0.14 * learning
        + 0.14 * accountability
        + 0.15 * equity
        - 0.02 * burden;
}

int main(void) {
    double score = resilience_value(8.3, 7.5, 7.8, 7.6, 7.9, 8.9, 9.1, 3.0);

    printf("legitimacy,capacity,flexibility,coordination,learning,accountability,equity,burden,resilience_value\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           8.3, 7.5, 7.8, 7.6, 7.9, 8.9, 9.1, 3.0, score);
    return 0;
}
