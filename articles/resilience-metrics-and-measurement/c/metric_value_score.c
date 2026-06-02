#include <stdio.h>

double metric_value(
    double resistance,
    double recovery,
    double adaptive,
    double buffer,
    double justice,
    double data_quality,
    double threshold_blindness
) {
    return 0.16 * resistance
        + 0.16 * recovery
        + 0.16 * adaptive
        + 0.15 * buffer
        + 0.13 * justice
        + 0.10 * data_quality
        - 0.14 * threshold_blindness;
}

int main(void) {
    double score = metric_value(8.5, 8.4, 8.7, 8.2, 8.1, 8.5, 3.2);

    printf("resistance,recovery,adaptive,buffer,justice,data_quality,threshold_blindness,metric_value\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           8.5, 8.4, 8.7, 8.2, 8.1, 8.5, 3.2, score);
    return 0;
}
