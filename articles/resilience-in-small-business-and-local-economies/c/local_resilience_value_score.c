#include <stdio.h>

double local_value(
    double liquidity,
    double workforce,
    double supply,
    double digital,
    double public_capacity,
    double community,
    double equity,
    double inequality,
    double implementation
) {
    return 0.14 * liquidity
        + 0.14 * workforce
        + 0.12 * supply
        + 0.12 * digital
        + 0.14 * public_capacity
        + 0.15 * community
        + 0.16 * equity
        - 0.07 * inequality
        - 0.06 * implementation;
}

int main(void) {
    double score = local_value(9.2, 7.4, 7.2, 7.4, 8.3, 7.5, 8.6, 2.8, 3.0);

    printf("liquidity,workforce,supply,digital,public_capacity,community,equity,inequality,implementation,local_resilience_value\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           9.2, 7.4, 7.2, 7.4, 8.3, 7.5, 8.6, 2.8, 3.0, score);
    return 0;
}
