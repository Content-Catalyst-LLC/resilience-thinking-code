#include <stdio.h>

double slack_value(
    double financial,
    double workforce,
    double operational,
    double knowledge,
    double network,
    double governance,
    double ethics,
    double burden,
    double implementation
) {
    return 0.13 * financial
        + 0.14 * workforce
        + 0.13 * operational
        + 0.13 * knowledge
        + 0.13 * network
        + 0.14 * governance
        + 0.13 * ethics
        - 0.04 * burden
        - 0.03 * implementation;
}

int main(void) {
    double score = slack_value(7.8, 8.1, 8.0, 8.4, 8.1, 9.1, 8.4, 2.8, 3.2);

    printf("financial,workforce,operational,knowledge,network,governance,ethics,burden,implementation,slack_resilience_value\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           7.8, 8.1, 8.0, 8.4, 8.1, 9.1, 8.4, 2.8, 3.2, score);
    return 0;
}
