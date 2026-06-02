#include <stdio.h>

double adaptive_learning_value(
    double monitoring_quality,
    double memory_retention,
    double feedback_use,
    double governance_flexibility,
    double community_knowledge,
    double justice_protection,
    double implementation_reliability,
    double forgetting_pressure
) {
    return 0.15 * monitoring_quality
        + 0.15 * memory_retention
        + 0.17 * feedback_use
        + 0.14 * governance_flexibility
        + 0.12 * community_knowledge
        + 0.11 * justice_protection
        + 0.09 * implementation_reliability
        - 0.07 * forgetting_pressure;
}

int main(void) {
    double score = adaptive_learning_value(8.1, 7.9, 8.8, 8.7, 7.9, 8.0, 8.0, 3.1);

    printf("monitoring_quality,memory_retention,feedback_use,governance_flexibility,community_knowledge,justice_protection,implementation_reliability,forgetting_pressure,adaptive_learning_value\n");
    printf("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.6f\n",
           8.1, 7.9, 8.8, 8.7, 7.9, 8.0, 8.0, 3.1, score);
    return 0;
}
