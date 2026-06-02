#include <stdio.h>

double technology_value(
    double architecture,
    double redundancy,
    double observability,
    double cybersecurity,
    double data_integrity,
    double maintainability,
    double governance,
    double human,
    double vendor,
    double debt,
    double implementation
) {
    return 0.10 * architecture
        + 0.10 * redundancy
        + 0.10 * observability
        + 0.11 * cybersecurity
        + 0.11 * data_integrity
        + 0.11 * maintainability
        + 0.11 * governance
        + 0.11 * human
        + 0.10 * vendor
        - 0.03 * debt
        - 0.02 * implementation;
}

int main(void) {
    double score = technology_value(8.0, 8.9, 8.5, 9.2, 8.4, 8.1, 8.6, 8.0, 7.9, 3.2, 3.5);

    printf("architecture,redundancy,observability,cybersecurity,data_integrity,maintainability,governance,human,vendor,debt,implementation,technology_resilience_value\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           8.0, 8.9, 8.5, 9.2, 8.4, 8.1, 8.6, 8.0, 7.9, 3.2, 3.5, score);
    return 0;
}
