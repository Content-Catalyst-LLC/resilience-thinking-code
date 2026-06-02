#include <stdio.h>

double adaptive_capacity_score(
    double learning,
    double flexibility,
    double diversity,
    double governance,
    double slack,
    double trust,
    double rigidity
) {
    return 0.18 * learning
        + 0.18 * flexibility
        + 0.17 * diversity
        + 0.17 * governance
        + 0.14 * slack
        + 0.16 * trust
        - 0.12 * rigidity;
}

int main(void) {
    double score = adaptive_capacity_score(0.60, 0.57, 0.64, 0.58, 0.50, 0.57, 0.55);

    printf("learning,flexibility,diversity,governance,slack,trust,rigidity,adaptive_capacity\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           0.60, 0.57, 0.64, 0.58, 0.50, 0.57, 0.55, score);
    return 0;
}
