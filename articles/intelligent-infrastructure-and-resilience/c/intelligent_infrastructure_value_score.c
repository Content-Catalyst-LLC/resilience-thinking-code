#include <stdio.h>

double infrastructure_value(
    double monitoring,
    double maintenance,
    double cyber,
    double twin,
    double redundancy,
    double climate,
    double governance,
    double equity,
    double ecology,
    double fragility,
    double implementation
) {
    return 0.10 * monitoring
        + 0.11 * maintenance
        + 0.11 * cyber
        + 0.10 * twin
        + 0.11 * redundancy
        + 0.11 * climate
        + 0.12 * governance
        + 0.12 * equity
        + 0.10 * ecology
        - 0.04 * fragility
        - 0.04 * implementation;
}

int main(void) {
    double score = infrastructure_value(8.5, 9.3, 8.2, 8.6, 8.4, 8.4, 8.4, 8.2, 8.0, 2.8, 3.8);

    printf("monitoring,maintenance,cyber,twin,redundancy,climate,governance,equity,ecology,fragility,implementation,infrastructure_resilience_value\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           8.5, 9.3, 8.2, 8.6, 8.4, 8.4, 8.4, 8.2, 8.0, 2.8, 3.8, score);
    return 0;
}
