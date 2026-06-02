#include <stdio.h>

double financial_value(
    double capital,
    double liquidity,
    double infrastructure,
    double governance,
    double inclusion,
    double exposure,
    double burden
) {
    return 0.16 * capital
        + 0.16 * liquidity
        + 0.16 * infrastructure
        + 0.16 * governance
        + 0.16 * inclusion
        - 0.12 * exposure
        - 0.08 * burden;
}

int main(void) {
    double score = financial_value(8.9, 8.8, 7.6, 8.3, 7.4, 3.9, 3.2);

    printf("capital,liquidity,infrastructure,governance,inclusion,exposure,burden,financial_resilience_value\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           8.9, 8.8, 7.6, 8.3, 7.4, 3.9, 3.2, score);
    return 0;
}
