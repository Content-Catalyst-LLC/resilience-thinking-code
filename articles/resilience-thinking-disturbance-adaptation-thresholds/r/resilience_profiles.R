# Resilience Thinking: Resilience Profiles in R
# Educational example only.

library(tidyverse)

systems <- read_csv("../data/resilience_profiles.csv", show_col_types = FALSE)

systems <- systems |>
  mutate(
    resilience_profile =
      0.18 * adaptive_capacity +
      0.17 * threshold_distance +
      0.16 * learning_capacity +
      0.13 * modularity +
      0.13 * redundancy +
      0.12 * governance_capacity +
      0.11 * equity_capacity
  )

systems_long <- systems |>
  pivot_longer(
    cols = c(
      adaptive_capacity,
      threshold_distance,
      learning_capacity,
      modularity,
      redundancy,
      governance_capacity,
      equity_capacity
    ),
    names_to = "dimension",
    values_to = "value"
  )

vulnerability_flags <- systems |>
  mutate(
    low_threshold_distance = threshold_distance < 0.55,
    low_redundancy = redundancy < 0.50,
    low_equity_capacity = equity_capacity < 0.50,
    vulnerability_flag =
      low_threshold_distance | low_redundancy | low_equity_capacity
  )

dir.create("../outputs", showWarnings = FALSE, recursive = TRUE)

write_csv(systems, "../outputs/r_resilience_profiles.csv")
write_csv(systems_long, "../outputs/r_resilience_dimensions_long.csv")
write_csv(vulnerability_flags, "../outputs/r_vulnerability_flags.csv")

print(systems)
print(vulnerability_flags)
