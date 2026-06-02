#include <stdio.h>

double adaptive_value(double p,double h,double l,double e,double t,double eco,double b,double i) {
    return 0.12*p + 0.20*h + 0.16*l + 0.16*e + 0.18*t + 0.14*eco - 0.03*b - 0.01*i;
}

int main(void) {
    printf("adaptive_resilience_value\n%.6f\n", adaptive_value(7.6,8.8,8.6,8.7,8.9,9.0,2.9,4.0));
    return 0;
}
