#include <stdio.h>

double ai_value(
    double monitoring,
    double forecasting,
    double scenario,
    double decision,
    double governance,
    double equity,
    double human,
    double local,
    double security,
    double risk,
    double implementation
) {
    return 0.11 * monitoring
        + 0.10 * forecasting
        + 0.11 * scenario
        + 0.11 * decision
        + 0.12 * governance
        + 0.12 * equity
        + 0.12 * human
        + 0.10 * local
        + 0.10 * security
        - 0.05 * risk
        - 0.04 * implementation;
}

int main(void) {
    double score = ai_value(8.1, 8.0, 8.4, 9.1, 8.7, 8.4, 9.2, 8.2, 8.4, 2.7, 3.4);

    printf("monitoring,forecasting,scenario,decision,governance,equity,human,local,security,risk,implementation,ai_resilience_value\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           8.1, 8.0, 8.4, 9.1, 8.7, 8.4, 9.2, 8.2, 8.4, 2.7, 3.4, score);
    return 0;
}
