#include <stdio.h>

double supply_chain_value(
    double redundancy,
    double flexibility,
    double visibility,
    double coordination,
    double adaptation,
    double equity,
    double infrastructure,
    double exposure,
    double burden
) {
    return 0.13 * redundancy
        + 0.13 * flexibility
        + 0.13 * visibility
        + 0.13 * coordination
        + 0.13 * adaptation
        + 0.13 * equity
        + 0.13 * infrastructure
        - 0.06 * exposure
        - 0.03 * burden;
}

int main(void) {
    double score = supply_chain_value(8.1, 8.8, 8.0, 8.2, 8.5, 7.8, 8.5, 4.0, 3.4);

    printf("redundancy,flexibility,visibility,coordination,adaptation,equity,infrastructure,exposure,burden,supply_chain_value\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           8.1, 8.8, 8.0, 8.2, 8.5, 7.8, 8.5, 4.0, 3.4, score);
    return 0;
}
