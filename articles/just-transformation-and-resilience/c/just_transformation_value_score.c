#include <stdio.h>

double just_transformation_value(double r,double t,double e,double eco,double g,double l,double x,double b,double k,double i) {
    return 0.13*r + 0.16*t + 0.16*e + 0.13*eco + 0.14*g + 0.13*l + 0.13*x - 0.03*b - 0.02*k - 0.01*i;
}

int main(void) {
    printf("just_transformation_value\n%.6f\n", just_transformation_value(8.4,8.9,8.7,9.2,8.8,8.5,9.0,2.9,2.8,4.0));
    return 0;
}
