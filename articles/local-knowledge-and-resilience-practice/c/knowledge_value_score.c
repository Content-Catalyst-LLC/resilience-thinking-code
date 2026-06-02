#include <stdio.h>

double knowledge_value(
    double participation,
    double diversity,
    double influence,
    double trust,
    double protection,
    double reciprocity,
    double accountability,
    double burden
) {
    return 0.14 * participation
        + 0.14 * diversity
        + 0.15 * influence
        + 0.14 * trust
        + 0.14 * protection
        + 0.14 * reciprocity
        + 0.15 * accountability
        - 0.02 * burden;
}

int main(void) {
    double score = knowledge_value(9.0, 8.7, 9.1, 8.8, 8.5, 8.9, 9.0, 3.3);

    printf("participation,diversity,influence,trust,protection,reciprocity,accountability,burden,knowledge_value\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           9.0, 8.7, 9.1, 8.8, 8.5, 8.9, 9.0, 3.3, score);
    return 0;
}
