#include <stdio.h>

double extraction_pressure(double q, double social_pressure, double ecology) {
    return q * social_pressure * ecology;
}

int main(void) {
    double q = 0.10;
    double social_pressure = 0.55;
    double ecology = 0.75;
    double extraction = extraction_pressure(q, social_pressure, ecology);

    printf("q,social_pressure,ecology,extraction_pressure\n");
    printf("%.4f,%.4f,%.4f,%.6f\n", q, social_pressure, ecology, extraction);
    return 0;
}
