#include <iostream>

double adaptive_value(double p,double h,double l,double e,double t,double eco,double b,double i) {
    return 0.12*p + 0.20*h + 0.16*l + 0.16*e + 0.18*t + 0.14*eco - 0.03*b - 0.01*i;
}

int main() {
    std::cout << "adaptive_resilience_value\n" << adaptive_value(8.1,8.5,8.2,8.6,8.7,8.2,3.0,3.8) << "\n";
    return 0;
}
