#include <iostream>

double scenario_value(double h,double w,double s,double a,double p,double d,double g,double e,double t,double r,double i) {
    return 0.10*h + 0.10*w + 0.11*s + 0.12*a + 0.11*p + 0.10*d + 0.12*g + 0.12*e + 0.12*t - 0.04*r - 0.04*i;
}

int main() {
    std::cout << "scenario_resilience_value\n" << scenario_value(8.8,8.7,8.4,8.9,8.7,8.4,9.4,8.9,8.8,2.5,3.6) << "\n";
    return 0;
}
