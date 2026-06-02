#include <stdio.h>

double support_value(double p,double s,double a,double g,double t,double x,double b,double i) {
    return 0.18*p + 0.18*s + 0.16*a + 0.14*g + 0.13*t + 0.16*x - 0.04*b - 0.01*i;
}

int main(void) {
    printf("support_resilience_value\n%.6f\n", support_value(8.5,8.6,8.7,8.5,8.4,8.7,2.7,3.9));
    return 0;
}
