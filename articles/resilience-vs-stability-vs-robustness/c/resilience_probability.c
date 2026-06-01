#include <math.h>
#include <stdio.h>

double sigmoid(double z) {
    return 1.0 / (1.0 + exp(-z));
}

double predict_failure(double adaptive, double threshold, double learning, double redundancy,
                       double modularity, double exposure, double sensitivity, double shock) {
    double protective = 0.24*adaptive + 0.22*threshold + 0.18*learning + 0.18*redundancy + 0.18*modularity;
    double pressure = 0.32*exposure + 0.28*sensitivity + 0.40*shock;
    return sigmoid(-2.0 + 4.2*pressure - 3.8*protective);
}

int main(void) {
    double p = predict_failure(0.38, 0.46, 0.33, 0.60, 0.43, 0.70, 0.58, 0.52);
    printf("predicted_failure_probability\n");
    printf("%.4f\n", p);
    return 0;
}
