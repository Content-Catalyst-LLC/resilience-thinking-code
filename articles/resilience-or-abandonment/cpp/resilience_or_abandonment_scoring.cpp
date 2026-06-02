#include <iostream>

double support_value(double p,double s,double a,double g,double t,double x,double b,double i) {
    return 0.18*p + 0.18*s + 0.16*a + 0.14*g + 0.13*t + 0.16*x - 0.04*b - 0.01*i;
}

int main() {
    std::cout << "support_resilience_value\n" << support_value(8.0,8.2,8.4,9.1,8.0,7.8,2.9,3.5) << "\n";
    return 0;
}
