#include <stdio.h>

double ethical_resilience_value(double p,double e,double g,double r,double a,double b,double i) {
    return 0.24*p + 0.22*e + 0.18*g + 0.14*r + 0.14*a - 0.05*b - 0.03*i;
}

int main(void) {
    printf("ethical_resilience_value\n%.6f\n", ethical_resilience_value(8.4,9.0,8.6,8.3,8.8,2.8,3.8));
    return 0;
}
