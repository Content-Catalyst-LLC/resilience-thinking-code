#include <iostream>

double ethical_resilience_value(double p,double e,double g,double r,double a,double b,double i) {
    return 0.24*p + 0.22*e + 0.18*g + 0.14*r + 0.14*a - 0.05*b - 0.03*i;
}

int main() {
    std::cout << "ethical_resilience_value\n" << ethical_resilience_value(8.2,8.7,9.1,9.4,8.9,2.7,4.0) << "\n";
    return 0;
}
