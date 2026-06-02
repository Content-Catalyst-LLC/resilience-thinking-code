#include <iostream>

double resilience_value(double a,double b,double t,double g,double q,double d,double c,double e,double i) {
    return 0.16*a + 0.14*b + 0.16*t + 0.14*g + 0.14*q + 0.12*d + 0.14*c - 0.05*e - 0.05*i;
}

int main() {
    std::cout << "resilience_value\n" << resilience_value(8.9,7.7,8.8,9.2,8.8,8.1,8.5,3.9,3.5) << "\n";
    return 0;
}
