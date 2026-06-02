#include <stdio.h>

double functional_output(double abundance, double trait_contribution) {
    return abundance * trait_contribution;
}

int main(void) {
    double abundance = 0.88;
    double trait_contribution = 0.82;
    double output = functional_output(abundance, trait_contribution);

    printf("abundance,trait_contribution,functional_output\n");
    printf("%.4f,%.4f,%.6f\n", abundance, trait_contribution, output);
    return 0;
}
