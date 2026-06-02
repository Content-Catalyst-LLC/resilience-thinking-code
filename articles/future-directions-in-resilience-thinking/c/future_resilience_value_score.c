#include <stdio.h>

double resilience_value(double a,double b,double t,double g,double q,double d,double c,double e,double i) {
    return 0.16*a + 0.14*b + 0.16*t + 0.14*g + 0.14*q + 0.12*d + 0.14*c - 0.05*e - 0.05*i;
}

int main(void) {
    printf("resilience_value\n%.6f\n", resilience_value(8.7,8.0,8.4,8.6,9.1,7.4,8.3,3.9,3.2));
    return 0;
}
