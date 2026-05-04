# Resilience Thinking: Disturbance Scenario Comparison in R
# Educational example only.

library(tidyverse)

scenarios <- read_csv("../data/disturbance_scenarios.csv", show_col_types = FALSE)

score_scenario <- function(adaptive_capacity, threshold_distance, learning_capacity, redundancy,
                           disturbance_frequency, disturbance_intensity) {
  resilience_profile <-
    0.30 * adaptive_capacity +
    0.28 * threshold_distance +
    0.24 * learning_capacity +
    0.18 * redundancy

  disturbance_load <- disturbance_frequency * disturbance_intensity

  resilience_profile - disturbance_load
}

scenario_scores <- scenarios |>
  rowwise() |>
  mutate(
    resilience_margin = score_scenario(
      adaptive_capacity,
      threshold_distance,
      learning_capacity,
      redundancy,
      disturbance_frequency,
      disturbance_intensity
    ),
    high_concern = resilience_margin < 0.45
  ) |>
  ungroup()

dir.create("../outputs", showWarnings = FALSE, recursive = TRUE)

write_csv(scenario_scores, "../outputs/r_disturbance_scenario_scores.csv")

print(scenario_scores)
