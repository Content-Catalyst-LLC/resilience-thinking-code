#include <stdio.h>

double governance_value(
    double learning,
    double flexibility,
    double coordination,
    double knowledge,
    double legitimacy,
    double accountability,
    double equity,
    double burden
) {
    return 0.15 * learning
        + 0.14 * flexibility
        + 0.14 * coordination
        + 0.14 * knowledge
        + 0.14 * legitimacy
        + 0.14 * accountability
        + 0.15 * equity
        - 0.02 * burden;
}

int main(void) {
    double score = governance_value(8.3, 7.6, 8.0, 9.1, 8.8, 8.3, 8.7, 3.1);

    printf("learning,flexibility,coordination,knowledge,legitimacy,accountability,equity,burden,governance_value\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           8.3, 7.6, 8.0, 9.1, 8.8, 8.3, 8.7, 3.1, score);
    return 0;
}
