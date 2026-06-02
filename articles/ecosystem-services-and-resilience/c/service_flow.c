#include <stdio.h>

double service_flow(double ecosystem_condition, double functional_capacity, double disturbance) {
    double flow = ecosystem_condition * functional_capacity * (1.0 - 0.35 * disturbance);
    if (flow < 0.0) return 0.0;
    if (flow > 1.0) return 1.0;
    return flow;
}

int main(void) {
    double condition = 0.62;
    double functional_capacity = 0.58;
    double disturbance = 0.18;
    double flow = service_flow(condition, functional_capacity, disturbance);

    printf("ecosystem_condition,functional_capacity,disturbance,service_flow\n");
    printf("%.4f,%.4f,%.4f,%.6f\n", condition, functional_capacity, disturbance, flow);
    return 0;
}
