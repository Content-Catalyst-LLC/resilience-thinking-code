#include <stdio.h>

double scenario_value(double h,double w,double s,double a,double p,double d,double g,double e,double t,double r,double i) {
    return 0.10*h + 0.10*w + 0.11*s + 0.12*a + 0.11*p + 0.10*d + 0.12*g + 0.12*e + 0.12*t - 0.04*r - 0.04*i;
}

int main(void) {
    printf("scenario_resilience_value\n%.6f\n", scenario_value(8.2,8.4,8.5,9.4,8.3,8.5,8.9,8.5,8.7,2.7,3.7));
    return 0;
}
